
import pytest
from decimal import Decimal
from core.models.account import Account
from core.models.category import Category
from core.models.transaction import Transaction
from datetime import date, timedelta
from django.contrib.auth.models import User


@pytest.fixture
def user():
    return User.objects.create_user('snoopdogg')


@pytest.fixture
def super_user():
    return User.objects.create_superuser('snoopzilla')


@pytest.fixture
def category(user):
    return Category.objects.create(
        owner=user,
        name='drugs'
    )


@pytest.fixture
def category_with_one_child(category):
    category.create_child_category(
        name='licit'
    )
    return category


@pytest.fixture
def category_with_two_children(category):
    category.create_child_category(
        name='licit'
    )
    category.create_child_category(
        name='illicit'
    )
    return category


@pytest.fixture
def category_with_parent(user, category):
    return Category.objects.create(
        owner=user,
        name='illicit',
        parent_category=category
    )


@pytest.fixture
def account(user):
    return Account.objects.create(
        owner=user,
        name='teapot',
        opening_balance=Decimal(126.0)
    )


@pytest.fixture
def account_with_one_transactions(account, category_with_parent):
    account.create_related_transaction(
        transaction_date=date.today(),
        description='cannabis for recreational use',
        ammount=Decimal(-42.0),
        category_id=category_with_parent.id
    )
    return account


@pytest.fixture
def account_with_three_transactions(account, category):
    today = date.today()
    account.create_related_transaction(
        transaction_date=today + timedelta(days=-1),
        description='cannabis for recreational use',
        ammount=Decimal(-42.0),
        category_id=category.id,
        notes='banzai'
    )
    account.create_related_transaction(
        transaction_date=today,
        description='cannabis for medical use',
        ammount=Decimal(-42.0),
        category_id=category.id
    )
    account.create_related_transaction(
        transaction_date=today + timedelta(days=1),
        description='cannabis for religious use',
        ammount=Decimal(-42.0),
        category_id=category.id
    )
    return account


@pytest.fixture
def debit_transaction(user, account, category):
    return Transaction(
        owner=user,
        from_account=account,
        date=date.today(),
        description='cannabis for everyone',
        ammount=Decimal(-42.0),
        category=category
    )


@pytest.fixture
def credit_transaction(user, account, category):
    return Transaction(
        owner=user,
        from_account=account,
        date=date.today(),
        description='money for drugs',
        ammount=Decimal(42.0),
        category=category
    )


@pytest.fixture
def transfer_transaction(user, account, category):
    to_account = Account(
        owner=user,
        name='wallet',
        opening_balance=Decimal(42.0)
    )
    return Transaction(
        owner=user,
        from_account=account,
        to_account=to_account,
        date=date.today(),
        description='transfer',
        ammount=Decimal(42.0),
        category=category
    )
