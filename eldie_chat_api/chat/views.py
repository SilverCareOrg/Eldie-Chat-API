import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from eldie_chat_api.settings import openai_client
from django.shortcuts import render

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def chat_send_message(request):
    data = json.loads(request.body)
    message = data['message']
    user = data['user']

    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for elderly people."},
            {"role": "user", "content": message}
        ],
        user=user,
        temperature=0.5,
    )

    return completion.choices[0].message