from django.urls import path

from . import views

app_name = "twentyone"
urlpatterns = [
    path('', views.game, name='game'),
]
