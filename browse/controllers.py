"""
controllers.py
====================
Functionality in Browse mode: 1.click box and expand. 2.click box and show the corresponding category introduction.
Creator: Zijie Huang
Data: Feb/18/2020
"""

import sys
sys.path.append("...")
from flask import request, session, Blueprint
from __init__ import browse_categories
import json
from search.controllers import high_search

# Define the blueprint: 'browse'
browse = Blueprint('browse', __name__)



def include_category_tree(tmp_tree, tmp_dict):
    """
    Return the catoegry tree dict from the input tmp_tree, tmp_dict
    :param tmp_tree: an input list
    :param tmp_dict: an input dictionary

    """
    for child in tmp_tree:
        tmp_dict[child["id"]] = child["category_name"]
        sub_categories = child.get("sub_categories", [])
        if len(sub_categories):
            tmp_dict = include_category_tree(sub_categories, tmp_dict)
    return tmp_dict

id2categories = include_category_tree(browse_categories, {-1: "Welcome to Education AI"})

def get_category_introduction(category_id=-1):
    """
    Return the catoegry introduction information given the category id.
    :param category_id: the id for the query category.

    """
    if category_id == -1:
        introduction = "We will help you get started with AI and enjoy your study."
    else:
        introduction = "brief introduction of category {}: {}".format(category_id, id2categories[category_id])
    return introduction


def get_category_content(category_id=-1):
    """
    Return the catoegry content information given the category id.
    :param category_id: the id for the query category.

    """
    if category_id == -1:
        content = [
            {   "title": "Hot Topics",
                "content": ["We have some keywords for you that are recent very popular:",
                    [
                        {"Machine Learning" : "search/search_keyword/machine learning"},
                        {"Artificial Intelligence": "search/search_keyword/Artificial Intelligence"},
                        {"Data Mining": "search/search_keyword/Data Mining"},
                        {"Big Data": "search/search_keyword/Big Data"}
                    ]
                ]
            },
            {   "title": "Popular Resource",
                "content": ["Here is a great visualization about concepts in computer science domain!"
                ],
                "link": "concepts"
            },
            {   "title": "What\'s New",
                "content": ["Here are some of the recently updates of our website"
                ],
                "link": "aboutEduAI"
            }
        ]
    else:
        category_name = id2categories[category_id]
        content = [
            {   "title": "Related Topics",
                "content": ["Check out our concept graph to find out related topics!"
                ],
                "link": "concepts"
            },
            {   "title": "Brief History",
                "content": ["The development of {} experienced the following main stages".format(category_name),
                    [
                        {"stage 1": "#"},
                        {"stage 2": "#"},
                        {"stage 3": "#"},
                        {"stage 4": "#"}
                    ]
                ],
                "link": "#"
            },
            {   "title": "Most Recent Paper",
                "content": ["Here are some of the most-recent research papers in {}... ".format(category_name)
                ],
                "link": "search/search_keyword/{}".format(category_name)
            }
        ]
    return content

def get_category_info(category_id):
    """
    Return the aggregated catoegry information (id,name,intro,content) given the category id.
    :param category_id: the id for the query category.

    """
    category_intro = get_category_introduction(category_id)
    category_name = id2categories[category_id]
    category_content = get_category_content(category_id)
    category_info = {"id": category_id, "name": category_name, "intro": category_intro, "content": category_content}
    return category_info


# handeling the category selection
@browse.route('/select_category', methods=['POST'])
def select_category():
    """
    The front-end interaction part. When calling from the front by ajax, it returns all needed information about the selected category.

    """
    jsondata = request.form.get('data')
    data = json.loads(jsondata)
    # Notice: this category id is turned to string after passing back from the front-end
    category_id = int(data["category_id"])
    if category_id == -1:
        print("TODO: category selection is canceled, please do something to clear the selection in the backend")
    else:
        print("TODO: category {} selected, please do something to implement browse mode".format(category_id))
    session["current_category"] = get_category_info(category_id)
    success = 1
    info = [{
        "success": success,
        "current_category": session["current_category"]
    }]
    return json.dumps(info)





