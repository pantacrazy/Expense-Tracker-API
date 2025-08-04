from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Expensestypes(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Expenses(models.Model):
    title=models.CharField(max_length=200)
    amount=models.FloatField()
    type=models.ForeignKey(Expensestypes,on_delete=models.CASCADE)
    date=models.DateField()
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title


