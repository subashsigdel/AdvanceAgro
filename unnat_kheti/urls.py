from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kheti.urls')),
    path('client/', include('balli.urls')),
]
