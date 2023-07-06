from django.db import models
from user_profile.models import Account, Category


class Transactions(models.Model):
    class TransactionType(models.TextChoices):
        income = "I", "Income"
        expense = "E", "Expense"

    amount = models.FloatField()
    categoty = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    description = models.TextField()
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    ttypeipo = models.CharField(max_length=1, choices=TransactionType.choices)

    def __str__(self):
        return self.description
