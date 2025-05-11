from flask import Blueprint, request, Response, make_response
from app.models.task import Task
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
import os
import requests

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@bp.get("")
def get_all_tasks():
    sort_param = request.args.get("sort")  

    query = db.select(Task)  

    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())

    tasks = db.session.scalars(query).all()  

    return [task.to_dict() for task in tasks], 200  

@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.today()
    db.session.commit()

    slack_url = "https://slack.com/api/chat.postMessage"
    slack_token = os.environ.get("SLACKBOT_TOKEN")

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    data = {
        "channel": "test-slack-api",
        "text": f"Someone just completed the task {task.title}"
    }

    response = requests.post(slack_url, headers=headers, json=data)  
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
    return ({"task": task.to_dict()})

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json") # 204 No Content

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

