from django.db.models import manager

import exceptions

import dbconf

class ShardException(exceptions.Exception):
	pass

class ShardManager(manager.Manager):
	
	def use(self, alias):
		self._db = alias
	
	def find_alias(self, hint):
		if hint is None:
			return None
		shard = dbconf.db_find(hint)		
		return 'test%d' % shard
	
	def get(self, *args, **kwargs):
		alias = self.find_alias(kwargs.get('id', kwargs.get('pk')))
		if alias is None:
			return super(ShardManager, self).get(*args, **kwargs)
		self.use(alias)
		return super(ShardManager, self).get(*args, **kwargs)
		
	def all(self):
		raise ShardException('Cannot call all() on sharded data.')
		