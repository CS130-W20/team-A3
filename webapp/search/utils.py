import os

import xml.etree.ElementTree as ET
import sqlite3
import re

from search import DIR_PATH
from search import DIR_CONCEPT_PATH
from search import CONFIG_PATH

from search.search_engine import SearchEngine

def searchidlist(key, selected=0):
    """

    :param key:
    :param se:
    :param selected:
    :return:
    """
    se = SearchEngine(config_path=CONFIG_PATH, config_encoding='utf-8')
    flag, id_scores = se.search(key, selected)
    doc_id = [i for i, s in id_scores]
    page = []
    for i in range(1, (len(doc_id) // 10 + 2)):
        page.append(i)
    return flag, page, doc_id


def str_list_naive_parse(list_string):
    seps = '\', \'|\', \"|\", \'|\", \"'
    parsed = re.split(seps, list_string[2:-2])
    return parsed


def safe_et_find(root, elem_key, default=""):
    elem = root.find(elem_key)
    if elem is not None and elem.text is not None:
        return elem.text
    return default

def find(docid, extra=False):
    """

    :param docid:
    :param extra:
    :return:
    """
    docs = []
    for id in docid:
        root = ET.parse(DIR_PATH + '%s.xml' % id).getroot()
        id = root.find('id').text
        course_url = safe_et_find(root, 'course_url', "#")
        course_name = safe_et_find(root, 'course_name', "N/A")
        course_platform = safe_et_find(root, 'course_platform', "N/A")
        course_instructor = safe_et_find(root, 'course_instructor', "N/A")
        course_introduction = safe_et_find(root, 'course_introduction', "N/A")
        course_category = safe_et_find(root, 'course_category', "N/A")
        course_tag = safe_et_find(root, 'course_tag', "N/A")
        course_rating = safe_et_find(root, 'course_rating', "N/A")
        course_orgnization = safe_et_find(root, 'course_orgnization', "N/A")
        course_chapter = safe_et_find(root, 'course_chapter', "N/A").split("//")
        course_sub_chapter = safe_et_find(root, 'course_sub_chapter', "N/A")
        course_time = safe_et_find(root, 'course_time', "N/A")
        reviews = str_list_naive_parse(safe_et_find(root, 'reviews', "N/A"))
        reviewers = safe_et_find(root, 'reviewers', "N/A")
        review_date = safe_et_find(root, 'review_date', "N/A")
        print("from search.utils.find: the video information is fake, please fix it here")
        # for Youtube video, in order to display them inline, we need to change the url to */embed/*
        # videos from other sites might have other tricks
        video_urls = ["https://www.youtube.com/embed/aircAruvnKk"]
        doc = {'id': id, 'course_url': course_url, 'course_name': course_name,
               'course_platform': course_platform, 'course_instructor': course_instructor,
               'course_introduction': course_introduction, 'course_category': course_category,
               'course_tag': course_tag, 'course_rating': course_rating, 'course_orgnization': course_orgnization,
               'course_chapter': course_chapter, 'course_sub_chapter': course_sub_chapter,
               'course_time': course_time, 'reviews': reviews, 'reviewers': reviewers,
               'review_date': review_date, 'extra': [], 'video_urls': video_urls}

        if extra:
            pass
        docs.append(doc)
    return docs


def find_concept(docid, extra=False):
    """

    :param docid:
    :param extra:
    :return:
    """
    docs = []
    for id in docid:
        root = ET.parse(DIR_CONCEPT_PATH + '%s.xml' % id).getroot()
        id = root.find('id').text
        course_url = safe_et_find(root, 'course_url', "#")
        course_name = safe_et_find(root, 'course_name', "N/A")
        course_platform = safe_et_find(root, 'course_platform', "N/A")
        course_instructor = safe_et_find(root, 'course_instructor', "N/A")
        course_introduction = safe_et_find(root, 'course_introduction', "N/A")
        course_category = safe_et_find(root, 'course_category', "N/A")
        course_tag = safe_et_find(root, 'course_tag', "N/A")
        course_rating = safe_et_find(root, 'course_rating', "N/A")
        course_orgnization = safe_et_find(root, 'course_orgnization', "N/A")
        course_chapter = safe_et_find(root, 'course_chapter', "N/A").split("//")
        course_sub_chapter = safe_et_find(root, 'course_sub_chapter', "N/A")
        course_time = safe_et_find(root, 'course_time', "N/A")
        reviews = str_list_naive_parse(safe_et_find(root, 'reviews', "N/A"))
        reviewers = safe_et_find(root, 'reviewers', "N/A")
        review_date = safe_et_find(root, 'review_date', "N/A")
        print("from search.utils.find: the video information is fake, please fix it here")
        # for Youtube video, in order to display them inline, we need to change the url to */embed/*
        # videos from other sites might have other tricks
        video_urls = ["https://www.youtube.com/embed/aircAruvnKk"]
        doc = {'id': id, 'course_url': course_url, 'course_name': course_name,
               'course_platform': course_platform, 'course_instructor': course_instructor,
               'course_introduction': course_introduction, 'course_category': course_category,
               'course_tag': course_tag, 'course_rating': course_rating, 'course_orgnization': course_orgnization,
               'course_chapter': course_chapter, 'course_sub_chapter': course_sub_chapter,
               'course_time': course_time, 'reviews': reviews, 'reviewers': reviewers,
               'review_date': review_date, 'extra': [], 'video_urls': video_urls}

        if extra:
            pass
        docs.append(doc)
    return docs


def cut_page(page, no, doc_id):
    """

    :param page:
    :param no:
    :return:
    """
    docs = find(doc_id[no*10:page[no]*10])
    return docs


def get_k_nearest(db_path, docid, k=5):
    """
        Gets the "k" nearest documents to document with id = docid.
    :param db_path:     Courses database path
    :param docid:       Document ID
    :param k:           number of nearest documents to fetch
    :return: List of documents.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM knearest WHERE id=?", (docid,))
    docs = c.fetchone()
    conn.close()
    return docs[1: 1 + (k if k < 5 else 5)]  # max = 5

