from django.db import models
from user_profile.models import Category


class Invoice(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    description = models.TextField()
    amount = models.FloatField()
    due_date = models.IntegerField(default=5)
    recurring = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PaidInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.DO_NOTHING)
    payment_date = models.DateField()
