from django.db.models import Q
from user_profile.models import Account, Category


class AccountRepository:
    def get_all_accounts(self):
        return Account.objects.all()

    def get_account_by_id(self, id):
        return Account.objects.get(id=id)


class CategoryRepository:
    def get_all_categories(self):
        return Category.objects.all()

    def get_category_by_id(self, id):
        return Category.objects.get(id=id)

    def get_categories_by_expenses(self):
        return Category.objects.filter(Q(type="E") | Q(type="ALL"))

    def get_category_by_name(self, name):
        return Category.objects.filter(name=name)
