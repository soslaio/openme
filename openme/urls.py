
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core import views


router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet, basename='accounts')
router.register(r'transactions', views.TransactionViewSet, basename='transactions')
router.register(r'categories', views.CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]
