from app.core.interfaces.db import DbInterface
from flask_sqlalchemy import SQLAlchemy


class MySqlInterface(DbInterface):
    class __MySqlInterface:
        def __init__(self):
            from app.run_app import application

            self.db = SQLAlchemy(application)

    instance = None

    def __init__(self):
        if not MySqlInterface.instance:
            MySqlInterface.instance = MySqlInterface.__MySqlInterface()
            self.db = MySqlInterface.instance.db
        else:
            self.db = MySqlInterface.instance.db

    def save(self, x_rate):
        self.db.session.add(x_rate)
        self.db.session.commit()

    # TODO: Make optimal with aggregation and filters and order_by
    def get(self, key=None, value=None, n=None):
        no_filters = not any((key, value, n))
        if no_filters:
            results = self.get_all()
            return [results[0]] if results else []
        if key and value:
            pass
        return self.get_all()

    def get_all(self):
        from app.core.models.currency_x_rate import CurrencyXrate

        return self.db.session.query(CurrencyXrate).order_by("-created_at").all()
