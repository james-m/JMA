
from django.conf import settings

def db_find(id):
	if not id:
		return None
	return id >> 28

def get_shards(shard_type):
	shards = filter(
		lambda x: x[1] & shard_type == shard_type, 
		settings.DB_INFO)
	return [s[0] for s in shards]