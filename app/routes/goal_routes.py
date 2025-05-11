from flask import Blueprint, request, make_response, Response
from app.models.goal import Goal
from .. import db
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")