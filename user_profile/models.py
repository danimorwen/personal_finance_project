from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    essential = models.BooleanField(default=False)
    limit = models.FloatField(default=0)

    def __str__(self):
        return self.name


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
