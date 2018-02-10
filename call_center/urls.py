from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('call/', include('call.urls')),
    path('employee/', include('employee.urls')),
	path('stats/', include('stats.urls')),

]
