
from django.contrib import admin
from .models import Category, Account, Transaction


admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Transaction)
