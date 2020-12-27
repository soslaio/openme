
from django.contrib import admin
from .models.account import Account
from .models.category import Category
from .models.transaction import Transaction


admin.site.register(Account)
admin.site.register(Category)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_account', 'description', 'ammount', 'category')
    list_filter = ('from_account', 'category')
