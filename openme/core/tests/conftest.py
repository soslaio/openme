
import pytest
from decimal import Decimal
from core.models import Account, Category
from datetime import date, timedelta
from django.contrib.auth.models import User


@pytest.fixture
def user():
    return User.objects.create_user('xunda')


@pytest.fixture
def super_user():
    return User.objects.create_superuser('superxunda')


@pytest.fixture
def category(user):
    return Category.objects.create(
        owner=user,
        name='drugs'
    )


@pytest.fixture
def account(user):
    return Account.objects.create(
        owner=user,
        name='piggy bank',
        opening_balance=Decimal(882.0)
    )


@pytest.fixture
def account_with_three_transactions(account, category):
    today = date.today()
    yesterday = today + timedelta(days=-1)
    tomorrow = today + timedelta(days=1)
    account.add_transaction(
        transaction_date=yesterday,
        description='cannabis for recreational use',
        ammount=Decimal(-420.0),
        category_id=category.id,
        notes='banzai'
    )
    account.add_transaction(
        transaction_date=today,
        description='cannabis for medical use',
        ammount=Decimal(-420.0),
        category_id=category.id
    )
    account.add_transaction(
        transaction_date=tomorrow,
        description='cannabis for religious use',
        ammount=Decimal(-420.0),
        category_id=category.id
    )
    return account

