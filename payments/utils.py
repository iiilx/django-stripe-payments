import datetime
import decimal

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import importlib, timezone
from django.db.models.loading import get_model


def convert_tstamp(response, field_name=None):
    try:
        if field_name and response[field_name]:
            return datetime.datetime.fromtimestamp(
                response[field_name],
                timezone.utc
            )
        if not field_name:
            return datetime.datetime.fromtimestamp(
                response,
                timezone.utc
            )
    except KeyError:
        pass
    return None


def get_user_model():  # pragma: no cover
    return get_model(*settings.STRIPE_USER_MODEL.split('.'))


def load_path_attr(path):  # pragma: no cover
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1:]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured("Error importing {0}: '{1}'".format(module, e))
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(
            "Module '{0}' does not define a '{1}'".format(
                module,
                attr
            )
        )
    return attr


# currencies those amount=1 means 100 cents
# https://support.stripe.com/questions/which-zero-decimal-currencies-does-stripe-support
ZERO_DECIMAL_CURRENCIES = [
    "bif", "clp", "djf", "gnf", "jpy", "kmf", "krw",
    "mga", "pyg", "rwf", "vuv", "xaf", "xof", "xpf",
]


def convert_amount_for_db(amount, currency="usd"):
    return (amount / decimal.Decimal("100")) if currency.lower() not in ZERO_DECIMAL_CURRENCIES else decimal.Decimal(amount)


def convert_amount_for_api(amount, currency="usd"):
    return int(amount * 100) if currency.lower() not in ZERO_DECIMAL_CURRENCIES else int(amount)
