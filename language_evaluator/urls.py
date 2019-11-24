from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('test/<int:test_id>', views.test, name='test'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('question/<int:question_id>/answer', views.answer, name='answer'),
    path('question/<int:question_id>/answer_result?<int:answer_id>', views.answer_result, name='answer_result'),
    path('finish/<int:test_id>', views.finish, name='finish')
]
