from github2.client import Github
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils import simplejson
from hooky.main.models import User
from hooky.main.forms import UserProfileForm
from hooky.main.parser_utils import parse_message

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
    payload = simplejson.loads(request.POST.get('payload'))
    for commit in payload['commits']:
        msg_data = parse_message(commit['message'])
        for issue_num in msg_data['issues']:
            github = Github(
                username=user.get_profile().github_username,
                api_token=user.get_profile().github_key,
                requests_per_second=1
            )
            issue = github.issues.show("%s/%s" % (payload['repository']['owner']['name'], payload['repository']['name']), issue_num)
            issue.comment("Commit [%s](%s) - %s" % (commit['id'], commit['url'], commit['message']))
    return HttpResponse('OK')
