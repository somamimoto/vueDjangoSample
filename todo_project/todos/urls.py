from django.urls import path, include
from . import views
from .views import TodoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = [
    # path('', views.todo_list, name='todo_list'),
    # path('todo/<int:pk>/', views.todo_detail, name='todo_detail'),
    # path('todo/new/', views.todo_create, name='todo_create'),
    # path('todo/<int:pk>/edit/', views.todo_update, name='todo_update'),
    # path('todo/<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('api/', include(router.urls))
]
