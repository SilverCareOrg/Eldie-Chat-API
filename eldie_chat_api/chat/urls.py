from django.urls import path
from .views import (
    chat_send_message,
    get_previous_messages,
)

urlpatterns = [
    path('chat_send_message', chat_send_message),
    path('get_previous_messages', get_previous_messages),
]