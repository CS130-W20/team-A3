"""
controllers.py
====================
Functionality in visualization: click on the concept button, show the visualization of the concept graph.
"""
from visualization.__init__ import *
from __init__ import concept_dict


visualizer = Blueprint('visualizer', __name__)

@visualizer.route('/concepts')
def showing_concepts():
    """
     The front-end interaction part. Render to the visualize.html webpage.

    """
    return render_template('visualize.html')


@visualizer.route('/concept_pure',methods=['GET', 'POST'])
def concept_visualize():
    """
    Draw the concept graph

    """
    g.concept = concept_dict["children"]
    return render_template('concept_visualize.html')

@visualizer.route('/aboutEduAI',methods=['GET', 'POST'])
def aboutEduAI():

    return render_template('aboutEduAI.html')


@visualizer.route('/contact',methods=['GET', 'POST'])
def contact():

    return render_template('contact.html')

