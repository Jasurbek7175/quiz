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

    exam_paper = models.BooleanField(
        blank=False, default=False,
        help_text=("If yes, the result of each attempt by a user will be stored. Necessary for marking."),
        verbose_name=("Exam Paper")
    )

    pass_mark = models.SmallIntegerField(
        blank=True, default=0,
        verbose_name=("Pass Mark"),
        help_text=("Percentage required to pass exam."),
        validators=[MaxValueValidator(100)]
    )

    time = models.IntegerField(null=True, verbose_name=("Time"), help_text=("Time for quiz"))

    # def save(self, force_insert=False, force_update=False, *args, **kwargs):
    #     self.url = re.sub('\s+', '-', self.url).lower()
    #
    #     self.url = ''.join(letter for letter in self.url if letter.isalnum() or letter == '-')
    #
    #     if self.single_attempt is True:
    #         self.exam_paper = True
    #
    #     if self.pass_mark > 100:
    #         raise ValidationError('%s is above 100' % self.pass_mark)
    #
    #     super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        verbose_name = ("Викторина")
        verbose_name_plural = ("Викторины")

    def __str__(self):
        return self.title

    # def get_questions(self):
    #     return self.question_set.all().select_subclasses()


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
