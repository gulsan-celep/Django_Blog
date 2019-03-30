from django.conf.urls import url
from .views import register, user_login, user_logout, user_profile, user_settings, user_about, user_password_change


urlpatterns = [
    url(r'^register/$', view=register, name='register'),
    url(r'^user_login/$', view=user_login, name='user_login'),
    url(r'^logout/$', view=user_logout, name='user_logout'),
    url(r'^user_password_change/$', view=user_password_change, name='user_password_change'),
    url(r'^user_settings/$', view=user_settings, name='user_settings'),
    url(r'^(?P<username>[-\w]+)/about/$', view=user_about, name='user_about'),
    url(r'^(?P<username>[-\w]+)/$', view=user_profile, name='user_profile'),


]