# -*- coding: utf-8 -*-
"""
Define SearchEngine class
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
    """
    This is a class for search operations

    Attributes:
        config_path (string): configuration path
        config_encoding (string): data files encoding format
        stop_words (set<string>): set of stop words
        conn (Object): connection to database
        K1 (float): K1 (parameter used in search algorithm)
        B (float): B (parameter used in search algorithm)
        N (int): N (parameter used in search algorithm)
        AVG_L (float): average length of document in corpus
    """
    def __init__(self, config_path, config_encoding):
        """
        The constructor for SearchEngine class

        Parameters:
            config_path (string): configuration path
            config_encoding (string): data files encoding format        
        """
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
        """
        Closes connection to database
        """
        self.conn.close()

    def is_number(self, s):
        """
        Checks whether a string is a number or not.

        Parameters:
            s (string): the string to be checked.

        Returns:
            True or False
        """
        try:
            float(s)
        except ValueError:
            return False
        return True

    def clean_list(self, seg_list):
        """
        clean a list of string and map to dictionary

        Parameters:
            seg_list (list<string>): a list of string

        Returns:
            cleaned_dict (dictionary): map<string, int>, cleaned word and its count in the list
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
        Retrieves docs from database

        Parameters:
            term (string): word
        
        Returns:
            (Object): retrieved documents
        """
        c = self.conn.cursor()
        c.execute('SELECT * FROM postings WHERE term=?', (term,))
        return c.fetchone()

    def getIDF(self, file):
        """
        Get a dictionary of word and its idf (inverse-document-frequency) value from the corpus

        Parameters:
            file (string): path to the idf file
        
        Returns:
            idfDict (dictionary): Map<string, float>, word and its idf value
        """
        idfDict = {}
        with open(file,'r', encoding='utf-8') as f:
            for x in f.readlines():
                w,v = x.split()
                idfDict[w] = v
        return idfDict

    def tfIdf(self, tf, idf, k, b, length, avglen = 2200):
        """
        Calculates the tf-idf value of a word

        Parameters:
            tf (float): word tf value
            idf (float): word idf value
            k (float): parameter, usually between [1.2, 2.0]
            b (float): parameter, usually 0.75

        Returns:
            float: tf-idf value
        """
        return idf*tf*(k+1)/(tf+k*(1-b+b*length/avglen))

    def Replace(self, content):
        """
        preprocessing doc content

        Parameters:
            content (string): input string

        Returns:
            content (string): preprocessed string
        """
        content = content.replace("\"","")
        content = content.replace("'", "")
        content = content.replace("[", "")
        content = content.replace("]", "")
        content = content.replace("/", " ")
        content = content.replace("//", " ")
        content = content.replace(".", " ")
        return content

    def minDistance(self, word1, word2):
        """
        Calculate edit distance between two words, including insertion, deletion, and replacement

        Parameters:
            word1 (string)
            word2 (string)

        Returns:
            int: edit distance
        """
        m, n = len(word1), len(word2)  # switch word1 and word2 if m < n to ensure n ≤ m
        curr = list(range(n+1))
        for i in range(m):
            prev, curr = curr, [i+1] + [0] * n
            for j in range(n):
                curr[j+1] = prev[j] if word1[i] == word2[j] else min(curr[j], prev[j], prev[j+1]) + 1
        return curr[n]

    def result_by_BM25(self, sentence):
        """
        Get ranking results using BM25 (tf-idf) IR algorithm (with spelling error tolerance within edit distance two)

        Parameters:
            sentence (string): keyword string typed by user
        
        Returns:
            0, []: no document is found that matches any of the keywords
            1, BM25_scores (list<tuple>): retrived docids and their ranking scores
        """
        idfDict = self.getIDF('search/idf.txt')
        seg_list = jieba.lcut(sentence, cut_all=False)
        #seg_list = nltk.word_tokenize(sentence)
        cleaned_dict = self.clean_list(seg_list)
        BM25_scores = {}
        for term in cleaned_dict.keys():
            print(term)
            r = self.fetch_from_db(term)
            if r is None:
                #add edit distance checking (tolerate error within edit distance 2)
                for k in idfDict.keys():
                    if self.minDistance(term, k) < 3:
                        print(k)
                        r = self.fetch_from_db(k)
                        if r is None:
                            continue
                        else:
                            break
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

    def result_by_recommendation(self, sentence):
        """
        Get ranking results using recommendation system

        Parameters:
            sentence (string): keyword string typed by user
        
        Returns:
            0, []: no document is found that matches any of the keywords
            1, time_scores (list<tuple>): retrived docids and their ranking scores
        """
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

    def result_by_popularity(self, sentence):
        """
        Get ranking results using popularity

        Parameters:
            sentence (string): keyword string typed by user
        
        Returns:
            0, []: no document is found that matches any of the keywords
            1, hot_scores (list<tuple>): retrived docids and their ranking scores
        """
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
        """
        Which algorithm to use for search ranking

        Parameters:
            sentence (string): keyword string typed by user
            sort_type: ranking strategy (0 for BM25, 1 for popularity, 2 for time)

        Returns:
            list<tuple>: sorted results of documents 
        """
        if sort_type == 0:
            return self.result_by_BM25(sentence)
        elif sort_type == 1:
            return self.result_by_popularity(sentence)
        elif sort_type == 2:
            return self.result_by_recommendation(sentence)


# For testing purpose only.
if __name__ == "__main__":
    se = SearchEngine('../config.ini', 'utf-8')
    flag, rs = se.search('', 0)
