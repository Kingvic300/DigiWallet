from decimal import Decimal
from operator import truth

from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError


# Create your models here.

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    account_number = models.CharField(max_length=11, unique=True)



    def deposit(self, amount):
        if amount > Decimal('0.00'):
            self.balance += Decimal(amount)



class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('D','Deposit'),
        ('W','Withdraw'),
        ('T','Transfer'),
    ]
    reference_number = models.CharField(max_length=200 ,unique=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPE, default='D')
    transaction_time = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='sender',null=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='receiver',null=True)


    def save(self, *args, **kwargs):
        if self.sender is None and self.receiver is None:
            raise ValidationError('sender and receiver cannot be none ')
        super().save(*args, **kwargs)