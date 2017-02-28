from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_account/$', views.add_account, name='add_account'),
    url(r'^(?P<account_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<account_id>[0-9]+)/add_list/$', views.add_list, name='add_list'),
    url(r'^(?P<account_id>[0-9]+)/download_csv/$', views.download_csv, name='download_csv'),
    url(r'^(?P<account_id>[0-9]+)/upload_csv/$', views.upload_csv, name='upload_csv'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
