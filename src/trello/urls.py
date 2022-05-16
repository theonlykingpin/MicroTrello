from django.conf import settings
from django.contrib import admin
from django.urls import path, include


api_urlpatterns = [
    path('users/', include(('trello.apps.users.urls', 'trello.apps.users'), namespace='users'))
]


urlpatterns = [
    path('api/', include(api_urlpatterns)),
]


if settings.DEBUG:
    urlpatterns += [path('mgm/', admin.site.urls)]
