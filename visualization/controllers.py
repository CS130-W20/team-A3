from visualization.__init__ import *
from __init__ import concept_dict


visualizer = Blueprint('visualizer', __name__)

@visualizer.route('/concepts')
def showing_concepts():
    return render_template('visualize.html')


@visualizer.route('/concept_pure',methods=['GET', 'POST'])
def concept_visualize():
    g.concept = concept_dict
    return render_template('concept_visualize.html')




