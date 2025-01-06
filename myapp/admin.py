from django.contrib import admin

# Register your models here.
from .models import Question, Quiz, Category, Answer, SubCategory

admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Category)
admin.site.register(Answer)
admin.site.register(SubCategory)
