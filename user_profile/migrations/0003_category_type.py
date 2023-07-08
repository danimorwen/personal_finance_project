# Generated by Django 4.2.3 on 2023-07-08 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_profile", "0002_account"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="type",
            field=models.CharField(
                choices=[("E", "Expense"), ("I", "Income"), ("ALL", "All")],
                default="ALL",
                max_length=3,
            ),
        ),
    ]
