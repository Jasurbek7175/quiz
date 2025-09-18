from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from myapp.models import Question, Answer, Quiz, Category
from myapp.forms import QuestionForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from myapp.forms import QuizForm, CategoryForm


# Create your views here.
def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES)
        answer_contents = request.POST.getlist('content[]')
        correct_answers = request.POST.getlist('correct[]')

        if question_form.is_valid():
            with transaction.atomic():
                question = question_form.save()
                for index, content in enumerate(answer_contents):
                    is_correct = str(index) in correct_answers
                    Answer.objects.create(question=question, content=content, correct=is_correct)

            messages.success(request, 'The question and answers have been created successfully.')
            return redirect('question_list')
        else:
            messages.error(request, 'There was an error with your input. Please check the form and try again.')
    else:
        question_form = QuestionForm()

    return render(request, 'create.html', {
        'question_form': question_form,
        'title': 'Create Question'
    })


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, 'You have successfully logged in')
                return redirect('question_list')
        else:
            messages.warning(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('login')


@login_required(login_url='login')
def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    existing_answers = list(Answer.objects.filter(question=question))

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES, instance=question)
        answer_contents = request.POST.getlist('content[]')
        correct_answers = request.POST.getlist('correct[]')

        if question_form.is_valid():
            try:
                with transaction.atomic():
                    question = question_form.save()
                    for index, content in enumerate(answer_contents):
                        is_correct = str(existing_answers[index].id) in correct_answers if index < len(
                            existing_answers) else False
                        if index < len(existing_answers):
                            answer = existing_answers[index]
                            answer.content = content
                            answer.correct = is_correct
                            answer.save()
                        else:
                            Answer.objects.create(question=question, content=content, correct=is_correct)
                    if len(answer_contents) < len(existing_answers):
                        for answer in existing_answers[len(answer_contents):]:
                            answer.delete()

                messages.success(request, 'The question and answers have been updated successfully.')
                return redirect('question_list')
            except Exception as e:
                messages.error(request, 'An error occurred while updating the question.')
                print("Error:", e)
        else:
            messages.error(request, 'There was an error with your input. Please check the form and try again.')
            print("Question Form Errors:", question_form.errors)
    else:
        question_form = QuestionForm(instance=question)

    return render(request, 'update.html', {
        'question_form': question_form,
        'title': 'Update Question',
        'existing_answers': existing_answers
    })


@login_required(login_url='login')
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        question.delete()
        messages.success(request, 'The question has been deleted successfully.')
        return redirect('question_list')

    return render(request, 'delete_question_confirmation.html', {
        'question': question
    })


@login_required(login_url='login')
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'question_list.html', {'questions': questions})


# List all quizzes
@login_required(login_url='login')
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})


# Create a new quiz.
@login_required(login_url='login')
def quiz_create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz created successfully!')
            return redirect('quiz_list')
    else:
        form = QuizForm()
    return render(request, 'quiz_form.html', {'form': form})


# Update an existing quiz
@login_required()
def quiz_update(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz updated successfully!')
            return redirect('quiz_list')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quiz_form.html', {'form': form})


# Delete a quiz
@login_required(login_url='login')
def quiz_delete(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz deleted successfully!')
        return redirect('quiz_list')
    return render(request, 'quiz_confirm_delete.html', {'quiz': quiz})


# List Categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

# Create Category
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form, 'action': 'Create'})

# Update Category
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form, 'action': 'Update'})

# Delete Category
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})