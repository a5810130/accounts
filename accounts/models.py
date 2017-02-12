from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=30)
    create = models.DateTimeField('created')
    def __str__(self):
        return self.name
    def amount(self):
        list_set = self.list_set.all()
        amount = 0
        for list_ in list_set:
            if list_.listType == 'I':
                amount += list_.value
            else:
                amount -= list_.value
        return amount
    

class List(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField('date')
    TYPE_CHOICES = (
        ('I', 'Income'),
        ('E', 'Expenses')
        )
    listType = models.CharField(max_length=1, choices=TYPE_CHOICES) 
    description = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=14, decimal_places=2)
    def __str__(self):
        return self.description