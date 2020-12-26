
from rest_framework import serializers
from .models import Account, Transaction
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
