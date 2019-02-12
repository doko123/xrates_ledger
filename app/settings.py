import decimal
import os

# Set the precision and rounding policy.
custom_decimal_context = decimal.Context(prec=8, rounding=decimal.ROUND_UP)
decimal.setcontext(custom_decimal_context)

DYNACONF_NAMESPACE = "APP"
APP_NAME = "APP"

DB_URI = os.environ.get("DB_URI")
DABATASE_USER_NAME = "root"
DATABASE_PASSWORD = "pass"

LEDGER_URL = os.environ.get("LEDGER_URL", "redis://redis/")

RESPONSE_TIMEOUT = os.environ.get("RESPONSE_TIMEOUT", "@int 10")
ISO_CURR_LIMIT = os.environ.get("ISO_CURR_LIMIT", "@int 3")
OXR_BASE_URL = os.environ.get("OXR_BASE_URL", "")
OXR_API_KEY = os.environ.get("OXR_API_KEY", "")
