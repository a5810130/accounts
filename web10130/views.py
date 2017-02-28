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
    resolver = get_resolver(urls).reverse_dict.keys()
    
    for i in urls.urlpatterns:
        s = i.regex.pattern
        a = re.sub(r'[^\w]', ' ', s)
        if (a.strip()):
            print(a)
        #print(resolver)
    skin = request.GET.get( 'skin', "default")
    return render(request, 'home.html',{'skin':skin,})

