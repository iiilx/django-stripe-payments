from django.core.management.base import BaseCommand

from ...utils import get_user_model
from ...models import Customer


class Command(BaseCommand):

    help = "Sync customer data"

    def handle(self, *args, **options):
        User = get_user_model()
        qs = Customer.objects.all()
        count = 0
        total = qs.count()
        for customer in qs:
            user = customer.user
            count += 1
            perc = int(round(100 * (float(count) / float(total))))
            if hasattr(User, "USERNAME_FIELD"):
                # Using a Django 1.5+ User model
                username = getattr(user, user.USERNAME_FIELD)
            else:
                # Using a pre-Django 1.5 User model
                username = user.username
            print("[{0}/{1} {2}%] Syncing {3} [{4}]".format(
                count, total, perc, username, user.pk
            ))
            cu = customer.stripe_customer
            customer.sync(cu=cu)
            customer.sync_current_subscription(cu=cu)
            customer.sync_invoices(cu=cu)
            customer.sync_charges(cu=cu)
