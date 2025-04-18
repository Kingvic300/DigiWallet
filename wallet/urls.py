from wallet import views
from django.urls import path

urlpatterns = [
    path('welcome/', views.welcome, name='index'),
    path('greet/<str:name>',views.greeting,name='greet'),
    path('fund/account', views.fund_wallet, name ='fund_wallet'),
]