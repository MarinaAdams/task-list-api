import os, requests
from flask import abort, make_response

from ..db import db


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"details": f"{cls.__name__} id {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"details": f"{cls.__name__} id {model_id} not found"}
        abort(make_response(response, 404))

    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)

    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()
    return ({cls.__name__.lower(): new_model.to_dict()}), 201


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    sort_param = None

    if filters:
        filters_dict = dict(filters)  # Convert ImmutableMultiDict to dict
        sort_param = filters_dict.pop("sort", None)

        for attribute, value in filters_dict.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    if sort_param == "asc":
        query = query.order_by(cls.title.asc())
    elif sort_param == "desc":
        query = query.order_by(cls.title.desc())
    else:
        query = query.order_by(cls.id)

    models = db.session.scalars(query)
    return [model.to_dict() for model in models]


def call_slack_api(task):
    slack_url = "https://slack.com/api/chat.postMessage"
    slack_token = os.environ.get("SLACKBOT_TOKEN")

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json",
    }

    data = {
        "channel": "test-slack-api",
        "text": f"Someone just completed the task {task.title}",
    }

    responce = requests.post(slack_url, headers=headers, json=data)
    return responce
