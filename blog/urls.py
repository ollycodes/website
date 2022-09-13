from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('entry/<int:pk>/', views.EntryView.as_view(), name='entry'),
]
