import six
from django.conf import settings

from .utils import load_path_attr


STRIPE_PUBLIC_KEYS = settings.STRIPE_PUBLIC_KEYS
INVOICE_FROM_EMAILS = settings.PAYMENTS_INVOICE_FROM_EMAILS

DEFAULT_INVOICE_FROM_EMAIL = 'billing@example.com'

PAYMENTS_PLANS = getattr(settings, "PAYMENTS_PLANS", {})

PLAN_CHOICES = {}
for client_id, plans in PAYMENTS_PLANS.iteritems():
    choices = [(plan, PAYMENTS_PLANS[client_id][plan].get("name", plan)) for plan in plans]
    PLAN_CHOICES[client_id] = choices

DEFAULT_PLANS = settings.PAYMENTS_DEFAULT_PLANS

TRIAL_PERIOD_FOR_USER_CALLBACKS = getattr(
    settings,
    "PAYMENTS_TRIAL_PERIOD_FOR_USER_CALLBACKS",
    {}
)
PLAN_QUANTITY_CALLBACKS = getattr(
    settings,
    "PAYMENTS_PLAN_QUANTITY_CALLBACKS",
    {}
)

for client_id in TRIAL_PERIOD_FOR_USER_CALLBACKS:
    callback = TRIAL_PERIOD_FOR_USER_CALLBACKS[client_id]
    if isinstance(callback, six.string_types):
        TRIAL_PERIOD_FOR_USER_CALLBACKS[client_id] = load_path_attr(
            callback
        )

for client_id in PLAN_QUANTITY_CALLBACKS:
    callback = PLAN_QUANTITY_CALLBACKS[client_id]
    if isinstance(callback, six.string_types):
        PLAN_QUANTITY_CALLBACKS[client_id] = load_path_attr(callback)

SEND_EMAIL_RECEIPTS = getattr(settings, "SEND_EMAIL_RECEIPTS", True)


def plan_from_stripe_id(stripe_id):
    for client_id, plans in PAYMENTS_PLANS.iteritems():
        for key in plans:
            if plans[key].get("stripe_plan_id") == stripe_id:
                return key

for client_id in settings.STRIPE_CLIENT_IDS:
    for d in (STRIPE_PUBLIC_KEYS, settings.STRIPE_SECRET_KEYS, INVOICE_FROM_EMAILS,
              PAYMENTS_PLANS, PLAN_CHOICES, DEFAULT_PLANS):
        assert(client_id in d)
