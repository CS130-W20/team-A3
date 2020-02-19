from users.__init__ import *
from auth import load_user
from users.modules.history import get_user_history
from users.modules.recommendation import recommend_course_for_user
# from users.modules.education import get_education_options
# from users.modules.portfolio import get_user_description, get_user_photo, remove_previous_image
# from users.modules.analyze import get_analyze_radar_data, get_analyze_line_data

from __init__ import application as app

users = Blueprint('user', __name__)

@users.route('/chatbot_handle', methods=['POST'])
def chatbot_handle():
    jsondata = request.form.get('data')
    data = json.loads(jsondata)
    text = data["text"]
    success, reply_text = chatbot(text)
    if success == 0:
        success = 1
        reply_text = "Sorry I can't understand what are you talking about."
    info = [{
            "success": success,
            "reply": reply_text
        }
    ]
    return json.dumps(info)

# for uploading the photo
@users.route('/upload_photo', methods=['POST'])
def upload_photo():
    direct_to = request.referrer or '/'
    if request.method == 'POST':
        f = request.files['img']
        filename_raw = secure_filename(f.filename)
        user_id = current_user.get_id()
        filename = "{}.{}".format(user_id, filename_raw.split(".")[-1])
        remove_previous_image(user_id, app.config["UPLOAD_FOLDER"])
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        # return 'file uploaded successfully'
    return redirect(direct_to)

@users.route('/user_data_vis/<user_id>', methods=['GET', 'POST'])
@users.route('/user_data_vis/<user_id>/<visualize_mode>/', methods=['GET', 'POST'])
@users.route('/user_data_vis/<user_id>/<visualize_mode>', methods=['GET', 'POST'])
def user_visualize(user_id=None, visualize_mode="0", methods=['GET', 'POST']):
    # visualize_mode is string
    welcome_page = redirect(url_for("main"))
    if user_id is None or user_id == -1:
        return welcome_page
    if visualize_mode == "0":
        # radar
        g.data = get_analyze_radar_data(user_id)
        g.mode = "radar"
    elif visualize_mode == "1":
        print("here")
        g.data = get_analyze_line_data(user_id, most_recent=30)
        g.mode = "line_chart"
    return render_template('pure_visualize.html')

@users.route('/home', methods=['GET', 'POST'])
@users.route('/home/<user_id>/', methods=['GET', 'POST'])
@users.route('/home/<user_id>', methods=['GET', 'POST'])
def user_home(user_id=None):
    '''
    could be @login_required, but I decided to let the anonymous users see our
    '''
    welcome_page = redirect(url_for("main"))
    print("TODO: do something to really implement the backend of the user panel")
    # return redirect(url_for("main"))
    authorized = False
    if user_id is None or user_id == -1:
        return welcome_page

    current_user_id = current_user.get_id()
    authorized = current_user_id==user_id

    try:
        show_user = load_user(user_id)
        if show_user.get_id() == -1 or not show_user.is_verified():
            return welcome_page
        g.show_user = show_user
        # actually it is also doable if we use the standard way of passing everything in
        # like
        # render_template('home.html', authorized=authorized, user=show_user)
        # so please feel free to switch back to the old fashion if there's any problem encountered by the use of g
    except:
        return welcome_page
    g.user_history = get_user_history(user_id)
    g.user_recommend = recommend_course_for_user(user_id)
    g.education_levels = get_education_options()
    g.user_description = get_user_description(user_id)
    # # g.user_image = get_user_photo(user_id, url_for("static", filename="img/users"))
    g.user_image = get_user_photo(user_id, app.config["UPLOAD_FOLDER"])
    # I think we don't need to make the interested fields explicitly shown there for the users each time
    # we use it as our initial value, and keep updating it in the backend, how about that?
    g.analyze_data = get_analyze_radar_data(user_id)
    return render_template('home.html', authorized=authorized)
