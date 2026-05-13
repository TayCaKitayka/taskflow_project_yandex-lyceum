from flask import Flask, render_template
from flask_login import LoginManager
from data import db_session
from data.users import User
from routes.api import api_blueprint
from routes.auth import auth_blueprint
from routes.files import files_blueprint
from routes.projects import projects_blueprint
from routes.tasks import tasks_blueprint

app = Flask(__name__)
app.config["SECRET_KEY"] = "taskflow_secret_key"
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Для доступа к странице выполните вход."
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, int(user_id))


@app.route("/")
def index():
    return render_template("index.html", title="TaskFlow")


def main():
    db_session.global_init("instance/taskflow.sqlite")
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(projects_blueprint)
    app.register_blueprint(tasks_blueprint)
    app.register_blueprint(files_blueprint)
    app.register_blueprint(api_blueprint)
    app.run(host="127.0.0.1", port=8080, debug=True)


if __name__ == "__main__":
    main()
