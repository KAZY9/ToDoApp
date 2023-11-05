from typing import Any
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from ToDoApp.models import Task

# Create your views here.
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs): #ListViewの持っている関数→オーバーライドしている
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)

        searchInputText = self.request.GET.get("search") or "" #検索窓に打ち込んだ文字を取得
        if searchInputText:
            context["tasks"] = context["tasks"].filter(title__startswith=searchInputText)

        context["search"] = searchInputText
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "completed"] #モデルの全ての属性 ["user", "title", ...]
    success_url = reverse_lazy("tasks") #クラスベースビューredirecの際はreverse_lazy、関数ベースビューの場合render

    def form_valid(self, form): #formを投稿できる人を制限する　オーバーライド
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = "__all__" #モデルの全ての属性 ["user", "title", ...]
    success_url = reverse_lazy("tasks") #クラスベースビューredirecの際はreverse_lazy、関数ベースビューの場合render

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    fields = "__all__" #モデルの全ての属性 ["user", "title", ...]
    success_url = reverse_lazy("tasks") #クラスベースビューredirecの際はreverse_lazy、関数ベースビューの場合render
    context_object_name = "task"

class TaskListLoginView(LoginView):
    fields = "__all__"
    template_name = "ToDoApp/login.html" #テンプレートのフォルダパスを変更できる

    def get_success_url(self):
        return reverse_lazy("tasks")

class RegisterToDoApp(FormView):
    template_name = "ToDoApp/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form) #フォームの成功したバリデーション後に success_url にリダイレクトする動作
