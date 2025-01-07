from django.db import models
# Create your models here.
import re
from django.db import models
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import MaxValueValidator, validate_comma_separated_integer_list
from django.utils.timezone import now
from django.conf import settings
# from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, validate_comma_separated_integer_list
from django.conf import settings
from model_utils.managers import InheritanceManager
import re


class CustomUser(AbstractUser):
    telephone = models.CharField(max_length=15, blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


class CategoryManager(models.Manager):
    def new_category(self, category):
        new_category = self.create(category=re.sub('\s+', '-', category).lower())
        new_category.save()
        return new_category


class Category(models.Model):
    category = models.CharField(
        verbose_name=("Category"),
        max_length=250, blank=True,
        unique=True, null=True
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = ("Категория")
        verbose_name_plural = ("Категории")

    def __str__(self):
        return self.category


class SubCategory(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    sub_category = models.CharField(verbose_name=("SubCategory"),
                                    max_length=250, blank=True,
                                    unique=True, null=True)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
    def __str__(self):
        return self.sub_category


class Quiz(models.Model):
    title = models.CharField(
        verbose_name=("Title"),
        max_length=60, blank=False
    )
    description = models.TextField(
        verbose_name=("Description"),
        blank=True, help_text=("a description of the quiz")
    )

    url = models.SlugField(
        max_length=60, blank=False,
        help_text=("a user friendly url"),
        verbose_name=("user friendly url")
    )

    category = models.ForeignKey(
        Category, related_name='quizs', null=True, blank=True,
        verbose_name=("Category"), on_delete=models.CASCADE
    )

    sub_category = models.ForeignKey(
        SubCategory, related_name='quizs', null=True, blank=True,
        verbose_name=("SubCategory"), on_delete=models.CASCADE
    )

    random_order = models.BooleanField(
        blank=False, default=False,
        verbose_name=("Random Order"),
        help_text=("Display the questions in a random order or as they are set?")
    )

    max_questions = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=("Max Questions"),
        help_text=("Number of questions to be answered on each attempt.")
    )

    answers_at_end = models.BooleanField(
        blank=False, default=False,
        help_text=("Correct answer is NOT shown after question. Answers displayed at the end."),
        verbose_name=("Answers at end")
    )
    exam_paper = models.BooleanField(
        blank=False, default=False,
        help_text=("If yes, the result of each attempt by a user will be stored. Necessary for marking."),
        verbose_name=("Exam Paper")
    )

    single_attempt = models.BooleanField(
        blank=False, default=False,
        help_text=("If yes, only one attempt by a user will be permitted. Non users cannot sit this exam."),
        verbose_name=("Single Attempt")
    )
    pass_mark = models.SmallIntegerField(
        blank=True, default=0,
        verbose_name=("Pass Mark"),
        help_text=("Percentage required to pass exam."),
        validators=[MaxValueValidator(100)]
    )

    success_text = models.TextField(
        blank=True, help_text=("Displayed if user passes."),
        verbose_name=("Success Text")
    )

    fail_text = models.TextField(
        verbose_name=("Fail Text"),
        blank=True, help_text=("Displayed if user fails.")
    )

    draft = models.BooleanField(
        blank=True, default=False,
        verbose_name=("Draft"),
        help_text=(
            "If yes, the quiz is not displayed in the quiz list and can only be taken by users who can edit quizzes.")
    )

    time = models.IntegerField(null=True, verbose_name=("Time"), help_text=("Time for quiz"))

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.url = re.sub('\s+', '-', self.url).lower()

        self.url = ''.join(letter for letter in self.url if letter.isalnum() or letter == '-')

        if self.single_attempt is True:
            self.exam_paper = True

        if self.pass_mark > 100:
            raise ValidationError('%s is above 100' % self.pass_mark)

        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        verbose_name = ("Викторина")
        verbose_name_plural = ("Викторины")

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.question_set.all().select_subclasses()

    @property
    def get_max_score(self):
        return self.get_questions().count()

    def anon_score_id(self):
        return str(self.id) + "_score"

    def anon_q_list(self):
        return str(self.id) + "_q_list"

    def anon_q_data(self):
        return str(self.id) + "_data"


class ProgressManager(models.Manager):

    def new_progress(self, user):
        new_progress = self.create(user=user, score="")
        new_progress.save()
        return new_progress


class Progress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=("User"), on_delete=models.CASCADE)

    score = models.CharField(validators=[validate_comma_separated_integer_list], max_length=1024,
                             verbose_name=("Score"))

    correct_answer = models.CharField(max_length=10, verbose_name=('Correct Answers'))

    wrong_answer = models.CharField(max_length=10, verbose_name=('Wrong Answers'))

    objects = ProgressManager()

    class Meta:
        verbose_name = ("User Progress")
        verbose_name_plural = ("User progress records")


class SittingManager(models.Manager):

    def new_sitting(self, user, quiz):
        if quiz.random_order is True:
            question_set = quiz.question_set.all().select_subclasses().order_by('?')
        else:
            question_set = quiz.question_set.all().select_subclasses()

        question_set = [item.id for item in question_set]

        if len(question_set) == 0:
            raise ImproperlyConfigured('Question set of the quiz is empty. Please configure questions properly')

        if quiz.max_questions and quiz.max_questions < len(question_set):
            question_set = question_set[:quiz.max_questions]

        questions = ",".join(map(str, question_set)) + ","

        new_sitting = self.create(user=user, quiz=quiz, question_order=questions, question_list=questions,
                                  incorrect_questions="", current_score=0, complete=False, user_answers='{}')
        return new_sitting


class Sitting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=("User"), on_delete=models.CASCADE)

    quiz = models.ForeignKey(Quiz, verbose_name=("Quiz"), on_delete=models.CASCADE)

    question_order = models.CharField(validators=[validate_comma_separated_integer_list], max_length=1024,
                                      verbose_name=("Question Order"))

    question_list = models.CharField(validators=[validate_comma_separated_integer_list], max_length=1024,
                                     verbose_name=("Question List"))

    incorrect_questions = models.CharField(validators=[validate_comma_separated_integer_list], max_length=1024,
                                           blank=True, verbose_name=("Incorrect questions"))

    current_score = models.IntegerField(verbose_name=("Current Score"))

    complete = models.BooleanField(default=False, blank=False, verbose_name=("Complete"))

    user_answers = models.TextField(blank=True, default='{}', verbose_name=("User Answers"))

    start = models.DateTimeField(auto_now_add=True, verbose_name=("Start"))

    end = models.DateTimeField(null=True, blank=True, verbose_name=("End"))

    objects = SittingManager()


class Question(models.Model):
    quiz = models.ManyToManyField(Quiz, verbose_name="Quiz", blank=True)

    category = models.ForeignKey(Category, verbose_name=("Category"), blank=True, null=True, on_delete=models.CASCADE)

    figure = models.ImageField(upload_to='media/%Y/%m/%d', blank=True, null=True, verbose_name=("Figure"))

    content = models.CharField(max_length=1000, blank=False,
                               help_text=
                               ("Enter the question text that you want displayed"),
                               verbose_name=('Question'))

    explanation = models.TextField(max_length=2000, blank=True,
                                   help_text=("Explanation to be shown after the question has been answered."),
                                   verbose_name=('Explanation'))

    objects = InheritanceManager()

    class Meta:
        verbose_name = ("Вопрос")
        verbose_name_plural = ("Вопросы")
        ordering = ['category']

    def __str__(self):
        return self.content


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answer', verbose_name='Question', on_delete=models.CASCADE)

    content = models.CharField(max_length=1000, blank=False, help_text="Enter the answer text that you want displayed",
                               verbose_name="Content")

    correct = models.BooleanField(blank=False, default=False, help_text="Is this a correct answer?",
                                  verbose_name="Correct")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
