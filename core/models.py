
import functools
import uuid
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from datetime import date


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Base):
    name = models.CharField(max_length=200)
    parent_category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Account(Base):
    name = models.CharField(max_length=200)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def add_transaction(
        self,
        transaction_date: date,
        description: str,
        ammount: Decimal,
        category_id: uuid,
        notes: str = None
    ):
        return Transaction.objects.create(
            owner_id=self.owner_id,
            date=transaction_date,
            description=description,
            ammount=ammount,
            category_id=category_id,
            from_account_id=self.id,
            notes=notes
        )

    def get_account_balance(self, balance_date: date):
        transactions = Transaction.objects.filter(
            from_account_id=self.id,
            date__lte=str(balance_date)
        )
        account_balance = functools.reduce(
            lambda x, y: x + y.ammount,
            transactions,
            self.opening_balance
        )
        return account_balance

    def get_current_balance(self):
        return self.get_account_balance(date.today())

    def __str__(self):
        return self.name


class Transaction(Base):
    date = models.DateField()
    description = models.CharField(max_length=400)
    ammount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    from_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='from_transactions')
    to_account = models.ForeignKey('Account', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='to_transactions')
    notes = models.TextField(null=True, blank=True)

    @property
    def is_transfer(self):
        return self.from_account and self.to_account

    @property
    def type(self):
        if self.is_transfer:
            return 'transfer'
        return 'credit' if self.ammount > 0 else 'debit'

    def __str__(self):
        return self.description
