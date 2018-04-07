from pymongo import *
from bson.objectid import *
import random
import json
import hashlib
import uuid
from pprint import pprint


class UsersMongo:
	def __init__(self,clientHost,clientPort,username,password,database):
		self.clientHost = clientHost
		self.clientPort = clientPort
		self.username = username
		self.password = password
		self.database = database

	#populates user collection with user information
	def populateLogin(self,login):
		db = self.clientConnect()
		login['password'] = hashlib.md5(login['password'].encode('utf-8')).hexdigest()
		db.users.insert_one(login)

	#authenticating login given a username and
	def authenticateLogin(self,username,password):
		db = self.clientConnect()
		login = db.users.find_one({"username": username})
		if(login):
			if(login["password"] == hashlib.md5(password.encode('utf-8')).hexdigest()):
				return(True)
		return(False)

	#verifies email with the user 
	def verifyEmail(self,username,unique_id):
		db = self.clientConnect()
		user = db.users.find_one({"username": username})
		if(user['user_unique_id'] == unique_id):
			user['verify'] = True
			return(True)
		return(False)

	#populates the tags
	def addTags(self,username,tags):
		db = self.clientConnect()
		user = db.users.find_one({"username": username})
		for tag in tags:
			if(tag not in user['tags']):
				db.users.update_one({'username': username},{'$push':{'tags':tag}})
				return("Added")
			else:
				return("Already Exists")

	def removeTags(self,username,tags):
		db = self.clientConnect()
		for tag in tags:
			db.users.update_one({'username': username},{'$pull':{'tags':tag}})
			print("removed")

	def getTags(self,username):
		db = self.clientConnect()
		user = db.users.find_one({"username": username})
		return(user['tags'])

		#authenticate login and return true or false
	#adds favorite places to user profile
	def addFavoritePlaces(self,username,place_id):
		db = self.clientConnect()
		user = db.users.find({'username': username})
		if(place_id not in db.users.find({'username': username})):
			db.users.update_one({'username': username},{'$push':{'favorite_places':place_id}})
			return("Added")
		else:
			return("Already Exists")

	#removes favorite places to user profile
	def removeFavoritePlaces(self,username,place_id):
		db = self.clientConnect()
		db.users.update_one({'username': username},{'$pull':{'favorite_places':place_id}})
		print("added")

	#gets all the favorite place id's from the user profile
	def getFavoritePlacesIds(self,username):
		db = self.clientConnect()
		user = db.users.find_one({"username": username})
		print(user['favorite_places'])
		return(user['favorite_places'])

	#gets all the favorite places from the user profile
	def getFavoritePlaces(self,username):
		db = self.clientConnect()
		favoritePlaces = []
		user = db.users.find_one({"username": username})
		if(user['favorite_places']):
			for placeId in user['favorite_places']:
				place = db.places.find_one({"place_id": placeId})
				if(place is not None):
					place['_id'] = str(place['_id'])
					favoritePlaces.append(place)
		return(favoritePlaces)

	#adds a saved trip place to the user profile 
	def addTripPlaces(self,username,place_id):
		db = self.clientConnect()
		user = db.users.find({'username': username})
		if(place_id not in db.users.find({'username': username})):
			db.users.update_one({'username': username},{'$push':{'current_trip_places':place_id}})
			return("Added")
		else:
			return("Already Exists")

	#removes a saved trip place to the user profile
	def removeTripPlaces(self,username,place_id):
		db = self.clientConnect()
		db.users.update_one({'username': username},{'$pull':{'current_trip_places':place_id}})
		print("added")

	#gets all the saved trip placeid's to the user profile
	def getTripPlacesIds(self,username):
		db = self.clientConnect()
		user = db.users.find_one({"username": username})
		return(user['current_trip_places'])

	#gets all the saved trip places by the user
	def getTripPlaces(self,username):
		db = self.clientConnect()
		TripPlaces = []
		user = db.users.find_one({"username": username})
		if(user['current_trip_places']):
			for placeId in user['current_trip_places']:
				place = db.places.find_one({"place_id": placeId})
				if(place is not None):
					place['_id'] = str(place['_id'])
					TripPlaces.append(place)
		return(TripPlaces)