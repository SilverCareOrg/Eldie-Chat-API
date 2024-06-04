from django.urls import path
from .views import chat_send_message

urlpatterns = [
    path('chat_send_message', chat_send_message),
]