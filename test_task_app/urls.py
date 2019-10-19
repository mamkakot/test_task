from django.urls import path

from . import views

app_name = 'test_task_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
