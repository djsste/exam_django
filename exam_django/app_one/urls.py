from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('login', views.login),
    path('quotes', views.success),
    path('logout', views.logout),
    path('upload_quote', views.upload_quote),
    path('user/<int:id>', views.view_user, name='view_user'),
    path('like_quote/<int:id>', views.like_quote, name='like_quote'),
    path('myaccount/<int:id>', views.edit_account_page, name='edit_account_page'),
    path('edit/<int:id>', views.edit_account, name='edit_account'),
    path('delete/<int:id>', views.delete_quote, name='delete_quote')
]