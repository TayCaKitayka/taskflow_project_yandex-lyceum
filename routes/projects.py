from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from data import db_session
from data.projects import Project
from forms.project_forms import ProjectForm

projects_blueprint = Blueprint("projects", __name__)


def get_user_project(project_id):
    db_sess = db_session.create_session()
    project = db_sess.get(Project, project_id)

    if not project:
        abort(404)

    if project.user_id != current_user.id:
        abort(403)

    return db_sess, project


@projects_blueprint.route("/projects")
@login_required
def projects():
    db_sess = db_session.create_session()
    user_projects = (
        db_sess.query(Project)
        .filter(Project.user_id == current_user.id)
        .order_by(Project.created_at.desc())
        .all()
    )

    return render_template(
        "projects.html",
        title="Мои проекты",
        projects=user_projects,
    )


@projects_blueprint.route("/projects/create", methods=["GET", "POST"])
@login_required
def create_project():
    form = ProjectForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        project = Project(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id,
        )

        db_sess.add(project)
        db_sess.commit()

        flash("Проект создан.", "success")
        return redirect(url_for("projects.projects"))

    return render_template(
        "project_form.html",
        title="Новый проект",
        form=form,
    )


@projects_blueprint.route("/projects/<int:project_id>")
@login_required
def project_detail(project_id):
    db_sess, project = get_user_project(project_id)

    return render_template(
        "project_detail.html",
        title=project.title,
        project=project,
    )


@projects_blueprint.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    db_sess, project = get_user_project(project_id)
    form = ProjectForm()

    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data

        db_sess.commit()

        flash("Проект обновлён.", "success")
        return redirect(url_for("projects.project_detail", project_id=project.id))

    form.title.data = project.title
    form.description.data = project.description

    return render_template(
        "project_form.html",
        title="Редактирование проекта",
        form=form,
    )


@projects_blueprint.route("/projects/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id):
    db_sess, project = get_user_project(project_id)

    db_sess.delete(project)
    db_sess.commit()

    flash("Проект удалён.", "success")
    return redirect(url_for("projects.projects"))
