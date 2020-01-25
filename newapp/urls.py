from django.urls import path
from .import views
urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('book',views.show),
    path('addbook',views.addbook),
    path('logout',views.logout),
    path('bookshow/<int:id>',views.showbook),
    path('addfavorite/<int:id>',views.addfavorite),
    path('removefavorite/<int:id>',views.removefavorite),
    path('delete/<int:id>',views.delete),
    path('update/<int:id>',views.update),
]
