from django.contrib import admin

from .models import Invoice, PaidInvoice

admin.site.register(Invoice)
admin.site.register(PaidInvoice)
