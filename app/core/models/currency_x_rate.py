from dynaconf import settings

from sqlalchemy import types

from app.core.interfaces.my_sql import MySqlInterface

database = MySqlInterface().db


class CurrencyXrate(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    currency = database.Column(database.String(settings.ISO_CURR_LIMIT))
    amount = database.Column(database.DECIMAL(precision=14, scale=8))
    created_at = database.Column(database.DateTime, server_default=database.func.now())
    price = database.Column(types.DECIMAL(14, 8))
    final_amount = database.Column(
        types.DECIMAL(14, 8)
    )  # TODO: Rethink if its better to have field or property?
