from django import forms
import django_magnificent_messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import engines
from django.template.response import TemplateResponse
from django.urls import path, re_path, reverse
from django.views.decorators.cache import never_cache
from django.views.generic.edit import FormView

NOTIFICATIONS_TEMPLATE = """{% if messages %}
<ul class="messages">
    {% for text in notifications.all %}
    <li{% if text.level_tag %} class="{{ text.level_tag }}"{% endif %}>
        {{ text.text }}
    </li>
    {% endfor %}
</ul>
{% endif %}
"""


@never_cache
def notifications_add(request, message_type):
    # Don't default to False here to test that it defaults to False if
    # unspecified.
    fail_silently = request.POST.get('fail_silently', None)
    for msg in request.POST.getlist('notifications'):
        if fail_silently is not None:
            getattr(django_magnificent_messages.notifications, message_type)(request, msg, fail_silently=fail_silently)
        else:
            getattr(django_magnificent_messages.notifications, message_type)(request, msg)
    return HttpResponseRedirect(reverse('show_notification'))


@never_cache
def notifications_add_template_response(request, message_type):
    for msg in request.POST.getlist('messages'):
        getattr(django_magnificent_messages.notifications, message_type)(request, msg)
    return HttpResponseRedirect(reverse('show_template_response_notification'))


@never_cache
def notifications_show(request):
    template = engines['django'].from_string(NOTIFICATIONS_TEMPLATE)
    return HttpResponse(template.render(request=request))


@never_cache
def show_template_response_notification(request):
    template = engines['django'].from_string(NOTIFICATIONS_TEMPLATE)
    return TemplateResponse(request, template)


urlpatterns = [
    re_path('^notifications_add/(secondary|primary|info|success|warning|error)/$', notifications_add,
            name='add-notification'),
    path('notifications_show/', notifications_show, name='show_notification'),
    re_path(
        '^template_response/notifications_add/(secondary|primary|info|success|warning|error)/$',
        notifications_add_template_response, name='notifications_add_template_response',
    ),
    path('template_response/notifications_show/', show_template_response_notification,
         name='show_template_response_notification'),
]
