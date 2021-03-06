from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.views import login
from django.template.loader import render_to_string
from django.http import HttpResponseNotFound, HttpResponseServerError
from hooky.main.views import setup, hook_callback


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^_hooky-admin/', include(admin.site.urls), name='admin_urls'),

    url(r'^accounts/login/$', login, {'template_name': 'hooky/login.html'}, name='auth_login'),
    url(
        r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'template_name': 'registration/logout.html'},
        name='auth_logout'
    ),
    url(r'^$', setup, name='setup'),
    url(r'^hook/(?P<id>\d+)/(?P<key>\w+)/$', hook_callback, name='hook_callback'),
)

if getattr(settings, 'SERVE_STATIC', False):
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT }
         ),
    )

# These custom error handlers return the correct Http codes for their respective
# errors, as opposed to a 200 as normally returned.
# We can also redirect to templates wherever we like here.
handler404 = '%s.return_404' % (settings.ROOT_URLCONF,)
handler500 = '%s.return_500' % (settings.ROOT_URLCONF,)

def return_404(request):
    return HttpResponseNotFound(render_to_string("hooky/404.html"))

def return_500(request):
    return HttpResponseServerError(render_to_string("hooky/500.html"))
