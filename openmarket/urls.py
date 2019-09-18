from django.urls import path
from openmarket import views


urlpatterns = [
    path('',views.market_page,name='market_page'),
    path('auction/',views.auction, name='auction'),
    path('market_11/',views.market_11,name='market_11'),
]
