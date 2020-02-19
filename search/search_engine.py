# -*- coding: utf-8 -*-
"""

"""

import jieba
import nltk
import math
import operator
import sqlite3
import configparser
from datetime import *
import numpy as np


class SearchEngine:
    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)

        # Read stopwords
        with open(config['DEFAULT']['stop_words_path'],
                  encoding=config['DEFAULT']['stop_words_encoding']) as f:
            words = f.read()
            self.stop_words = set(words.split('\n'))

        # Open connection to course database.
        self.conn = sqlite3.connect(config['DEFAULT']['db_path'])

        # Read search function IR parameters
        self.K1 = float(config['DEFAULT']['k1'])
        self.B = float(config['DEFAULT']['b'])
        self.N = int(config['DEFAULT']['n'])
        self.AVG_L = float(config['DEFAULT']['avg_l'])

    def __del__(self):
        self.conn.close()

    def is_number(self, s):
        """
            Checks if a string is a number or not.
        :param s: the string to be checked.
        :return: True or False
        """
        try:
            float(s)
        except ValueError:
            return False
        return True

    def clean_list(self, seg_list):
        """

        :param seg_list:
        :return:
        """
        cleaned_dict = {}
        for i in seg_list:
            i = i.strip().lower()
            if i != '' and not self.is_number(i):  # and i not in self.stop_words:
                if i in cleaned_dict:
                    cleaned_dict[i] = cleaned_dict[i] + 1
                else:
                    cleaned_dict[i] = 1
        return cleaned_dict

    def fetch_from_db(self, term):
        """

        :param term:
        :return:
        """
        c = self.conn.cursor()
        c.execute('SELECT * FROM postings WHERE term=?', (term,))
        return c.fetchone()

    def getIDF(self, file):
        idfDict = {}
        with open(file,'r', encoding='utf-8') as f:
            for x in f.readlines():
                w,v = x.split()
                idfDict[w] = v
        return idfDict

    def tfIdf(self, tf, idf, k, b, length, avglen = 2200):
        return idf*tf*(k+1)/(tf+k*(1-b+b*length/avglen))

    def Replace(self, content):
        content = content.replace("\"","")
        content = content.replace("'", "")
        content = content.replace("[", "")
        content = content.replace("]", "")
        content = content.replace("/", " ")
        content = content.replace("//", " ")
        content = content.replace(".", " ")
        return content

    def result_by_BM25(self, sentence):
        idfDict = self.getIDF('search/idf.txt')
        seg_list = jieba.lcut(sentence, cut_all=False)
        #seg_list = nltk.word_tokenize(sentence)
        cleaned_dict = self.clean_list(seg_list)
        BM25_scores = {}
        # print ("before for")
        for term in cleaned_dict.keys():
            r = self.fetch_from_db(term)
            if r is None:
                continue
            docs = r[2].split('\!@#$')
            for doc in docs:
                tf = 0
                docid = doc.split('\%^&*')[0]
                doc = self.Replace(doc)
                tokens = jieba.lcut(doc, cut_all=False)
                for w in tokens:
                    w = w.strip().lower()
                    if w == term:
                        tf = tf + 1
                score = 0
                if term in idfDict.keys():
                    score = self.tfIdf(tf, float(idfDict[term]), 1.5, 0.75, len(tokens), avglen = 2200)
                if docid in BM25_scores:
                    BM25_scores[docid] = BM25_scores[docid] + score
                else:
                    BM25_scores[docid] = score
        BM25_scores = sorted(BM25_scores.items(), key=operator.itemgetter(1))
        BM25_scores.reverse()
        if len(BM25_scores) == 0:
            return 0, []
        else:
            return 1, BM25_scores

    def result_by_time(self, sentence):
        seg_list = jieba.lcut(sentence, cut_all=False)
        n, cleaned_dict = self.clean_list(seg_list)
        time_scores = {}
        for term in cleaned_dict.keys():
            r = self.fetch_from_db(term)
            if r is None:
                continue
            docs = r[2].split('\n')
            for doc in docs:
                docid, date_time, tf, ld = doc.split('\t')
                if docid in time_scores:
                    continue
                news_datetime = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
                now_datetime = datetime.now()
                td = now_datetime - news_datetime
                docid = int(docid)
                td = (timedelta.total_seconds(td) / 3600)  # hour
                time_scores[docid] = td
        time_scores = sorted(time_scores.items(), key=operator.itemgetter(1))
        if len(time_scores) == 0:
            return 0, []
        else:
            return 1, time_scores

    def result_by_hot(self, sentence):
        seg_list = jieba.lcut(sentence, cut_all=False)
        n, cleaned_dict = self.clean_list(seg_list)
        hot_scores = {}
        for term in cleaned_dict.keys():
            r = self.fetch_from_db(term)
            if r is None:
                continue
            df = r[1]
            w = math.log2((self.N - df + 0.5) / (df + 0.5))
            docs = r[2].split('\n')
            for doc in docs:
                docid, date_time, tf, ld = doc.split('\t')
                docid = int(docid)
                tf = int(tf)
                ld = int(ld)
                news_datetime = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
                now_datetime = datetime.now()
                td = now_datetime - news_datetime
                BM25_score = (self.K1 * tf * w) / (tf + self.K1 * (1 - self.B + self.B * ld / self.AVG_L))
                td = (timedelta.total_seconds(td) / 3600)  # hour
                hot_score = math.log(BM25_score) + 1 / td
                if docid in hot_scores:
                    hot_scores[docid] = hot_scores[docid] + hot_score
                else:
                    hot_scores[docid] = hot_score
        hot_scores = sorted(hot_scores.items(), key=operator.itemgetter(1))
        hot_scores.reverse()
        if len(hot_scores) == 0:
            return 0, []
        else:
            return 1, hot_scores

    def search(self, sentence, sort_type=0):
        if sort_type == 0:
            return self.result_by_BM25(sentence)
        elif sort_type == 1:
            return self.result_by_hot(sentence)
        elif sort_type == 2:
            return self.result_by_time(sentence)


# For testing purpose only.
if __name__ == "__main__":
    se = SearchEngine('../config.ini', 'utf-8')
    flag, rs = se.search('', 0)
