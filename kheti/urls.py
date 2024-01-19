# everest_broker/urls.py
from django.urls import path
from .views import receive_post, live_data

urlpatterns = [
    path('receive_post/', receive_post, name='receive_post'),
    path('', live_data, name='live_data'),
    # Add other URL patterns as needed
]
