import datetime

import factory as fc
import factory.fuzzy

from app.core.models.currency_x_rate import CurrencyXrate


class CurrencyXrateFactory(fc.alchemy.SQLAlchemyModelFactory):
    class Meta:

        model = CurrencyXrate

    id = factory.Sequence(lambda i: i + 1)
    currency = "EUR"
    amount = factory.fuzzy.FuzzyDecimal(0.0, 100)
    price = factory.fuzzy.FuzzyDecimal(0.0, 10)
    final_amount = factory.fuzzy.FuzzyDecimal(0.0, 10)
    created_at = factory.LazyAttribute(lambda o: datetime.datetime.now())
