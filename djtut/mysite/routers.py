import exceptions
import random
import sys
import os

from django.conf import settings

import dbconf

class RouterException(exceptions.Exception):
	pass

class BaseRouter(object):
	APP_LABEL = None # set me in subclass
	
	def _validate(self, *models):
		for model in models:
			if model._meta.app_label != self.APP_LABEL:
				return False
		return True

	def db_for_read(self, model, **hints):
		if not self._validate(model):
			return None
		return self.read(model, **hints)
		
	def db_for_write(self, model, **hint):
		if not self._validate(model):
			return None
		return self.write(model, **hint)
		
	def allow_relation(self, model1, model2, **hints):
		if not self._validate(model1, model2):
			return None
		return self.relation(model1, model2, **hints)
	
	def allow_syncdb(self, db, model):
		if not self._validate(model):
			return False
		return self.syncdb(db, model)

	# overwrite in the sub-class
	#
	def read(self, model, **hints):
		pass		
	def write(self, model, **hints):
		pass	
	def relation(self, obj1, obj2, **hints):
		pass		
	def syncdb(self, db, model):
		pass

class PollsRouter(BaseRouter):
	APP_LABEL  = 'polls'
	SHARD_TYPE = settings.DB_SHARD_POLLS
	
	def read(self, model, **hints):
		print 'db_for_read', model, hints
		return None
	
		
	def write(self, model, **hints):
		# if there is an isntance hint, use it to find the shard. 
		# if the instance's pk is None this implies an insert, so 
		# we pick a instance at random.
		#
		print 'write', model, hints
		obj = hints.get('instance')
		if obj is None:
			# unclear what to do
			return None
			
		# if the model is a Choice, we need to select the shard based on 
		# the Choice's poll id
		#
		print 'model.poll', getattr(model, 'poll', None)
		if model._meta.object_name == 'Choice':
			shard = dbconf.db_find(obj.poll.pk)
			print 'write Choice, found shard', shard
			if shard is None:
				raise Exception('No poll set for Choice!')
		else:
			shard = dbconf.db_find(obj.pk)
			print 'write Poll, found shard', shard
			if shard is None:
				# new object, find a random shard and select it
				#
				return self.find_new_poll()
		# we've found the shard, return the name
		#
		return 'test%s' % shard
		
		
	def relation(self, model1, model2, **hints):
		print 'allow_relation', model1, model2, hints
		return None
	
	def syncdb(self, db, model):
		# if we pass the validate in the super class (which simply checks
		# the correct app_label for now) we're good to sync
		#
		return True
		
	def find_new_poll(self):
		# when an object is new we need to select a shard to insert it into.
		# here its just a random selection but one could easily have waited
		# random selection as new shards get added to the pool. 
		# 
		poll_shards = dbconf.get_shards(self.SHARD_TYPE)
		shard = random.choice(shards)
		print 'shard for create', shard
		return shard[0]