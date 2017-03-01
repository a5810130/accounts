from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone 
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from . import urls
from django.core.urlresolvers import get_resolver, RegexURLPattern
import re

def home(request):
    urlset = []
    for url in urls.urlpatterns:
        temp = url.regex.pattern
        appname = re.sub('[\W]', '', temp)
        if (appname.strip() and appname!="admin"):
            urlset.append(appname)
    skin = request.GET.get( 'skin', "default")
    return render(request, 'home.html',{'urlset':urlset, 'skin':skin})

