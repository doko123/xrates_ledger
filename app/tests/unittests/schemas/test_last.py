import pytest

from app.core.schemas.views.last import LastRequest


@pytest.mark.parametrize(
    "request_body, expected_kwargs, expected_error",
    [
        ({}, {}, {}),
        ({"n": 2}, {"n": 2}, {}),
        ({"currency": "EUR"}, {"currency": "EUR"}, {}),
        ({"currency": "EUR", "n": 2}, {"currency": "EUR", "n": 2}, {}),
        (
            {"currency": "AlaMaKota"},
            {},
            {"currency": ["Currency is invalid according to ISO 4217"]},
        ),
        ({"n": "1.6"}, {}, {"n": ["Not a valid integer."]}),
        ({"currency": 123}, {}, {"currency": ["Not a valid string."]}),
    ],
)
def test_schema_should_fail(request_body, expected_kwargs, expected_error):

    kwargs, err = LastRequest().load(request_body)

    assert expected_error == err
    assert expected_kwargs == kwargs
