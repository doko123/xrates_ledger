import decimal

import pytest

from app.core.schemas.views.grab_and_save import GrabAndSaveRequest


@pytest.mark.parametrize(
    "request_body, expected_kwargs, expected_error",
    [
        (
            {"currency": "EUR", "amount": 1.2334},
            {"currency": "EUR", "amount": decimal.Decimal("1.2334")},
            {},
        ),
        (
            {"currency": "AlaMaKota", "amount": 1.2334},
            {"amount": decimal.Decimal("1.2334")},
            {"currency": ["Currency is invalid according to ISO 4217"]},
        ),
        (
            {"currency": "EUR", "amount": -1.2334},
            {"currency": "EUR"},
            {"amount": ["Value must be greater than 0"]},
        ),
        (
            {"currency": 123, "amount": "233.4"},
            {"amount": decimal.Decimal("233.4")},
            {"currency": ["Not a valid string."]},
        ),
    ],
)
def test_schema_(request_body, expected_kwargs, expected_error):

    kwargs, err = GrabAndSaveRequest().load(request_body)

    assert expected_error == err
    assert expected_kwargs == kwargs
