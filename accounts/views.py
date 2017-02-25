from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone 
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
import csv
import mimetypes
import os
from wsgiref.util import FileWrapper

from .models import Account, Transaction


def index(request):
    account_list = Account.objects.order_by('-create')
    skin = request.GET.get( 'skin', "default")
    context = {'account_list':account_list, 'skin':skin}
    return render(request, 'accounts/index.html', context)

def detail(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    skin = request.GET.get( 'skin', "default")
    transaction = account.transaction_set.order_by('-date','-id')
    paginator = Paginator(transaction, 5)
    page = request.GET.get('page')
    try: 
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    balance_forward = 0
    balance = 0
    try:
        balance_forward = account.balance_forward(contacts.end_index())
        balance = account.balance(contacts.start_index(), contacts.end_index())
    except: 
        pass
    return render(request, 'accounts/detail.html', {'account':account, 'contacts':contacts, 'balance_forward':balance_forward, 'balance':balance,'skin':skin})

def add_account(request):
    skin = request.GET.get( 'skin', "default")
    try:
        account_name = request.POST['account_name']
        if not account_name.strip():
            raise 
    except :
        messages.error(request, 'Account Name is empty.')
        return HttpResponseRedirect(reverse('accounts:index',)+"?skin="+skin)
    else:
        a = Account(name=account_name, create=timezone.now())
        a.save()
        return HttpResponseRedirect(reverse('accounts:index',)+"?skin="+skin)
    
def add_list(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    skin = request.GET.get( 'skin', "default")
    try:
        date_str = request.POST['date']
        description = request.POST['description']
        actionType = request.POST['type']
        value = request.POST['value']
        if (not date_str.strip() or not description.strip()
        or not value.strip()):
            raise 
    except :
        messages.error(request, 'incomplete form.')
        return HttpResponseRedirect(reverse('accounts:detail', args=(account_id))+"?skin="+skin)
    date = datetime.strptime(date_str,"%m/%d/%Y")
    account.transaction_set.create( date=date, actionType=actionType,
                            description=description,
                            value=value)
    account.save()
    return HttpResponseRedirect(reverse('accounts:detail', args=(account_id))+"?skin="+skin)
    
def download_css (request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    transaction = account.transaction_set.order_by('-date','-id')
    filepath="accounts/download/temp.csv"
    with open(filepath, "w+") as csvfile:
        fieldnames = ["date", "description", "type", "money"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for action in transaction:
            writer.writerow({'date':action.date,'description':action.description, 'type':action.actionType, 'money':action.value})
    download_name = account.name+".csv"
    wrapper      = FileWrapper(open(filepath))
    content_type = mimetypes.guess_type(filepath)[0]
    response     = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filepath)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
    
    
        
    
    