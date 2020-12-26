
import pytest
from django.contrib.auth.models import User
from core.models import Account, Category


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
        name='No category'
    )


@pytest.mark.django_db
class TestCategory:
    def test_category_creation_with_no_parent(self, user):
        Category.objects.create(
            owner=user,
            name='Drogas'
        )
        assert Category.objects.count() == 1

    def test_category_creation_with_parent(self, user, category):
        Category.objects.create(
            owner=user,
            name='Drogas',
            parent_category=category
        )
        assert Category.objects.count() == 2


@pytest.mark.django_db
class TestAccount:
    def test_account_creation(self, user):
        Account.objects.create(
            owner=user,
            name='Cofrinho',
            opening_balance=0.0
        )
        assert Account.objects.count() == 1
