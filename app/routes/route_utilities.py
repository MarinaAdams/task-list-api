from flask import abort, make_response
from ..db import db

# Helper functions, exist separately, repetitive
def validate_model(cls, model_id): # Defines a reusable function to find a model instance by id
    try:
        model_id = int(model_id)
    except:
        response = {"details": f"{cls.__name__} id {model_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    
    if not model:
        response = {"details": f"{cls.__name__} id {model_id} not found"}
        abort(make_response(response, 404))
    
    return model

def create_model(cls, model_data): # Defines a function to create a new model instance (Task or Goal) using a dictionary
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model) # Adds the new model to the database and saves it
    db.session.commit()

    return ({cls.__name__.lower(): new_model.to_dict()}), 201

def get_models_with_filters(cls, filters=None): # Fetches multiple records of a model (tasks/goals), optionally filtering by query string values
    query = db.select(cls)
    
    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    models = db.session.scalars(query.order_by(cls.id)) # Executes the query and sorts results by id
    models_response = [model.to_dict() for model in models] # Converts all model instances to dictionaries for JSON output

    return models_response