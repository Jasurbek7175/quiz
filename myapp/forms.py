from django import forms
from .models import Question, Answer, Category, Quiz
from django.forms import modelformset_factory


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'correct']

    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter the answer text'}),
        required=True,
        label='Answer'
    )

    correct = forms.BooleanField(
        required=False,
        label='Correct Answer'
    )


from django import forms
from .models import Question, Quiz, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']
        widgets = {
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name',
            }),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz', 'category', 'figure', 'content', 'explanation']

    quiz = forms.ModelMultipleChoiceField(
        queryset=Quiz.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-check-input',
                'style': 'margin-right: 40px; padding-right: 40px;'
            }
        ),
        required=True,
        label='Select Quizzes'
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'style': 'width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #007bff; background-color: #f8f9fa;'
            }
        ),
        required=True,
        label='Choose Category'
    )

    figure = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'style': 'padding: 12px; border-radius: 8px; border: 1px solid #007bff;'
            }
        ),
        label='Upload Figure (optional)'
    )

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Provide an explanation for the answer...',
                'style': 'padding: 12px; border-radius: 8px; border: 1px solid #007bff; background-color: #f8f9fa;'
            }
        ),
        required=True,
        label='Question'
    )

    explanation = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Provide an explanation for the answer...',
                'style': 'padding: 12px; border-radius: 8px; border: 1px solid #007bff; background-color: #f8f9fa;'
            }
        ),
        required=False,
        label='Explanation (optional)'
    )


AnswerFormSet = modelformset_factory(
    Answer,
    form=AnswerForm,
    extra=4,
    can_delete=True
)


from django import forms
from .models import Quiz

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quiz title',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'sub_category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'random_order': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'max_questions': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter maximum number of questions',
            }),
            'exam_paper': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'pass_mark': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter pass mark percentage (0-100)',
            }),
            'time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter time in minutes',
            }),
        }

