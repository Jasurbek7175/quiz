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

    def create(self, validated_data):
        answers_data = validated_data.get('answers', [])
        category = validated_data.get('category')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        # for category in category:
        #     Answer(question=question, **category)
        return question

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers')
        instance.quiz.set(validated_data.get('quiz', instance.quiz.all()))
        instance.category = validated_data.get('category', instance.category)
        instance.figure = validated_data.get('figure', instance.figure)
        instance.content = validated_data.get('content', instance.content)
        instance.explanation = validated_data.get('explanation', instance.explanation)
        instance.save()

        # Update answers
        instance.answer.all().delete()  # Clear existing answers
        for answer_data in answers_data:
            Answer.objects.create(question=instance, **answer_data)

        return instance


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
