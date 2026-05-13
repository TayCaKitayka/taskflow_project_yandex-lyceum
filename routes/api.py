from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from data import db_session
from data.projects import Project
from data.tasks import Task

api_blueprint = Blueprint("api", __name__, url_prefix="/api")


def project_to_dict(project):
    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "created_at": project.created_at.isoformat(),
        "tasks_count": len(project.tasks),
    }


@api_blueprint.route("/projects")
@login_required
def get_projects():
    db_sess = db_session.create_session()
    projects = (
        db_sess.query(Project)
        .filter(Project.user_id == current_user.id)
        .order_by(Project.created_at.desc())
        .all()
    )

    return jsonify([project_to_dict(project) for project in projects])


@api_blueprint.route("/projects/<int:project_id>")
@login_required
def get_project(project_id):
    db_sess = db_session.create_session()
    project = db_sess.get(Project, project_id)

    if not project or project.user_id != current_user.id:
        return jsonify({"error": "project not found"}), 404

    project_data = project_to_dict(project)
    project_data["tasks"] = [task.to_dict() for task in project.tasks]

    return jsonify(project_data)


@api_blueprint.route("/tasks")
@login_required
def get_tasks():
    db_sess = db_session.create_session()
    tasks = (
        db_sess.query(Task)
        .join(Project)
        .filter(Project.user_id == current_user.id)
        .order_by(Task.created_at.desc())
        .all()
    )

    return jsonify([task.to_dict() for task in tasks])


@api_blueprint.route("/tasks/<int:task_id>")
@login_required
def get_task(task_id):
    db_sess = db_session.create_session()
    task = db_sess.get(Task, task_id)

    if not task or task.project.user_id != current_user.id:
        return jsonify({"error": "task not found"}), 404

    return jsonify(task.to_dict())


@api_blueprint.route("/tasks", methods=["POST"])
@login_required
def create_task_api():
    request_data = request.get_json()

    if not request_data:
        return jsonify({"error": "empty json"}), 400

    title = request_data.get("title")
    project_id = request_data.get("project_id")

    if not title or not project_id:
        return jsonify({"error": "title and project_id are required"}), 400

    db_sess = db_session.create_session()
    project = db_sess.get(Project, project_id)

    if not project or project.user_id != current_user.id:
        return jsonify({"error": "project not found"}), 404

    task = Task(
        title=title,
        description=request_data.get("description", ""),
        status=request_data.get("status", "Новая"),
        priority=request_data.get("priority", "Средний"),
        project_id=project.id,
    )

    db_sess.add(task)
    db_sess.commit()

    return jsonify(task.to_dict()), 201


@api_blueprint.route("/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task_api(task_id):
    db_sess = db_session.create_session()
    task = db_sess.get(Task, task_id)

    if not task or task.project.user_id != current_user.id:
        return jsonify({"error": "task not found"}), 404

    db_sess.delete(task)
    db_sess.commit()

    return jsonify({"success": True})
