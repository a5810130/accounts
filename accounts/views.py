from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Account, List

def index(request):
    account_list = Account.objects.order_by('-create')
    context = {'account_list':account_list}
    return render(request, 'accounts/index.html', context)

def detail(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    return render(request, 'accounts/detail.html', {'account':account, })
        
    
    