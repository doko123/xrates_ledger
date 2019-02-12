import decimal

import attr

# Set the precision and rounding policy.
custom_decimal_context = decimal.Context(prec=8, rounding=decimal.ROUND_UP)
decimal.setcontext(custom_decimal_context)


class AmountPriceCalculator:
    @attr.s
    class Request:
        amount: decimal.Decimal = attr.ib()
        price: decimal.Decimal = attr.ib()

    def calculate_final_amount(self, request):
        return request.amount * request.price
