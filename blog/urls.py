from django.conf.urls import url
from .views import post_update,post_delete,post_create,posts_list,sanatcilar,post_detail, add_comment, add_or_remove_favorite, post_list_favorite_user, new_add_comment, get_child_comment_form

urlpatterns = [
    url(r'^$', posts_list, name='post_list'),
    url(r'^post_detail/(?P<slug>[-\w]+)/$', post_detail, name='post_detail'),
    url(r'^post_update/(?P<slug>[-\w]+)/$', post_update, name='post_update'),
    url(r'^post_delete/(?P<slug>[-\w]+)/$', post_delete, name='post_delete'),
    url(r'^post_create/$', post_create, name='post_create'),
    url(r'^get_child_comment_form/$', get_child_comment_form, name='get_child_comment_form'),
    url(r'^new_add_comment/(?P<pk>[0-9]+)/(?P<model_type>[\w]+)/$', new_add_comment, name='new_add_comment'),
    url(r'^add_comment/(?P<slug>[-\w]+)/$', add_comment, name='add_comment'),
    url(r'^post-favorite-users/(?P<slug>[-\w]+)/$', post_list_favorite_user, name='post-favorite-users'),
    url(r'^add_remove_favorite/(?P<slug>[-\w]+)/$', add_or_remove_favorite, name='add_remove_favorite'),
    url(r'^sanatcilar/(?P<sayi>[0-9a-z]+)/', sanatcilar)
]