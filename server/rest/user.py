from flask import Response, request
from flask import current_app as app
from db.models import User
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from errors import InternalServerError, SchemaValidationError, UserNotFoundError, EmailAlreadyExistError
from redis import Redis
from datetime import timedelta
import json
from random import randrange
import math
from faker import Faker
from faker.providers import date_time

fake = Faker()
fake.add_provider(date_time)

redis_cache = Redis("redis-master", 6379)

def cache_key():
   args = request.args
   key = request.path
  
   return key

CACHE_TIMEOUT = 100

class UsersApi(Resource):
	def get(self):

		#app.logger.info(cache_key())
		
		cached_user = redis_cache.get(cache_key())
		if cached_user is not None:
			#app.logger.info("Users in the cache")
			#app.logger.info(cached_user)

			ttl = redis_cache.ttl(cache_key())
			rnd = randrange(CACHE_TIMEOUT)
			if rnd < CACHE_TIMEOUT - ttl:
				users = User.objects().to_json()
				redis_cache.setex(cache_key(), timedelta(seconds=CACHE_TIMEOUT), value=users,)
			else:
				cdata = json.loads(cached_user.decode("UTF-8"))
				users = json.dumps(cdata)
		else:
			#app.logger.info("No users in the cache")
			users = User.objects().to_json()
			redis_cache.setex(cache_key(), timedelta(seconds=CACHE_TIMEOUT), value=users,)

		return Response(users, mimetype="application/json", status=200)

	def delete(self):
		redis_cache.delete(cache_key())
		user = User.objects.delete()
		return '', 200

	def post(self):
		try:
			#body = json.loads(request.get_json())
			body = {}
			body['birthdate'] = fake.date()
			body["name"] = fake.name()
			body["email"] = fake.email()

			#app.logger.info(body)
			#user = User(name=body["name"], email=body["email"], birthdate=datetime.strptime(body["birthdate"], '%Y-%m-%d').date())
			user = User(name=body["name"], email=body["email"], birthdate=body["birthdate"])
			
			#db.session.add(user)
			#db.session.commit()
			#app.logger.info(user.serialize())

			user.save()
			id = user.id

			redis_cache.delete(cache_key())
			redis_cache.setex(str(id), timedelta(seconds=CACHE_TIMEOUT), value=json.dumps(body),)

			return {'id': str(id)}, 201
		except Exception as e:
			app.logger.error(e)
			raise InternalServerError

class UserApi(Resource):
	def put(self, id):
		body = request.get_json()
		
		redis_cache.delete(cache_key())
		redis_cache.setex(id, timedelta(seconds=CACHE_TIMEOUT), value=body,)

		User.objects.get(id=id).update(**body)

		return '', 200

	def get(self, id):
		try:
			cached_user = redis_cache.get(id)
			if cached_user is not None:
				#app.logger.info("User {0} in the cache".format(id))
				#app.logger.info(cached_user)

				cdata = json.loads(cached_user.decode("UTF-8"))
				users = json.dumps(cdata)
			else:
				#app.logger.info("No user {0} in the cache".format(id))
				users = User.objects.get(id=id).to_json()
			return Response(users, mimetype="application/json", status=200)
		except DoesNotExist:
			raise UserNotFoundError

	def delete(self, id):
		redis_cache.delete(id)
		redis_cache.delete(cache_key())
		user = User.objects.get(id=id).delete()
		return '', 200