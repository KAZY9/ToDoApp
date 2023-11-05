from django.urls import path
from . import views
from .views import TaskCreate, TaskList, TaskDetail, TaskUpdate, TaskDelete ,TaskListLoginView, RegisterToDoApp
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", TaskList.as_view(), name="tasks"),  #rootディレクトリを選ぶときは空にする #views.pyでクラスビューの場合はas_view()をつける
    path("task/<int:pk>/",  TaskDetail.as_view(), name="task"), #nameを指定することでhtmlでurlを表示する際nameで指定できる
    path("create-task/",  TaskCreate.as_view(), name="create-task"),
    path("edit-task/<int:pk>/",  TaskUpdate.as_view(), name="edit-task"),
    path("delete-task/<int:pk>/",  TaskDelete.as_view(), name="delete-task"),
    path("login/",  TaskListLoginView.as_view(), name="login"),
    path("logout/",  LogoutView.as_view(next_page="login"), name="logout"),
     path("register/",  RegisterToDoApp.as_view(), name="register")
]