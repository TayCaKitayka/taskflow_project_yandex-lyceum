from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from data import db_session
from data.projects import Project
from data.tasks import Task
from forms.task_forms import TaskForm

tasks_blueprint = Blueprint("tasks", __name__)


def get_user_task(task_id):
    db_sess = db_session.create_session()
    task = db_sess.get(Task, task_id)

    if not task:
        abort(404)

    if task.project.user_id != current_user.id:
        abort(403)

    return db_sess, task


@tasks_blueprint.route("/projects/<int:project_id>/tasks/create", methods=["GET", "POST"])
@login_required
def create_task(project_id):
    db_sess = db_session.create_session()
    project = db_sess.get(Project, project_id)

    if not project:
        abort(404)

    if project.user_id != current_user.id:
        abort(403)

    form = TaskForm()

    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            priority=form.priority.data,
            deadline=form.deadline.data,
            project_id=project.id,
        )

        db_sess.add(task)
        db_sess.commit()

        flash("Задача создана.", "success")
        return redirect(url_for("projects.project_detail", project_id=project.id))

    return render_template(
        "task_form.html",
        title="Новая задача",
        form=form,
        project=project,
    )


@tasks_blueprint.route("/tasks/<int:task_id>")
@login_required
def task_detail(task_id):
    db_sess, task = get_user_task(task_id)

    return render_template(
        "task_detail.html",
        title=task.title,
        task=task,
    )


@tasks_blueprint.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    db_sess, task = get_user_task(task_id)
    form = TaskForm()

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data
        task.priority = form.priority.data
        task.deadline = form.deadline.data

        db_sess.commit()

        flash("Задача обновлена.", "success")
        return redirect(url_for("tasks.task_detail", task_id=task.id))

    form.title.data = task.title
    form.description.data = task.description
    form.status.data = task.status
    form.priority.data = task.priority
    form.deadline.data = task.deadline

    return render_template(
        "task_form.html",
        title="Редактирование задачи",
        form=form,
        project=task.project,
    )


@tasks_blueprint.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    db_sess, task = get_user_task(task_id)
    project_id = task.project_id

    db_sess.delete(task)
    db_sess.commit()

    flash("Задача удалена.", "success")
    return redirect(url_for("projects.project_detail", project_id=project_id))


@tasks_blueprint.route("/tasks/<int:task_id>/done", methods=["POST"])
@login_required
def complete_task(task_id):
    db_sess, task = get_user_task(task_id)

    task.status = "Готово"
    db_sess.commit()

    flash("Задача отмечена как выполненная.", "success")
    return redirect(url_for("projects.project_detail", project_id=task.project_id))
