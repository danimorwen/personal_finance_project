from datetime import datetime
from statement.models import Transactions


class TransactionsRepository:
    def get_all_transactions(self):
        return Transactions.objects.all()

    def get_transactions_for_current_month(self):
        return Transactions.objects.filter(date__month=datetime.now().month)

    def get_all_expenses(self):
        return Transactions.objects.filter(type="E")

    def get_filtered_income(self, transactions):
        return transactions.filter(type="I")

    def get_filtered_expenses(self, transactions):
        return transactions.filter(type="E")

    def get_filtered_transactions_by_account(self, transactions, account_id):
        return transactions.filter(account__id=account_id)

    def get_current_month_expenses_by_category(self, category_id):
        return (
            Transactions.objects.filter(category__id=category_id)
            .filter(date__month=datetime.now().month)
            .filter(type="E")
        )
