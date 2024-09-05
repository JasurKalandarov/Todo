from django.contrib import admin
from django.urls import path, include
from task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('task.urls')),
    path('accounts/', include('accounts.urls')),
]
