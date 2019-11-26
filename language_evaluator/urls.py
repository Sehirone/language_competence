from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('test/<int:test_id>', views.test, name='test'),
    path('finish/<int:test_id>', views.finish, name='finish')
]
