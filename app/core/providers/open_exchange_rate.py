import decimal

from dynaconf import settings


class OpenXRateProvider:
    def __init__(self, base="USD"):
        self._base_url = settings.OXR_BASE_URL
        self.__api_key = settings.OXR_API_KEY
        self.base = base

    def get_auth_latest_xrates_request(self):
        # TODO: Validate request
        return (
            f"{self._base_url}/latest.json",
            {"app_id": self.__api_key, "base": self.base},
        )

    def parse_latest_xrates_response(self, response, wanted_currency):
        # TODO: Validate response and check timestamp?
        if self.base == response["base"]:
            return decimal.Decimal(response["rates"][wanted_currency])
