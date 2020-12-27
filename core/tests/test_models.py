
import pytest
from decimal import Decimal
from core.models.account import Account
from core.models.category import Category
from datetime import date, timedelta


@pytest.mark.django_db
class TestCategory:
    def test_category_creation_with_no_parent(self, user):
        Category.objects.create(
            owner=user,
            name='drugs'
        )
        assert Category.objects.count() == 1

    def test_category_creation_with_parent(self, user, category):
        Category.objects.create(
            owner=user,
            name='licits',
            parent_category=category
        )
        assert Category.objects.count() == 2


@pytest.mark.django_db
class TestAccount:
    def test_account_creation(self, user):
        Account.objects.create(
            owner=user,
            name='teapot',
            opening_balance=0.0
        )
        assert Account.objects.count() == 1

    def test_account_current_balance_is_correct(
        self,
        account_with_three_transactions
    ):
        current_balance = account_with_three_transactions.get_current_balance()
        assert current_balance == Decimal(42.0)

    def test_account_balance_is_correct(
        self,
        account_with_three_transactions
    ):
        balance_date = date.today() + timedelta(days=10)
        account_balance = account_with_three_transactions.get_account_balance(balance_date)
        assert account_balance == Decimal(0.0)


@pytest.mark.django_db
class TestTransaction:
    def test_transaction_type(
        self,
        debit_transaction,
        credit_transaction,
        transfer_transaction
    ):
        assert debit_transaction.type == 'debit'
        assert credit_transaction.type == 'credit'
        assert transfer_transaction.type == 'transfer'
