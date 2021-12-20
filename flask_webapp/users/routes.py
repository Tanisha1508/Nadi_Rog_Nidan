#users blueprint
from typing import final
from flask import render_template, url_for, flash, redirect, request, Blueprint,session
from flask_login import login_user, current_user, logout_user, login_required
from flask_webapp import db, bcrypt
from flask_webapp.db_models import User, Doc
from flask_webapp.users.forms import DataCollectionForm, RegisterationForm, LoginForm, UpdateAccountForm,RequestResetForm, ResetPasswordForm
from flask_webapp.users.utils import save_picture, send_reset_email
import pickle
import numpy as np
import pandas as pd
import sqlite3
from flask_login import login_manager
from flask_session import Session
from flask_webapp.thingspeak import read_data_thingspeak

conn = sqlite3.connect('site.db',check_same_thread=False)
c = conn.cursor()


final_features=[]
users=Blueprint('users',__name__) #'users' is the blueprint name
ohe = pickle.load( open('models//onehotencoding_logreg.pkl', "rb" ) )
model = pickle.load(open('models//finalized_logreg_model_2.pkl', 'rb'))
vatamodel=pickle.load(open('models//final_vata_rf_model.pkl', 'rb'))
pittamodel=pickle.load(open('models//final_pitta_rf_model.pkl', 'rb'))
kaphamodel=pickle.load(open('models//final_kapha_rf_model.pkl', 'rb'))

@users.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterationForm() 
    if form.validate_on_submit():
        hashed_pswd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data,email=form.email.data,password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        flash("Account created for successfully!",'success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='Register',form=form)


@users.route('/login',methods=['GET','POST'])
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        doc = Doc.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            session['Account_type']='User'
            next_page = request.args.get('next')
            if(next_page):
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        elif doc and bcrypt.check_password_hash(doc.password, form.password.data):
            login_user(doc,remember=form.remember.data)
            session['Account_type']='Doc'
            # if there is a next keyword in thje url it redirects to that url
            next_page = request.args.get('next')
            if(next_page):
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessful! Please check email and password.",'danger')
    return render_template('login.html',title='Login',form=form)

@users.route("/logout")
def logout():
    logout_user() 
    return redirect(url_for('main.home'))

#how to put certain restrictions on some routes so that you go to them only if you are logged in--->i.e. login before you can view that page
@users.route("/account",methods=['GET','POST'])
@login_required #--you need to login to access this route
def account():
    form = UpdateAccountForm()
    # if our form is valid then we can update our username and email
    if form.validate_on_submit():
        #check if there is any picture data
        if form.picture.data:
            #set the users profile pic
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        #to update:-->when updated the old values will no longer be in the db
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        #flash msg that tells the user that acc has been updtaed
        flash('Your account has been updated!','success')
        return redirect(url_for('users.account'))
    # for the form to display the current username and address when we visit the account
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    #tell where our login route is located?-->init--->login_manager.login_view = 'login'
    #set img file to be passed to the account template
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)




@users.route("/reset_password",methods=['GET','POST'])
#user will have to be logged out to access this
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RequestResetForm()
    # if form was validated and submitted
    if form.validate_on_submit():
        user =User.query.filter_by(email=form.email.data).first()
        #send email to the user with the token to reset pswd-->send_reset_email fn is used
        send_reset_email(user)
        flash('An email has been sent to reset your password','info')#email is sent using flask_mail in __init__.py
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title='Reset Password',form=form)

#route where user actually resets their pswd:
@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    #we have to make sure that its the actual user and the token we gave them in the email is active and we get the token from the url
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    #if invalid token:
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pswd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_pswd 
        db.session.commit()
        flash("Your password has been updated successfully!",'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title='Reset Password',form=form)
    
#add a link to the reset password page to our application
@users.route('/collectdata',methods=['GET','POST'])
def collectdata():
    global final_features
    form = DataCollectionForm()
    features = [x for x in request.form.values()]
    # user_id=features[0]
    final_features.clear()
    for i in range (1,len(features)-1):
        final_features.append(features[i])

    if form.validate_on_submit():     
        # db.session.add(user)
        # db.session.commit()

        return redirect(url_for('users.prediction'))

    
    return render_template('collectdata.html',title='Data Collection',form=form)

@users.route('/prediction',methods=['GET','POST'])
def prediction():
    global final_features
    final_features = [np.array(final_features)]
    final_features_to_use=ohe.transform(final_features)
    # print(final_features_to_use)
    prediction = model.predict(final_features_to_use)
    # print(prediction)
    # vata,pitta,kapha=read_data_thingspeak()

    if(current_user.username=='user1'):
        testdf=pd.read_csv('TestCases//testcase_vata_bp.csv')
    elif(current_user.username=='user2'):
        testdf=pd.read_csv('TestCases//testcase_vata_uh.csv')
    elif(current_user.username=='user3'):
        testdf=pd.read_csv('TestCases//testcase_pitta_h.csv')
    elif(current_user.username=='user4'):
        testdf=pd.read_csv('TestCases//testcase_pitta_uh.csv')
    elif(current_user.username=='user5'):
        testdf=pd.read_csv('TestCases//testcase_kapha_h.csv')
    elif(current_user.username=='user6'):
        testdf=pd.read_csv('TestCases//testcase_kapha_uh.csv')
    elif(current_user.username=='user7'):
        testdf=pd.read_csv('TestCases//testcase_vata_bp.csv')
    else:
        testdf=pd.read_csv('TestCases//testcase_kapha_h.csv')

    testdf=testdf.T
    vata=testdf.iloc[:1,:]
    pitta=testdf.iloc[1:2,:]
    kapha=testdf.iloc[2:3,:]

    if(prediction=='vata'):
        health=vatamodel.predict(vata)
    elif(prediction=='pitta'):
        health=pittamodel.predict(pitta)
    elif(prediction=='kapha'):
        health=kaphamodel.predict(kapha)

    prediction='vata'
    
    # print(health)
    # current_user.dosha=prediction
    # db.session.commit()
    return render_template('prediction.html',title="predict dosha",res=prediction,h=health,user='user7')

@users.route("/prediction2",methods=['GET'])
def prediction2():
    # print(res1,h1,user1)
    res1=request.args.get('res1')
    h1=request.args.get('h1')
    user1=request.args.get('user1')
    return render_template('prediction2.html',title="predict dosha",res=res1,h=h1,user=user1)


@users.route('/patients',methods=['GET','POST'])
def patients():
    # print(current_user.email)
    curr = conn.cursor()
    curr.execute("SELECT * FROM User where doc_assigned=? ",(current_user.username,))
    data = curr.fetchall()
    return render_template('patients.html',title="patient record",data=data)

