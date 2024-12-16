from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)
""" 
@errors.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html", error_num=404), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template("errors/403.html", error_num=403), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template("errors/500.html", error_num=500), 500
 """
@errors.app_errorhandler(Exception)
def error_all(error):
    error_num = getattr(error, "code", 500)
    exception_msgs = {
        403: "You do not have the right permissions.",
        404: "The requested resource does not exist.",
        405: "You do not have the right permissions.",
        500: "Internal server error. Please try again later.",
    }
    if error_num in exception_msgs.keys():
        msg = exception_msgs[error_num]
    else:
        msg = "An unexpected error occured."
    return render_template("errors/error_layout.html", error_num=error_num, msg=msg), error_num
