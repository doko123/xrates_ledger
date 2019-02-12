from dynaconf import settings
from flask import Flask
from flask_restful import Api


from app.core.interfaces.my_sql import MySqlInterface


def create_app(name=settings.APP_NAME, **kwargs):
    app = Flask(name)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config.update(**kwargs)

    app.app_context().push()

    api = Api(app)
    from app.core.views.grab_and_save import GrabAndSaveResource
    from app.core.views.last import LastResource

    api.add_resource(LastResource, "/last", strict_slashes=False)
    api.add_resource(GrabAndSaveResource, "/grab_and_save", strict_slashes=False)
    return app


def setup_db(app):
    db = MySqlInterface().db
    db.init_app(app)
    from app.core import models  # noqa

    db.create_all()
    db.session.commit()
    return db
