from django.conf.urls import url
from .views import kullanici_takip_et_cikar, fallowed_or_fallowers_list, kullanici_modal_takip_et_cikar, kullanici_takip_et_cikar_for_post

urlpatterns = [
    url(r'^takipleşme_sistemi/$',kullanici_takip_et_cikar, name='kullanici_takip_et_cikar'),
    url(r'^post-fav-user-takip-et-cikar/$', kullanici_takip_et_cikar_for_post, name='post-fav-user-takip-et-cikar'),
    url(r'^fallowed_or_fallowers_list/(?P<fallow_type>[-\w]+)/$', view=fallowed_or_fallowers_list, name='fallowed_or_fallowers_list'),
    url(r'^kullanici_modal_takip_et_cikar/$', kullanici_modal_takip_et_cikar, name='kullanici_modal_takip_et_cikar'),

]