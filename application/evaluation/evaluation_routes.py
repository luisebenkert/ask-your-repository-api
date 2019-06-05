"""Provides Evaluation functionality and routes"""
from flask import Blueprint

from .evaluation_view import EvaluationView

EVALUATION = Blueprint("evaluation", __name__)
EVALUATION.add_url_rule("", view_func=EvaluationView.as_view("evaluationview"))