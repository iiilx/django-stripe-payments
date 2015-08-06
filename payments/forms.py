from django import forms
from django.conf import settings

from .settings import PLAN_CHOICES


def get_plan_form(request):
    client_id = settings.STRIPE_CLIENT_ID_FUNCTION(request)

    class PlanForm(forms.Form):
        # pylint: disable=R0924
        plan = forms.ChoiceField(choices=PLAN_CHOICES[client_id] + [("", "-------")])
    return PlanForm
