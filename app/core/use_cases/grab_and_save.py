import requests
import settings
import logging

from app.core.providers.open_exchange_rate import OpenXRateProvider
from app.core.use_cases.amount_price_calculator import AmountPriceCalculator

logger = logging.getLogger(__name__)


class GrabAndSaveUC:
    def grab_and_save(self, amount, currency):
        from app.core.interfaces import my_sql, redis
        from app.core.models.currency_x_rate import CurrencyXrate

        logger.info(f"received amonut {amount} for{currency} currency")
        oxr = OpenXRateProvider()
        url, params = oxr.get_auth_latest_xrates_request()
        x_rates = self._make_request(url, params)

        if x_rates:
            xrate = oxr.parse_latest_xrates_response(x_rates, currency)
            dto = AmountPriceCalculator().Request(amount=amount, price=xrate)
            final_amount = AmountPriceCalculator().calculate_final_amount(dto)
            x_rate = CurrencyXrate(
                currency=currency, amount=amount, final_amount=final_amount, price=xrate
            )
            my_sql.MySqlInterface().save(x_rate)
            redis.RedisInterface().save(x_rate)
            logger.info(
                f"Succesfully grabbed and saved results for {amount} "
                f"{currency} with final cost: {final_amount} USD"
            )

    def _make_request(self, url, params):
        response = requests.get(url, params)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(
                f"Could not get response on GET request on "
                f"{settings.BASE_OXR_URL}, with query params: {params},"
                f" {response.status_code}"
            )
