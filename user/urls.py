from django.urls import path
from . import views
urlpatterns = [
    path('questions-list/', views.question_list, name='question_list'),
    path('questions/create/', views.create_question, name='create_question'),
    path('questions/update/<int:question_id>/', views.update_question, name='update_question'),
    path('questions/delete/<int:question_id>/', views.delete_question, name='delete_question'),
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('questions/delete/<int:question_id>/', views.delete_question, name='delete_question'),
    path('quiz-list/', views.quiz_list, name='quiz_list'),
    path('create/', views.quiz_create, name='quiz_create'),
    path('update/<int:pk>/', views.quiz_update, name='quiz_update'),
    path('delete/<int:pk>/', views.quiz_delete, name='quiz_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
]
