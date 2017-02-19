from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=30)
    create = models.DateTimeField('created')
    def __str__(self):
        return self.name
    def amount(self):
        transaction_set = self.transaction_set.all()
        amount = 0
        for action in transaction_set:
            if action.actionType == 'I':
                amount += action.value
            else:
                amount -= action.value
        return amount
    

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