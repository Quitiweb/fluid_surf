from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='stripe'),
    path('charge', views.charge, name='charge'),
    path('charge-account', views.charge_account, name='charge-account'),
    path('charge-iban', views.charge_iban, name='charge-iban'),
    path('transfer', views.transfer, name='transfer'),
    path('callback', views.CallBack.as_view(), name='callback'),
    path('authorize', views.Authorize.as_view(), name='authorize'),
]
