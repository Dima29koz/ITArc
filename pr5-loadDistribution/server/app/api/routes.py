from flask import jsonify, current_app

from . import api


@api.route('/')
def index():
    """returns json with game_data"""

    return jsonify(
        data=f'index {current_app.name}',
    )


@api.route('/data/<number>')
def get_data(number: int):
    """returns json with game_data"""

    return jsonify(
        data=number,
        app=current_app.name,
    )
