
import pytest
from decimal import Decimal
from core.models import Account, Category
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
            name='psychotropics',
            parent_category=category
        )
        assert Category.objects.count() == 2


@pytest.mark.django_db
class TestAccount:
    def test_account_creation(self, user):
        Account.objects.create(
            owner=user,
            name='piggy bank',
            opening_balance=0.0
        )
        assert Account.objects.count() == 1

    def test_account_current_balance_is_correct(
        self,
        account_with_three_transactions
    ):
        current_balance = account_with_three_transactions.get_current_balance()
        assert current_balance == Decimal(42)

    def test_account_balance_for_future_is_correct(
        self,
        account_with_three_transactions
    ):
        balance_date = date.today() + timedelta(days=10)
        account_balance = account_with_three_transactions.get_account_balance(balance_date)
        assert account_balance == Decimal(-378)
