from marshmallow import fields, validate, Schema


class GrabAndSaveRequest(Schema):
    currency = fields.String(
        validate=validate.Regexp(
            "^[A-Z]{3}", 0, "Currency is invalid according to ISO 4217"
        )
    )
    amount = fields.Decimal(
        validate=validate.Range(min=1, error="Value must be greater than 0")
    )
