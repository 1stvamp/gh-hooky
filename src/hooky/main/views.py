from github2.client import Github
from github2.issues import Issues
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils import simplejson
from django.core.mail import send_mail
from hooky.main.models import User, Notification
from hooky.main.forms import UserProfileForm, NotificationFormSet
from hooky.main.parser_utils import parse_message

@login_required
def setup(request):
    if request.method == 'POST':
        if request.POST.get('user', None) != str(request.user.id) \
          and request.POST.get('id', None) != str(request.user.get_profile().id):
            return HttpResponseNotAllowed('Not your user!')
        print request.POST
        form = UserProfileForm(request.POST)

        formset = NotificationFormSet(request.POST, request.FILES, instance=request.user)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('setup')
    else:
        form = UserProfileForm(instance=request.user.get_profile())
        formset = NotificationFormSet(instance=request.user)

    return render_to_response(
        'hooky/setup.html',
        {
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )

@csrf_exempt
def hook_callback(request, id, key):
    user = get_object_or_404(User, pk=id, userprofile__key=key)
    payload = simplejson.loads(request.POST.get('payload'))
    for commit in payload['commits']:
        msg_data = parse_message(commit['message'])
        for issue_num in msg_data['issues']:
            github = Github(
                username=user.get_profile().github_username,
                api_token=user.get_profile().github_key,
                requests_per_second=1
            )
            github.issues.comment(
                "%s/%s" % (payload['repository']['owner']['name'], payload['repository']['name']),
                issue_num,
                "Commit %s by %s - %s" % (commit['id'], commit['author']['name'], commit['message'])
            )
        def email_notification():
            send_mail(
                    'Hooky commit notication for %s/%s' % (payload['repository']['owner']['name'], payload['repository']['name']),
                    '%s committed %s @ %s\n\nMessage:\n%s' % (
                        commit['author']['name'],
                        commit['id'],
                        commit['url'],
                        commit['message'],
                    ),
                    'do-not-reply@hack1.1stvamp.net',
                    [notification.action_to],
                    fail_silently=False
                )
        for username in msg_data['users']:
            notifications = Notification.objects.filter(created_by=user, action_on=username, type='user')
            if notifications:
                for notification in notifications:
                    if notification.action == 'email':
                        email_notification()
        for username in msg_data['hashtags']:
            notifications = Notification.objects.filter(created_by=user, action_on=username, type='hashtag')
            if notifications:
                for notification in notifications:
                    if notification.action == 'email':
                        email_notification()
    return HttpResponse('OK')
