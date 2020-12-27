
from rest_framework import serializers
from .models.account import Account
from .models.category import Category
from .models.transaction import Transaction
from rest_framework.reverse import reverse


class AccountSerializer(serializers.ModelSerializer):
    current_balance = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = '__all__'

    def get_current_balance(self, obj):
        return obj.get_current_balance()

    def get_url(self, obj):
        request = self.context['request']
        return reverse('accounts-detail', args=[obj.id], request=request)


class TransactionSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    type = serializers.CharField()

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_url(self, obj):
        request = self.context['request']
        return reverse('transactions-detail', args=[obj.id], request=request)


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    is_root = serializers.BooleanField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_url(self, obj):
        request = self.context['request']
        return reverse('categories-detail', args=[obj.id], request=request)
