from django.urls import path
from . import views

app_name = 'call'

urlpatterns = [
    path('detail/', views.GetCall.as_view()),
    path('upload/', views.upload_call),
]
