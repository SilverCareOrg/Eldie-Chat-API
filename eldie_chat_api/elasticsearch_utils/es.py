import environ

from elasticsearch import Elasticsearch, NotFoundError
from datetime import datetime

env = environ.Env()
environ.Env.read_env()

def instantiate_elasticsearch():

	ELASTIC_HOST = f"https://{env('ELDIE_ELASTICSEARCH_HOST')}/elastic/"
	ELASTIC_USER = env('ELDIE_ELASTICSEARCH_USER')
	ELASTIC_PASSWORD = env('ELDIE_ELASTICSEARCH_PASSWORD')

	es = Elasticsearch(
		hosts = ELASTIC_HOST,
		basic_auth = (ELASTIC_USER, ELASTIC_PASSWORD),
	)

	return es

def save_to_es(es, index_name, doc):
	es.index(index = index_name, document = doc)

def save_message_to_es(es, user, message, d):
	doc = {
		'user': user,
		'message': message,
		'timestamp': datetime.now(),
		'direction': d
	}

	save_to_es(es, env('ELDIE_ES_MESSAGES_INDEX'), doc)
 
def save_keypoints_to_es(es, user, keypoints):
	doc = {
		'user': user,
		'message': keypoints,
		'timestamp': datetime.now()
	}

	save_to_es(es, env('ELDIE_ES_SUMMARIZED_MESSAGES_INDEX'), doc)