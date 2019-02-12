import copy
import decimal

import pytest

from app.core.interfaces import redis
from app.tests.factories.currency_x_rate import CurrencyXrateFactory

# Set the precision and rounding policy.
custom_decimal_context = decimal.Context(prec=8, rounding=decimal.ROUND_UP)
decimal.setcontext(custom_decimal_context)


@pytest.fixture
def testing_rate():
    return decimal.Decimal("0.884154")


@pytest.fixture(scope="function")
def initial_records(cache, testing_rate):
    records = []
    rec1_amount = decimal.Decimal("1.12345678")
    rec2_amount = decimal.Decimal("2.45678")
    records.append(
        CurrencyXrateFactory.build(
            amount=rec1_amount,
            currency="PLN",
            price=testing_rate,
            final_amount=testing_rate * rec1_amount,
        )
    )
    records.append(
        CurrencyXrateFactory.build(
            amount=rec2_amount,
            currency="EUR",
            price=testing_rate,
            final_amount=testing_rate * rec2_amount,
        )
    )
    assert redis.RedisInterface().get_all() == []
    redis.RedisInterface().save(records[0])
    redis.RedisInterface().save(records[1])
    assert len(redis.RedisInterface().get_all()) == 2
    return list(reversed(records))


@pytest.fixture(scope="function")
def extra_records(initial_records, testing_rate):
    assert len(initial_records) == 2
    extra_recs = copy.deepcopy(initial_records)
    rec3_amount = decimal.Decimal("3.45678")
    rec4_amount = decimal.Decimal("400.456738")
    extra_recs.append(
        CurrencyXrateFactory.build(
            amount=rec3_amount,
            currency="PLN",
            price=testing_rate,
            final_amount=testing_rate * rec3_amount,
        )
    )
    extra_recs.append(
        CurrencyXrateFactory.build(
            amount=rec4_amount,
            currency="EUR",
            price=testing_rate,
            final_amount=testing_rate * rec4_amount,
        )
    )
    assert len(redis.RedisInterface().get_all()) == 2
    redis.RedisInterface().save(extra_recs[2])
    redis.RedisInterface().save(extra_recs[3])
    assert len(extra_recs) == 4
    assert len(redis.RedisInterface().get_all()) == 4
    return extra_recs


def test_get_all(extra_records):
    records = redis.RedisInterface().get_all()
    assert len(set([r[0] for r in records])) == len(records)
    assert len(records) == len(extra_records)


def test_get_returns_last_record(initial_records, cache):
    ordered_fields = redis.RedisInterface().ORDERED_KEYS

    records = redis.RedisInterface().get()

    assert len(records) == 1
    _cmp_record(records[0], initial_records[0], ordered_fields)


@pytest.mark.parametrize(
    "filter_key, filter_value, n, exp_results_qty",
    [(None, None, None, 1), (None, None, 2, 2), ("currency", "EUR", None, 1)],
)
def test_get_returns_last_records_(
    initial_records, filter_key, filter_value, n, exp_results_qty, cache
):
    assert len(redis.RedisInterface().get_all()) == 2
    fields_order = redis.RedisInterface().ORDERED_KEYS
    records = redis.RedisInterface().get(key=filter_key, value=filter_value, n=n)

    assert len(records) == exp_results_qty
    for rec, exp_rec in zip(records, initial_records):
        _cmp_record(rec, exp_rec, fields_order)


def _cmp_record(rec, exp_rec, fields_order):
    assert str(exp_rec.amount) == rec[fields_order.index("amount")]
    assert exp_rec.currency == rec[fields_order.index("currency")]
    assert str(exp_rec.final_amount) == rec[fields_order.index("final_amount")]
    assert str(exp_rec.price) == rec[fields_order.index("price")]
