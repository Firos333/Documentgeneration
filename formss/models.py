from django.conf import settings
from django.db import models
from django.utils import timezone
import datetime 

class Monthly(models.Model):
    serial_No = models.IntegerField(unique=True)
    created_date = models.DateField(auto_now=True)
    month = models.CharField(max_length =200,default=0)
    year = models.CharField(max_length =200,default=0)
    income = models.CharField(max_length =200,default=0)
    expenditure = models.CharField(max_length =200,default=0)
    amount = models.IntegerField(default=0)


class Balance(models.Model):
    old_balance = models.IntegerField()
    new_balance = models.IntegerField()
 