
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('process/<int:hours>/<str:place>/<str:crop_type>/',
         views.process, name='process'),
    path("waterd/<str:place>/", views.water, name="waterd")

]
