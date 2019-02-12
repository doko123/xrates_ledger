from mock import patch

from app.core.use_cases.grab_and_save import GrabAndSaveUC


def test_grab_and_save_should_return_200(client, db):
    body = {"currency": "EUR", "amount": 1.23322345345}
    with patch.object(GrabAndSaveUC, "_make_request") as mock_external_request:
        mock_external_request.return_value = None
        response = client.post("/grab_and_save", json=body)

    assert 200 == response.status_code
