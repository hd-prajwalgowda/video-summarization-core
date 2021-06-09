from pymongo import MongoClient
import os

class DB(object):
	"""docstring for DB"""
	def __init__(self):
		BACKEND_URL = os.environ.get("BACKEND_URL")
		self.mongo_client = MongoClient(BACKEND_URL)
		self.db = self.mongo_client['videosum']
		
	def get_user_collection(self):
		self.user_collection = self.db['users']
		return self.user_collection
		