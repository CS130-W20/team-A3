"""
crawler.py
====================
Crawl course information from coursera.
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import xml.etree.ElementTree as ET
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager

def get_one_subchap(html):
    """
       Return webpage content list, given an input html.
    """
    subchap_html = html.contents[0].contents[0]
    sub_chap = []
    for i in range(1,len(subchap_html)):
        try:
            sub_chap.append(subchap_html.contents[i].a.string)
        except:
            sub_chap.append(subchap_html.contents[i].contents[1])
    return sub_chap

def get_syllabus(syllabus):
    """
       Error Handling when gettiing a content list from an input html.

    """
    try:
        sub = get_one_subchap(syllabus)
    except:
        sub = ["$null$"]
    return sub

def get_syllabus_list(soup):
    """
       Return a syllabuslist for a given course.

    """
    Syllabus_html = soup.find_all("div",class_="SyllabusModuleDetails")
    syllabuslist = [get_syllabus(syllabus) for syllabus in Syllabus_html]
    return syllabuslist

def save_xml(meta,doc_path="./data_courses/"):
    """
      Write data into an xml file.

    """
    doc = ET.Element("doc")
    for key in meta.keys():
        ET.SubElement(doc, key).text = str(meta[key])
    tree = ET.ElementTree(doc)
    tree.write(str(doc_path)+meta["id"]+".xml", encoding = "utf-8", xml_declaration = True)


def crawel_one_web_coursera(url, cnt, null_tag, null_star):
    """
    Return crawled coursera page for an input course url.
    :param url: course url
    :param cnt: course id

    """
    meta = {}
    url = url
    html = urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(html, "lxml")

    course_url = url
    course_name = soup.title.string.split("|")[0].strip()
    course_platform = soup.title.string.split("|")[1].strip()
    course_instructor = soup.find_all("a", class_="link-no-style", href=re.compile("/instructor/*"))[0].string
    course_introduction = soup.find_all("div", class_="content-inner")[0].p.string
    course_category = ".".join([(soup.find_all("div", class_="BreadcrumbItem_1pp1zxi"))[i].a.string for i in [0, 1, 2]])
    try:
        tag_html = soup.find_all("div", class_="Box_120drhm-o_O-displayflex_poyjc-o_O-wrap_rmgg7w")[0].contents
        course_tag = "//".join([span.string for span in tag_html])
    except:
        course_tag = ""
        print("course_tag is null:{}".format(url))
        null_tag.append(url)
    try:
        course_rating = soup.find_all("span", itemprop="ratingValue")[0].string
    except:
        try:
            course_rating = \
            soup.find_all("span", class_="H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-l-1s m-r-1 m-b-0")[0].text
        except:
            course_rating = ""
            print("course_rating is null:{}".format(url))
            null_star.append(url)
    try:
        course_orgnization = soup.find_all("img", class_=re.compile("rectangular.*"))[0]["title"]
    except:
        course_orgnization = soup.find_all("span", class_="text-uppercase")[0].text
    chapter_html = soup.find_all("h2", class_="H2_1pmnvep-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-2")
    course_chapter = "//".join([chap.string for chap in chapter_html])
    course_sub_chapter = get_syllabus_list(soup)
    course_time = soup.find_all("h4")[-2].string

    url2 = url + "/reviews"
    html2 = urlopen(url2).read().decode("utf-8")
    soup2 = BeautifulSoup(html2, "lxml")

    review_html = soup2.find_all("div", class_="rc-CML font-lg styled")
    reviews = [review.p.string for review in review_html]
    reviewers_html = soup2.find_all("p", class_="reviewerName p-x-1s m-b-0 text-secondary font-xs")
    reviewers = [review.string for review in reviewers_html]
    review_date_html = soup2.find_all("p", class_="dateOfReview")
    review_date = [review.string for review in review_date_html]

    #     meta["id"] = str(course_platform)+"_"+ str(course_name)+"_"+ str(course_instructor)
    meta["id"] = str(course_platform) + "_" + str(cnt)
    meta["course_url"] = course_url
    meta["course_name"] = course_name
    meta["course_platform"] = course_platform
    meta["course_instructor"] = course_instructor
    meta["course_introduction"] = course_introduction
    meta["course_category"] = course_category
    meta["course_tag"] = course_tag
    meta["course_rating"] = course_rating
    meta["course_orgnization"] = course_orgnization
    meta["course_chapter"] = course_chapter
    meta["course_sub_chapter"] = course_sub_chapter
    meta["course_time"] = course_time
    meta["reviews"] = reviews
    meta["reviewers"] = reviewers
    meta["review_date"] = review_date

    return meta, null_tag, null_star


def crawel_one_tag_coursera(url="https://www.coursera.org/browse/data-science"):
    """
       Return crawled course tag from coursera given its corresponding url.
       :param url: course url

    """

    full = []
    url = url
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="c-ph-right-nav"]/ul/li[4]/a').click()
    driver.find_element_by_xpath('//*[@id="emailInput_4-input"]').send_keys('songjiang@cs.ucla.edu')
    driver.find_element_by_xpath('//*[@id="passwordInput_47-input"]').send_keys('Blackmamba24.')
    driver.find_element_by_xpath(
        '//*[@id="authentication-box-content"]/div/div[2]/div/div[1]/form/div[1]/button/span').click()
    time.sleep(180)
    print("start scroll pages")

    def scroll_pages(times):
        base_url = "https://www.coursera.org"
        for i in range(times + 1):
            driver.execute_script("window.scrollBy(0, 300)")
            time.sleep(3)
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            url_html = soup.find_all("a", class_="nostyle search-offering-card")
            full.extend([base_url + uhtml["href"] for uhtml in url_html])
            print(i)

    scroll_pages(400)
    l1 = full
    l2 = list(set(l1))
    l2.sort(key=l1.index)
    print ("There are totally {} urls".format(len(l2)))
    return l2

if __name__ == "__main__":
    url = "https://www.coursera.org/browse/data-science"
    url_list = crawel_one_tag_coursera()
    null_tag = []
    null_star = []
    for i in range(0, len(url_list)):
        url = url_list[i]
        print(i, url)
        meta, null_tag, null_star = crawel_one_web_coursera(url, i, null_tag, null_star)
        save_xml(meta)
        print("done")
        i = i + 1
    print (len(null_tag))
    print (len(null_tag))
