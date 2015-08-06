from django import template

from ..forms import get_plan_form


register = template.Library()


@register.inclusion_tag("payments/_change_plan_form.html", takes_context=True)
def change_plan_form(context):
    form_class = get_plan_form(context.get('request'))
    context.update({
        "form": form_class(initial={
            "plan": context["request"].customer.current_subscription.plan
        })
    })
    return context


@register.inclusion_tag("payments/_subscribe_form.html", takes_context=True)
def subscribe_form(context):
    form_class = get_plan_form(context.get('request'))
    context.update({
        "form": form_class()
    })
    return context
