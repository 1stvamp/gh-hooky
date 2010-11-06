import github2
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils import simplejson

@login_required
def setup(request):
    return render_to_response(
        'hooky/setup.html',
        {
            'form': None,
        },
        context_instance=RequestContext(request)
    )

def hook_callback(request):
    return HttpResponse(simplejson.dumps({}))
