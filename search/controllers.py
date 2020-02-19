from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for

from search.utils import cut_page, find, searchidlist, \
    get_k_nearest
from search.search_engine import SearchEngine
from search import CONFIG_PATH
from __init__ import browse_categories

# Define the blueprint: 'search', and set its url prefix: search
searcher = Blueprint('searcher', __name__, url_prefix='/search/')



@searcher.route('/', methods=['POST'])
def search():
    """
    Implements search functionality to find courses.
    Input: (via POST)
        - Form containing:
            * key_word

    :return:
        HTML template with the results.
    """

    try:
        checked = ['checked="true"', '', '']
        keys = request.form['key_word']
        category = request.form['search_field']
        session['checked'] = checked
        session['keys'] = keys

        if keys not in ['']:
            flag, page, docid = searchidlist(keys)
            session['page'] = page
            session['s_flag'] = flag
            session['doc_id'] = docid

            if flag == 0:
                return render_template('search.html', nonempty=False, welcome=False,
                                       browse_categories=browse_categories)

            docs = cut_page(page, 0, docid)
            return render_template('high_search.html', checked=checked, key=keys, docs=docs, page=page,
                                   nonempty=True, welcome=False, browse_categories=browse_categories)
        else:
            return render_template('search.html', nonempty=False, welcome=True, browse_categories=browse_categories)

    except Exception as e:
        print('search error')
        print(e)
        return render_template('search.html', nonempty=False, welcome=True, browse_categories=browse_categories)


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

@searcher.route('concepts/<id>/', methods=['GET', 'POST'])
def content_concept(id):
    """
    Fetch concept content with document id = id.
    :param id:
    :return:
    """
    try:
        doc = find_concept([id], extra=True)
        return render_template('concept.html', doc=doc[0])
    except Exception(e):
        print('content error' + e)
        return error_page()

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


@searcher.route('/search/<key>/', methods=['POST'])
def high_search(key):
    """

    :param key:
    :return:
    """
    # REVIEW:
    # The errors should throw a 404 or a 500.
    # Not die silently.
    try:

        selected = int(request.form['order'])
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
            return render_template('search.html', nonempty=False, welcome=False)
        docs = cut_page(page, 0)
        return render_template('high_search.html', checked=session['checked'], key=session['keys'], docs=docs, page=page,
                               nonempty=True, welcome=False)
    except:
        print('high search error')






