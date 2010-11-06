import github2
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils import simplejson
from hooky.main.models import User
from hooky.main.forms import UserProfileForm

@login_required
def setup(request):
    if request.method == 'POST':
        if request.POST.get('user', None) != str(request.user.id) \
          and request.POST.get('id', None) != str(request.user.get_profile().id):
            return HttpResponseNotAllowed('Not your user!')
        print request.POST
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('setup')
    else:
        form = UserProfileForm(instance=request.user.get_profile())

    return render_to_response(
        'hooky/setup.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )

def hook_callback(request, id):
    if not request.GET.has_key():
        return HttpResponseNotAllowed('Invalid key')
    user = get_object_or_404(User, pk=id, userprofile__key=request.GET.get('key'))
    return HttpResponse(simplejson.dumps({}))
