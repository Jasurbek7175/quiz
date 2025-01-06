from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import CreateUserSerializer, CategoryQuizSerializer

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


from rest_framework.generics import ListAPIView
from .models import Category
from .serializers import CategorySerializer


class QuizListView(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


from rest_framework.generics import ListAPIView
from .models import Question
from .serializers import QuestionSerializer


class QuestionListView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class CaregoryQuizView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryQuizSerializer