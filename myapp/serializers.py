from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Question, Answer, SubCategory
from rest_framework import serializers
from .models import Quiz

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            # telephone=validated_data.get('telephone', '')
        )
        return user


class QuestionRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'figure']


from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category']


class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'sub_category', ]

    def get_category_name(self, obj):
        category_name = Category.objects.filter(category=obj.category).first()
        return {
            "id": category_name.id,
            "category": category_name.category
        } if category_name else None


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'content', 'correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'content', 'answers', 'figure']

    def get_answers(self, obj):
        answers = obj.answer.all()
        return AnswerSerializer(answers, many=True).data


# class QuizSerializer(serializers.ModelSerializer):
#     questions = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Quiz
#         fields = ['id', 'title', 'random_order', 'max_questions', 'exam_paper', 'category_id', 'questions', 'time']
#
#     def get_questions(self, obj):
#         questions = obj.questions.all()
#         max_questions = obj.max_questions
#         if obj.random_order:
#             questions = questions.order_by('?')[:max_questions]
#         elif max_questions:
#             questions = questions[:max_questions]
#         return QuestionSerializer(questions, many=True).data

class QuizSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'random_order', 'max_questions', 'exam_paper', 'category_id', 'sub_category',
                  'questions', 'time']

    def get_questions(self, obj):
        questions = Question.objects.filter(quiz=obj)
        max_questions = obj.max_questions
        if obj.random_order:
            questions = questions.order_by('?')[:max_questions]
        elif max_questions:
            questions = questions[:max_questions]
        return QuestionSerializer(questions, many=True).data

    def get_sub_category(self, obj):
        sub_category = SubCategory.objects.filter(sub_category=obj.sub_category).first()
        return {
            "id": sub_category.id,
            "name": sub_category.sub_category
        } if sub_category else None


class QuizListSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'random_order', 'max_questions', 'exam_paper', 'category_id', 'questions']

    def get_questions(self, obj):
        questions = obj.questions.all()
        return QuestionRelatedSerializer(questions, many=True).data


class CategoryQuizSerializer(serializers.ModelSerializer):
    quizs = QuizListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'category', 'quizs']

    def get_questions(self, obj):
        quizs = obj.quizs.all()
        return QuizListSerializer(quizs, many=True).data
