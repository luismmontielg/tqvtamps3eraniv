from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.views.generic.simple import direct_to_template

from django.template import RequestContext
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site
from django.contrib.auth import login as auth_login

from django import forms as dforms
from django.conf import settings
from django.utils import simplejson

from django.contrib.auth.models import User
from django.contrib.auth import logout

from rsvp.models import Event
from tqv.forms import TQVRSVPForm

def index(request):
    template = "index.html"
    event = get_object_or_404(Event, pk=1)
    form = TQVRSVPForm(initial={"event_id":event.pk})
    context = {
       'activities': event.activity_set.filter(enabled=True),
       'event': event,
       'title': event.title,
       'form': form,
    }
    return render_to_response(template,
        RequestContext(request, context))

def handle_rsvp(request):
    if not request.is_ajax():
        raise Http404
    if not request.POST:
        raise Http404
    form  = TQVRSVPForm(request.POST)
    results = {
        "success": False,
        "message": "Oops, error",
        "reservationForm": form.as_p(),
    }
    if form.is_valid():
        guest = form.save()
        results["message"] = "%s, muchas gracias!" % (guest.name,)
        results["success"] = True
        results["reservationForm"] = form.as_p()
        results["count"] = guest.event.guests_attending().count()
    return HttpResponse(simplejson.dumps(results), mimetype='application/json')
