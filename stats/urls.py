from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'stats'

urlpatterns = [
    path('', views.GetStats.as_view()),
    path('top/', views.GetTopEmployees.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)