from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'call'

urlpatterns = [
    path('detail/', views.GetCall.as_view()),
   	path('upload/', views.UploadCall.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)