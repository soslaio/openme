
import functools
import uuid
from decimal import Decimal
from django.db import models
from datetime import date
from .base import Base
from .transaction import Transaction


class Account(Base):
    name = models.CharField(max_length=200)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def create_related_transaction(
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
