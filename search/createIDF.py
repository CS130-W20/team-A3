"""
Create IDf file
"""
from os import listdir
import xml.etree.ElementTree as ET
import jieba
import sqlite3
import configparser
import nltk

def Replace(content):
    """
    preprocessing doc content (this function aligns with the SearchEngine.Replace)

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

def is_number(w):
    """
    Checks whether a string is a number or not.

    Parameters:
        s (string): the string to be checked.

    Returns:
        True or False
    """
    try:
        float(w)
    except ValueError:
        return False
    return True

total_len = 0
files = listdir('../database/data_courses/')
word2doc={}
#list1 = ['course_name', 'course_platform', 'course_instructor', 'course_introduction', 'course_category', 'course_tag', 'course_organization', 'course_chapter', 'course_sub_chapter', 'reviews']
for i in files:
    doc = set()
    root = ET.parse('../database/data_courses/' + i).getroot()
    for child in root:
        content = root.find(child.tag).text
        #if child.tag in list1:
        if not content:
            print(i, child.tag)
            continue
        content = Replace(content)
        tokens = jieba.lcut(content, cut_all=False)
        total_len = total_len + len(tokens)
        #tokens = jieba.cut_for_search(content)
        for w in tokens:
            if w!='' and not is_number(w):
                doc.add(w.strip().lower())
    for w in doc:
        if w not in word2doc:
            word2doc[w] = 1
        else:
            word2doc[w] = word2doc[w] + 1
        
N = len(files)
import numpy as np
i = 0
with open("idf.txt",'w',encoding='utf-8') as f:
    for w,v in word2doc.items():
        if i == 0:
            continue #skip first line because w is empty
        i = i + 1
        idf = np.log(N/(1+v))
        f.write(w+' '+str(idf)+'\n')
        
print(total_len/N) #average doc length (used in BM25 ranking algorithm)