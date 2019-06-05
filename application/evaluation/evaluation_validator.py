"""Defines validators for tags requests"""

from webargs import fields

def evaluation_args():
    """Defines and validates suggested tags params"""
    return {
        "data": fields.List(fields.String(), missing=[]),
    }
