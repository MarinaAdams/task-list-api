from datetime import datetime

from flask import Blueprint, request, Response, make_response
from dotenv import load_dotenv

from app.models.task import Task
from .route_utilities import validate_model, create_model, get_models_with_filters, call_slack_api
from ..db import db

load_dotenv()

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
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query).all()  
    return [task.to_dict() for task in tasks] 


@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.today()
    db.session.commit()

    call_slack_api(task)
    
    # ?? check response
    # if response.status_code != 200:
    #     abort(make_response({"details": "Slack error"}, 500))

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
