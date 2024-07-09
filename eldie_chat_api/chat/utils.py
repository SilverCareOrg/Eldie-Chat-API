import environ
import jwt

from rest_framework.exceptions import AuthenticationFailed
from elasticsearch import NotFoundError

env = environ.Env()
environ.Env.read_env()

def get_user(request):
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    if not token:
        raise AuthenticationFailed('Unauthenticated')

    return jwt.decode(token, key = 'SECRET_KEY', algorithms = ['HS256'])['username']

def summarize_conversation(openai, user, text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize the following text in few words, extract the keypoints and the most important information so I can resend the summarized version of the conversation to you."},
            {"role": "user", "content": text}
        ],
        user=user,
        temperature=0.5,
    )
    summary = response.choices[0].message.content
    return summary.strip()

def get_previous_chat(es, user):
    try:
        response = es.search(
            index = env('ELDIE_ES_SUMMARIZED_MESSAGES_INDEX'),
            body = {
                'query': {
                    'term': {
                        'user': user
                    }
                },
                'sort': [
                    {
                        'timestamp': {
                            'order': 'desc'
                        }
                    }
                ]
            }
        )
        
        if len(response['hits']['hits']) == 0:
            return "No previous chat found."

        # Concat all messages into a string with a newline separator and with the timestamp, sorted
        result = ''.join([f"{hit['_source']['timestamp']}: {hit['_source']['message']}\n" for hit in response['hits']['hits']])
        return result
    except:
        return "No previous chat found."
    
def get_last_messages(es, user, inf, sup):
    """
        inf - lower bound for the number of messages
        sup - upper bound for the number of messages
    """

    try:
        response = es.search(
            index = env('ELDIE_ES_MESSAGES_INDEX'),
            body = {
                'query': {
                    'term': {
                        'user': user
                    }
                },
                'sort': [
                    {
                        'timestamp': {
                            'order': 'desc'
                        }
                    }
                ],
                'from': inf,
                'size': sup
            }
        )

        if len(response['hits']['hits']) == 0:
            return "No previous chat found."

        result = {
            'messages': [
                {
                    'timestamp': hit['_source']['timestamp'],
                    'message': hit['_source']['message'],
                    'sender': 'user' if hit['_source']['direction'] == 'to' else 'assistant'
                } for hit in response['hits']['hits']
            ]
        }
        return result
    except Exception as e:
        print(e)
        return []
        
    