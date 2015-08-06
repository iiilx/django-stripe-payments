from django.conf import settings
from django.core.urlresolvers import resolve
from django.shortcuts import redirect

from .models import Customer


class CustomerMiddleware(object):

    def process_request(self, request):
        client_id = settings.STRIPE_CLIENT_ID_FUNCTION(request)
        request.client_id = client_id
        if request.user.is_authenticated():
            try:
                customer = Customer.objects.get(user=request.user, client_id=client_id)
            except Customer.DoesNotExist:
                customer = None
            request.customer = customer


class ActiveSubscriptionMiddleware(CustomerMiddleware):

    def process_request(self, request):
        super(ActiveSubscriptionMiddleware, self).process_request(request)
        if request.user.is_authenticated() and not request.user.is_staff:
            url_name = resolve(request.path).url_name
            if url_name not in settings.SUBSCRIPTION_REQUIRED_EXCEPTION_URLS:
                try:
                    if not request.customer or not request.customer.has_active_subscription():
                        return redirect(
                            settings.SUBSCRIPTION_REQUIRED_REDIRECT
                        )
                except Customer.DoesNotExist:
                    return redirect(settings.SUBSCRIPTION_REQUIRED_REDIRECT)
