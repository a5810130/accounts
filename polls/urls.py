from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^add_question/$', views.add_question, name='add_question'),
    url(r'^create_question/$', views.create_question, name='create_question'),
    url(r'^(?P<question_id>[0-9]+)/add_choice/$', views.add_choice, name='add_choice'),
    url(r'^(?P<question_id>[0-9]+)/create_choice/$', views.create_choice, name='create_choice'),
]
