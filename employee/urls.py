from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'employee'

urlpatterns = [
    path('list/', views.GetEmployeeList.as_view()),
    path('detail/', views.GetEmployee.as_view()),
    path('score/', views.GetScore.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
