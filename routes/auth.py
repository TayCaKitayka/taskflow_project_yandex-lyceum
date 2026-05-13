from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from data import db_session
from data.users import User
from forms.user_forms import LoginForm, RegisterForm

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("projects.projects"))

    form = RegisterForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        existing_user = db_sess.query(User).filter(User.email == form.email.data).first()

        if existing_user:
            flash("Пользователь с таким email уже существует.", "danger")
            return render_template("register.html", title="Регистрация", form=form)

        user = User(
            name=form.name.data,
            email=form.email.data.lower(),
        )
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()

        flash("Регистрация выполнена. Теперь войдите в аккаунт.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", title="Регистрация", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("projects.projects"))

    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data.lower()).first()

        if not user or not user.check_password(form.password.data):
            flash("Неверный email или пароль.", "danger")
            return render_template("login.html", title="Вход", form=form)

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("projects.projects"))

    return render_template("login.html", title="Вход", form=form)


@auth_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
