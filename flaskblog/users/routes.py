from flaskblog import bcrypt
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flaskblog import db
from flask_login import current_user, login_required, login_user, logout_user

from flaskblog.posts.models import Post
from flaskblog.users.models import User
from flaskblog.users.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(form.username.data, form.email.data, hashed_password)

        db.session.add(user)
        db.session.commit()

        flash(f"Welcome {user.username}! Your account has been created! You are now able to log in", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "warning")

    return render_template("login.html", title="Login", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename=f"profile_pics/{current_user.image_file}")
    return render_template("account.html", title="Account", 
                           image_file=image_file, form=form)
    
@users.route("/user/<string:username>")
def user_posts(username: str):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", title=f"Posts by {username}", posts=posts, user=user)

@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password croski.", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user: User = User.verify_reset_token(token)
    if not user:
        flash("Invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        flash("Password has been updated!", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)

#
# @users.route("/bulk_create", methods=["GET", "POST"])
# def bulk_create_users():
#
#     hashed_pass = bcrypt.generate_password_hash("testing").decode('utf-8')
#     u1 = User("BabyTron", "babytronshtyboyz@gmail.com", hashed_pass)
#     u2 = User("John Doe", "johndoe@gmail.com", hashed_pass)
#     u3 = User("Jane Doe", "janedoe@gmail.com", hashed_pass)
#     u4 = User("Taro Yamada", "yamadataro@gmail.com", hashed_pass)
#
#     db.session.add(u1)
#     db.session.add(u2)
#     db.session.add(u3)
#     db.session.add(u4)
#
#     db.session.commit()
#
#     flash("Test users created", "success")
#     return redirect(url_for("main.home"))
