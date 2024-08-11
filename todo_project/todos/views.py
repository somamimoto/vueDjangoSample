from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo
from rest_framework import viewsets
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


def todo_list(request):
    todos = Todo.objects.all()
    return render(request, 'todos/todo_list.html', {'todos': todos})


def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    return render(request, 'todos/todo_detail.html', {'todo': todo})


def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        todo = Todo(title=title, description=description)
        todo.save()
        return redirect('todo_list')
    return render(request, 'todos/todo_form.html')


def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.completed = 'completed' in request.POST
        todo.save()
        return redirect('todo_list')
    return render(request, 'todos/todo_form.html', {'todo': todo})


def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('todo_list')
