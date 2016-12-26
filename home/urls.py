from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView
from github_oauth.settings import STATIC_URL

import home.views as home

urlpatterns = [
    url(r'^$', home.home, name='home'),
    url(r'^favicon\.ico$', RedirectView.as_view(
        url=STATIC_URL + 'favicon.ico'
    )),
    url(r'^callback/', home.callback, name='callback'),
    url(r'^admin/', admin.site.urls, name="django_admin"),
]
