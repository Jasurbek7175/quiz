from django.shortcuts import render
# Create your views here.
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import CreateUserSerializer, CategoryQuizSerializer, CategorySerializer, SubCategorySerializer, \
    QuestionSerializer
from .models import Category, Question
from rest_framework.generics import ListAPIView
from rest_framework import viewsets

User = get_user_model()

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Question
from .serializers import QuestionSerializer
from .forms import QuizForm


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer


from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView
from .models import Quiz
from .serializers import QuizSerializer


class QuizDetailView(RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionCreate(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.prefetch_related('answer')
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


