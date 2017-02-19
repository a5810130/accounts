from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=30)
    create = models.DateTimeField('created')
    
    def __str__(self):
        return self.name
    
    def balance(self, start, end):
        transaction = self.transaction_set.order_by('-date','-id')[start-1:end]
        self.balance = self.balance_forward
        for action in transaction:
            if action.actionType == 'I':
                self.balance += action.value
            else:
                self.balance -= action.value
        return self.balance
    
    def balance_forward(self, end):
        transaction = self.transaction_set.order_by('-date','-id')[end:]
        self.balance_forward = 0
        for action in transaction:
            if action.actionType == 'I':
                self.balance_forward += action.value
            else:
                self.balance_forward -= action.value
        return self.balance_forward
    

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField('date')
    TYPE_CHOICES = (
        ('I', 'Income'),
        ('E', 'Expenses')
        )
    actionType = models.CharField(max_length=1, choices=TYPE_CHOICES) 
    description = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=14, decimal_places=2)
    def __str__(self):
        return self.description