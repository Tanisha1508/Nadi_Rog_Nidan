from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed #--to upload a profile pic
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError,InputRequired
from flask_webapp.db_models import User


#create forms using classes which then get converted to html templates

#create a registeration form

class DataCollectionForm(FlaskForm):
    size = SelectField(
        "Body size",
        [DataRequired()],
        choices=[
            "slim","medium","heavy"
        ],
    )
    weight = SelectField(
        "Weight",
        [DataRequired()],
        choices=[
            "low","medium","overweight"
        ],
    )
    chin = SelectField(
        "Chin Shape",
        [DataRequired()],
        choices=[
            "angular","triangular","rounded/double chin"
        ],
    )
    cheeks = SelectField(
        "Cheeks",
        [DataRequired()],
        choices=[
            "wrinkled","smooth","rounded"
        ],
    )
    eyeshape = SelectField(
        "Eye shape",
        [DataRequired()],
        choices=[
            "small","sharp","big"
        ],
    )
    eyecolor = SelectField(
        "Eye color",
        [DataRequired()],
        choices=[
            "black/brown","gray/green","blue"
        ],
    )
    nose = SelectField(
        "Nose shape",
        [DataRequired()],
        choices=[
            "uneven shape","long pointed","short rounded"
        ],
        default="uneven shape"
    )
    teeth_gums = SelectField(
        "Teeth gums",
        [DataRequired()],
        choices=[
            "thin","tender","strong"
        ],
    )
    skin = SelectField(
        "Skin type",
        [DataRequired()],
        choices=[
           "dry","smooth oily","thick oily"
        ],
    )
    skin_color = SelectField(
        "Skin color",
        [DataRequired()],
        choices=[
            "dark","rosy","pale"
        ],
    )
    hair = SelectField(
        "Hair type",
        [DataRequired()],
        choices=[
            "dry","straight","curly"
        ],
    )
    hair_color = SelectField(
        "Hair color",
        [DataRequired()],
        choices=[
            "dark gray","blonde/red","black/brown"
        ],
    )
    appetite = SelectField(
        "Appetite",
        [DataRequired()],
        choices=[
            "irregular","strong","slow but steady"
        ],
    )
    digestion = SelectField(
        "Digestion",
        [DataRequired()],
        choices=[
            "irregular","quick","prolonged"
        ],
    )
    thirst = SelectField(
        "Thirst",
        [DataRequired()],
        choices=[
            "changeable","surplus","sparse"
        ],
    )
    emotions = SelectField(
        "Emotions",
        [DataRequired()],
        choices=[
            "anxiety","anger","calm"
        ],
    )
    mind = SelectField(
        "Mind",
        [DataRequired()],
        choices=[
            "restless","impatient","calm"
        ],
    )
    intellect = SelectField(
        "Intellect",
        [DataRequired()],
        choices=[
            "quick but faulty","accurate","slow/exact"
        ],
    )
    speech = SelectField(
        "Speech",
        [DataRequired()],
        choices=[
            "rapid/unclear","clear/sharp","slow/monotonous"
        ],
    )
    voice = SelectField(
        "Voice",
        [DataRequired()],
        choices=[
            "weak","strong","deep"
        ],
    )
    lips = SelectField(
        "Lips type",
        [DataRequired()],
        choices=[
            "dry","red","smooth"
        ],
    )
    submit = SubmitField('Predict Dosha')


class RegisterationForm(FlaskForm):
    #different form fields which will be imported classes as well
    #apply checks and validations--use validators--classes imported
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)]) 
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])#can add min len validator also
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    #now we need a submit button that sends the info to us
    submit = SubmitField('Sign Up')

    # create a custom validations by creating a fn here---a template for the validation error
    # def validate_field(self,field):
    #     if True:
    #         raise ValidationError('Validation Message')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose another username!')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please choose another email address!')


#create a login form
class LoginForm(FlaskForm):
    #username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)]) 
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)]) 
    email = StringField('Email',validators=[DataRequired(),Email()])
    #to upload a pic
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose another username!')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists. Please choose another email address!')


# when we use these forms we need to set a secret key for our app which will protect against modifying cookies 
# and cross-site request forgery attacks etc
# we add a secret key in flask_webapp.py under app

#form to reset the pswd by submitting the email:
class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')
    #check/validate if the user has an account or not:
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


#form to pass pswd and conf pswd fields to reset pswd:
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])#can add min len validator also
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')