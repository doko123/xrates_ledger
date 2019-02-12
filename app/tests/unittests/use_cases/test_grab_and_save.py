import datetime
import decimal

from freezegun import freeze_time
from mock import patch
import pytest

from app.core.use_cases.grab_and_save import GrabAndSaveUC
from app.core.interfaces.my_sql import MySqlInterface


@pytest.fixture
def testing_currency():
    return "EUR"


@pytest.fixture
def testing_rate():
    return decimal.Decimal("0.884154")


@pytest.fixture
def example_correct_oxr_response(testing_currency, testing_rate):
    return {
        "disclaimer": "Usage subject to terms: " "https://openexchangerates.org/terms",
        "license": "https://openexchangerates.org/license",
        "timestamp": 1549893602,
        "base": "USD",
        "rates": {testing_currency: testing_rate},
    }


@freeze_time(datetime.datetime.now())
def test_grab_and_save_should_record_result(
    testing_currency, testing_rate, example_correct_oxr_response, db, cache
):
    requested_amount = decimal.Decimal("1.12345678")
    from app.tests.factories.currency_x_rate import CurrencyXrateFactory

    expected_record = CurrencyXrateFactory.build(
        id=1,
        amount=requested_amount,
        currency=testing_currency,
        price=testing_rate,
        final_amount=testing_rate * requested_amount,
    )

    with patch.object(GrabAndSaveUC, "_make_request") as mock_external_request:
        mock_external_request.return_value = example_correct_oxr_response
        GrabAndSaveUC().grab_and_save(
            amount=requested_amount, currency=testing_currency
        )

    records = MySqlInterface().get_all()
    assert 1 == len(records)
    record = records[0]
    assert expected_record.id == record.id
    assert expected_record.amount == record.amount
    assert expected_record.currency == record.currency
    assert expected_record.final_amount == record.final_amount
    assert expected_record.price == record.price
