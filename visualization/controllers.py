from visualization.__init__ import *

visualizer = Blueprint('visualizer', __name__)

@visualizer.route('/concepts')
def showing_concepts():
    return render_template('visualize.html')