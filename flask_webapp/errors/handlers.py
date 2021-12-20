from flask import Blueprint, render_template

#create an instance of Blueprint
errors=Blueprint('errors',__name__)

#decorators:
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'),404  #404(for coorect error code response) is the status code which by default is 200 


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'),403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'),500