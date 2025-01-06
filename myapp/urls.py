from django.contrib import admin
from django.urls import path
from .views import CategoryListView, QuizDetailView, CreateUserView, QuestionListView, QuizListView, CaregoryQuizView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/list/', QuizListView.as_view(), name='quiz-list'),
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('quiz-category/', CaregoryQuizView.as_view(), name='question-list'),
]
