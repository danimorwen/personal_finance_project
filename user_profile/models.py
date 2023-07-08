from datetime import datetime
from django.db import models
from .utils import sum_total


class Category(models.Model):
    class TransactionsType(models.TextChoices):
        expense = "E", "Expense"
        income = "I", "Income"
        all = "ALL", "All"

    name = models.CharField(max_length=50)
    essential = models.BooleanField(default=False)
    type = models.CharField(
        max_length=3, choices=TransactionsType.choices, default=TransactionsType.all
    )
    limit = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def total_spent(self):
        from statement.models import Transactions

        transactions = (
            Transactions.objects.filter(category__id=self.id)
            .filter(date__month=datetime.now().month)
            .filter(type="E")
        )
        return sum_total(transactions, "amount")

    def get_percentage(self):
        try:
            return self.total_spent() / self.limit * 100
        except ZeroDivisionError:
            return 0


class Account(models.Model):
    class Bank(models.TextChoices):
        nubank = "NU", "Nubank"
        hsbc = "HSBC", "HSBC"
        monzo = "MONZO", "Monzo"

    class AccountType(models.TextChoices):
        personal = "PA", "Personal Account"
        business = "BA", "Business Account"

    name = models.CharField(max_length=50)
    bank = models.CharField(max_length=50, choices=Bank.choices)
    type = models.CharField(max_length=2, choices=AccountType.choices)
    amount = models.FloatField(default=0)
    bank_icon = models.ImageField(upload_to="icons")

    def __str__(self):
        return self.name
