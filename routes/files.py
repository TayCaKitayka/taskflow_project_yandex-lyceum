from pathlib import Path
from flask import Blueprint, abort, current_app, flash, redirect, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from data import db_session
from data.attachments import Attachment
from data.tasks import Task

files_blueprint = Blueprint("files", __name__)

ALLOWED_EXTENSIONS = {"txt", "csv", "json", "png", "jpg", "jpeg", "pdf", "docx"}


def is_allowed_file(filename):
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


@files_blueprint.route("/tasks/<int:task_id>/upload", methods=["POST"])
@login_required
def upload_file(task_id):
    db_sess = db_session.create_session()
    task = db_sess.get(Task, task_id)

    if not task:
        abort(404)

    if task.project.user_id != current_user.id:
        abort(403)

    uploaded_file = request.files.get("file")

    if not uploaded_file or not uploaded_file.filename:
        flash("Файл не выбран.", "danger")
        return redirect(url_for("tasks.task_detail", task_id=task.id))

    if not is_allowed_file(uploaded_file.filename):
        flash("Недопустимый тип файла.", "danger")
        return redirect(url_for("tasks.task_detail", task_id=task.id))

    safe_name = secure_filename(uploaded_file.filename)
    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)

    file_path = upload_folder / f"task_{task.id}_{safe_name}"
    uploaded_file.save(file_path)

    attachment = Attachment(
        filename=safe_name,
        file_path=str(file_path).replace("\\", "/"),
        task_id=task.id,
    )

    db_sess.add(attachment)
    db_sess.commit()

    flash("Файл загружен.", "success")
    return redirect(url_for("tasks.task_detail", task_id=task.id))
