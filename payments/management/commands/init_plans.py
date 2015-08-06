import decimal

from django.conf import settings
from django.core.management.base import BaseCommand

import stripe


class Command(BaseCommand):

    help = "Make sure your Stripe account has the plans"

    def handle(self, *args, **options):
        for client_id, plans in settings.PAYMENTS_PLANS.iteritems():
            api_key = settings.STRIPE_SECRET_KEYS[client_id]
            for plan in plans:
                if plans[plan].get("stripe_plan_id"):
                    price = plans[plan]["price"]
                    if isinstance(price, decimal.Decimal):
                        amount = int(100 * price)
                    else:
                        amount = int(100 * decimal.Decimal(str(price)))

                    try:
                        plan_name = plans[plan]["name"]
                        plan_id = plans[plan].get("stripe_plan_id")

                        stripe.Plan.create(
                            amount=amount,
                            interval=plans[plan]["interval"],
                            name=plan_name,
                            currency=plans[plan]["currency"],
                            trial_period_days=plans[plan].get(
                                "trial_period_days"),
                            id=plan_id,
                            api_key=api_key
                        )
                        print("Plan created for {0}".format(plan))
                    except Exception as e:
                        print("{0} ({1}): {2}".format(plan_name, plan_id, e))
