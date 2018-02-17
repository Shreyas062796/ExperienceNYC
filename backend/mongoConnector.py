from pymongo import *
from places import *
from bson.objectid import *

def placesConnect():
	client = MongoClient('mongodb://localhost:27017/')
	placesdb = client.places
	return(placesdb)

def loginConnect():
	client = MongoClient('mongodb://localhost:27017/')
	logindb = client.loginInfo
	return(logindb)

def tagsConnect():
	client = MongoClient('mongodb://localhost:27017/')
	tagsdb = client.Tags
	return(tagsdb)


def populateRestaurants():
	restaurants = getNYCRestaurants()
	db = placesConnect()
	for restaurant in restaurants['results']:
		db.restaurants.insert_one(restaurant)

def populateBars():
	bars = getNYCBars()
	db = placesConnect()
	for bar in bars['results']:
		db.bars.insert_one(bar)


def getBars():
	allBars = []
	db = placesConnect()
	for document in db.bars.find():
		allBars.append(document)
	return(allBars)

def populateLogin(login):
	db = loginConnect()
	db.Info.insert_one(tag)

def authenticateLogin(username,password)):
	db = loginConnect()
	for login in db.Info.find({"username": username}):
		if(login["password"] == password):
			return(True)
	return(False)
	#authenticate login and return true or false


def populateTags(tags):
	db = tagsConnect()
	for tag in tags:
		db.Tags.insert_one(tag)

def getRestaurants():
	allRestaurants = []
	db = placesConnect()
	for document in db.restaurants.find():
		allRestaurants.append(document)
	return(allRestaurants)

def QueryRestaurants(cost,rating):
	for restaurant in getRestaurants():
		if('price_level' in restaurant and 'rating' in restaurant):
			if(restaurant['rating'] >= rating and restaurant['price_level'] >= cost):
				pprint(restaurant)

if __name__ == "__main__":
	#populateRestaurants()
	#populateBars()
	#print(getBars())
	QueryRestaurants(3,4)