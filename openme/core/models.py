
import uuid
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

    def get_account_balance(self, balance_date: date):
        transactions = Transaction.objects.all()
        print(transactions)
        return 69.00

    def get_current_balance(self):
        return self.get_account_balance(date.today())

    def __str__(self):
        return self.name


class Transaction(Base):
    date = models.DateTimeField()
    description = models.CharField(max_length=400)
    ammount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    from_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='from_transactions')
    to_account = models.ForeignKey('Account', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='to_transactions')
    notes = models.TextField()

    @property
    def is_transfer(self):
        return self.from_account and self.to_account

    def __str__(self):
        return self.description
