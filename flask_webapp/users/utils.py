import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_webapp import mail

#function to save the user profile pic uploaded by the user to our file system
def save_picture(form_picture):
    #we dont wnat to keep the file with the name they uploaded-->randomize the name
    random_hex = secrets.token_hex(8)#8 bytes
    #ensure the file is saved with the same extension it is uploaded
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pics', picture_fn)
    #resize the image before saving it to speed up our website---using pillow library
    output_size = (350,500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    #send user the email with reset token
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='noreply@demo.com',recipients=[user.email])
    msg.body=f'''To reset the password, visit the following link:
{url_for('users.reset_token',token=token,_external=True)}
 
If you did not make this request then simply ignore this email and no changes will be made.
'''
#_external is used cz we want an absolute url and not a relative url
#for longer/complicated msgs we can use the jinja2 templates
#route to enter the email address to rest the pswd
    mail.send(msg)
