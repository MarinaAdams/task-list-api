from datetime import datetime

from flask import Blueprint, request, Response, make_response

from app.models.task import Task
from .route_utilities import (
    validate_model,
    create_model,
    get_models_with_filters,
    call_slack_api,
)
from ..db import db


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@bp.post("")
def create_task():
    request_body = request.get_json()

    return create_model(Task, request_body)


@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)


@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.today()
    db.session.commit()

    call_slack_api(task)
    return make_response(task.to_dict(), 204)


@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")
