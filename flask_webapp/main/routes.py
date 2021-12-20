#home and about blueprint
from flask import render_template, request, Blueprint

main=Blueprint('main',__name__) #'users' is the blueprint name

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')#-->to create static html pages

# to write a code in html template we use code blocks like--> 
# {% for post in posts %}
#     {% endfor %}

@main.route('/instructions',methods=['GET','POST'])
def instructions():
    return render_template('instructions.html',title="instructions")

