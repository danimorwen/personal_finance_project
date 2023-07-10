from datetime import datetime
from invoices.models import Invoice, PaidInvoice


class InvoicesRepository:
    def get_all_invoices(self):
        return Invoice.objects.all()

    def get_paid_invoices(self):
        present_month = datetime.now().month
        return PaidInvoice.objects.filter(payment_date__month=present_month).values(
            "invoice"
        )

    def get_past_due_invoices(self, invoices, paid_invoices):
        present_day = datetime.now().day
        return invoices.filter(due_date__lt=present_day).exclude(id__in=paid_invoices)

    def get_due_invoices(self, invoices, paid_invoices):
        present_day = datetime.now().day
        return (
            invoices.filter(due_date__lte=present_day + 5)
            .filter(due_date__gte=present_day)
            .exclude(id__in=paid_invoices)
        )

    def get_future_invoices(
        self, invoices, past_due_invoices, paid_invoices, due_invoices
    ):
        return (
            invoices.exclude(id__in=past_due_invoices)
            .exclude(id__in=paid_invoices)
            .exclude(id__in=due_invoices)
        )

    def get_invoice_by_id(self, id):
        return Invoice.objects.filter(id=id)
