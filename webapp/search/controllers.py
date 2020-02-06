from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for

from search.utils import cut_page, find, searchidlist, \
    get_k_nearest
from search.search_engine import SearchEngine
from search import CONFIG_PATH
from __init__ import browse_categories

# Define the blueprint: 'search', and set its url prefix: search
searcher = Blueprint('searcher', __name__, url_prefix='/search/')

def error_page():
    return render_template('search.html', nonempty=False, welcome=False, browse_categories=browse_categories)

def is_valid_keys(keys):
    return keys not in ['']

@searcher.route('/', methods=['POST', 'GET'])
def search():
    """
        Implements search functionality to find courses.
        Input: (via POST)
            - Form containing:
               * key_word

    :return:
        HTML template with the results.
    """
    # request.form = {"form_name": "hi"}
    form_name = request.form.get("form_name")
    if form_name == "search":
        checked = ['checked="true"', '', '']
        keys = request.form.get('key_word', "")
        category = request.form.get('search_field')
        print("from search.controllers.search: category hasn't been added as a search option, will do later")
        session['checked'] = checked
        session['keys'] = keys
    else:
        if session.get("checked") is None or session.get("keys") is None:
            print('unrecognized form named {}'.format(form_name))
            return error_page()
        else:
            checked = session['checked']
            keys = session['keys']

    if is_valid_keys(keys):
        flag, page, docid = searchidlist(keys)
        session['page'] = page
        session['s_flag'] = flag
        session['doc_id'] = docid

        if flag == 0: return error_page()

        docs = cut_page(page, 0, docid)

        return render_template('high_search.html', checked=checked, key=keys, docs=docs, page=page,
                               nonempty=True, welcome=False, browse_categories=browse_categories)
    else:
        return redirect(url_for('main'))


@searcher.route('page/<page_no>/', methods=['GET'])
def next_page(page_no):
    """

    :param page_no:
    :return:
    """
    page, checked, docid = session['page'], session['checked'], session['doc_id']
    try:
        page_no = int(page_no)
        docs = cut_page(page, (page_no - 1), docid)
        return render_template('high_search.html', checked=checked, key=session['keys'], docs=docs, page=page,
                               nonempty=True, welcome=False, browse_categories=browse_categories)
    except:
        print('next error')


@searcher.route('/<id>/', methods=['GET', 'POST'])
def content(id):
    """
    Fetch content with document id = id.
    :param id:
    :return:
    """
    try:
        doc = find([id], extra=True)
        return render_template('content.html', doc=doc[0])
    except:
        print('content error')
        return error_page()


@searcher.route('/key/<key>/', methods=['POST'])
def high_search(key):
    """

    :param key:
    :return:
    """
    # REVIEW:
    # The errors should throw a 404 or a 500.
    # Not die silently.
    form_name = request.form.get("form_name")
    if form_name == "search_option":
        selected = int(request.form.get('order', 0))
        for i in range(3):
            if i == selected:
                session['checked'][i] = 'checked="true"'
            else:
                session['checked'][i] = ''
        flag, page, docid = searchidlist(key, selected)
        session['s_flag'] = flag
        session['page'] = page
        session['doc_id'] = docid
        if flag == 0:
            return error_page()
        docs = cut_page(page, 0, docid)
        return render_template('high_search.html', checked=session['checked'], key=session['keys'], docs=docs, page=page,
                               nonempty=True, welcome=False, browse_categories=browse_categories)
    else:
        print('high search error')
        return error_page()






