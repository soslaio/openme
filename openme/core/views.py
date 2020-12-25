
from rest_framework import viewsets
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from rest_framework.response import Response


class AccountViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Account.objects.all()
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Transaction.objects.all()
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)
