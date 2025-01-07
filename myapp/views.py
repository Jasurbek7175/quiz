from django.shortcuts import render
# Create your views here.
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import CreateUserSerializer, CategoryQuizSerializer, CategorySerializer, SubCategorySerializer, \
    QuestionSerializer
from .models import Category, Question
from rest_framework.generics import ListAPIView

User = get_user_model()


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer


from rest_framework.generics import RetrieveAPIView
from .models import Quiz
from .serializers import QuizSerializer


class QuizDetailView(RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizListView(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = SubCategorySerializer


class QuestionListView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class CaregoryQuizView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryQuizSerializer
