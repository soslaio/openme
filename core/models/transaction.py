
from django.db import models
from .base import Base


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
