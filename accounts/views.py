from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone 
from datetime import datetime

from .models import Account, List


def index(request):
    account_list = Account.objects.order_by('-create')
    context = {'account_list':account_list}
    return render(request, 'accounts/index.html', context)

def detail(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    return render(request, 'accounts/detail.html', {'account':account, })

def add_account(request):
    try:
        account_name = request.POST['account_name']
        if not account_name.strip():
            raise 
    except :
        account_list = Account.objects.order_by('-create')
        context = {'account_list':account_list, 
                   'error_message': "Account name is empty"}
        return render(request, 'accounts/index.html', context)
    else:
        a = Account(name=account_name, create=timezone.now())
        a.save()
        return HttpResponseRedirect(reverse('accounts:index',))
    
def add_list(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    try:
        date_str = request.POST['date']
        description = request.POST['description']
        listType = request.POST['type']
        value = request.POST['value']
        if (not date_str.strip() or not description.strip()
        or not value.strip()):
            raise 
    except :
        return render(request, 'accounts/detail.html', 
                {'account': account, 'message': "Incomplete information.",})
    date = datetime.strptime(date_str,"%m/%d/%Y")
    account.list_set.create(date=date, listType=listType,
                            description=description,
                            value=value)
    account.save()
    return render(request, 'accounts/detail.html', 
                {'account': account,})
        
    
    
    
        
    
    