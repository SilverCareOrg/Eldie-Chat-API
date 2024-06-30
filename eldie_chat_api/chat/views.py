import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.shortcuts import render

from eldie_chat_api.settings import openai_client
from .utils import (
    get_user,
    summarize_conversation,
    get_previous_chat,
)
from elasticsearch_utils.es import (
    save_message_to_es,
    instantiate_elasticsearch,
    save_keypoints_to_es,
)

@api_view(['POST'])
def chat_send_message(request):
    data = json.loads(request.body)

    message = data['message']
    user = get_user(request)    

    es = instantiate_elasticsearch()

    save_message_to_es(es, user, message, 'to')

    previous_chat = get_previous_chat(es, user)

    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for elderly people. Consider the previous chat but try to respond to the new message."},
            {"role": "user", "content": f"Previous Chat: {previous_chat}, New message: {message}"}
        ],
        user=user,
        temperature=0.5,
    )

    response = completion.choices[0].message.content
    
    save_message_to_es(es, user, response, 'from')
    
    processed_text = f"{user}: {message}\nAssistant: {response}"
    keypoints = summarize_conversation(openai_client, user, processed_text)

    save_keypoints_to_es(es, user, keypoints)    

    return JsonResponse({'response': response})