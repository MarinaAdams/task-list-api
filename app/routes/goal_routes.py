from flask import Blueprint, request, Response

from app.models.goal import Goal
from app.models.task import Task
from .. import db
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)


@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])
    goal.tasks = []

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)

    db.session.commit()
    return {"id": goal.id, "task_ids": task_ids}


@bp.get("/<goal_id>/tasks")
def get_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks = [task.to_dict() for task in goal.tasks]
    return {"id": goal.id, "title": goal.title, "tasks": tasks}


@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)


@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data. 'title' is required."}, 400

    goal.title = request_body["title"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")
