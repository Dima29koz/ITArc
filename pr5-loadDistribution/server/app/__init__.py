from flask import Flask


def create_app(config, name) -> Flask:
    """
    Creates app and register Blueprints

    :returns: app
    :rtype: Flask
    """
    app = Flask(name)
    app.config.from_object(config)

    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint)

    return app
