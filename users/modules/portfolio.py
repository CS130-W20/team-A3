import os
from flask import url_for

def get_user_description(user_id):
    return "Hi, I am user No.{}.".format(user_id)

def get_user_photo(user_id, user_imgs_path):
    '''
    Returns the name of the profile image for a user based on user ID
    '''
    all_imgs_names = os.listdir(user_imgs_path)

    file_name = "default.jpg"
    for img_name in all_imgs_names:
        img_id = img_name.split('.')[0]
        if len(img_id) and str(img_id) == str(user_id):
            file_name = img_name

    return file_name

def remove_previous_image(user_id, user_imgs_path):
    print("from user.modules.portfolio: remove_previous_image is not completely implemented yet. please implement it")
    all_imgs_names = os.listdir(user_imgs_path)
    for img_name in all_imgs_names:
        img_id = img_name.split('.')[0]
        if len(img_id) and str(img_id) == str(user_id):
            os.remove(os.path.join(user_imgs_path, img_name))
            '''
            in fact it'll be very expensive to loop through everyone when user size is large
            so we should keep a user portfolio indicating clearly which photo to use
            '''
