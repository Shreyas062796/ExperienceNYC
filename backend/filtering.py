import sys
import places
import json
from operator import itemgetter
from math import sin, cos, sqrt, atan2, radians

DEBUG = False


class Filtering:
	def __init__(self, latitude, longitude):
		# self.bars = dict()
		self.bars = places.getNYCBars()['results']
		self.restaurants = dict()
		self.latitude = latitude
		self.longitude = longitude


	def getBars(self):
		self.bars = places.getNYCBars()['results']

	def getRestaurants(self):
		self.restaurants= places.getNYCRestaurants()['results']

	# this is accomplished using the haversine formula (using the radius of earth in km)
	# assumes earth is a sphere, 0.5% error range
	def coorDistance(self, to_lat, to_lon, units='kms'):
		R = 6373.0 # approximate radius of earth

		# equation works in radians
		lat1 = radians(self.latitude)
		lon1 = radians(self.longitude)
		lat2 = radians(to_lat)
		lon2 = radians(to_lon)

		dlat = lat2-lat1
		dlon = lon2-lon1

		# haversine formula
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2* atan2(sqrt(a), sqrt(1-a))
		distance = R*c

		if units=='miles':
			#1km = 0.621371 miles
			distance = distance * 0.621371

		return distance

		# scoreing function for how likely you should be to go to a place
		# you shouldn't have to walk more than 3 miles from the place you are in
	def score(self, rating, distance):
		miles = distance/5280
		if miles>2:
			return 0
		else:
			return 1/(5.2-rating)*(2-miles)

	# WILL CHANGE AS WE CREATE A BETTER ESTIMATE
	# objective of this is to create a system that will work in the sort of give up .1 rating for ever 100 feet you have to walk
	# from the path you have
	def filterby(self, location_list, coordinates=(40.7831,-73.9712), rating=False, price_level=False, place_type=None):
		# print(location_list)
		top_places = dict()
		for place in location_list:
			d_id = place['place_id']
			lng = place['geometry']['location']['lng']
			lat = place['geometry']['location']['lat']
			distance = self.coorDistance(lat, lng, units='miles')
			rating = float(place['rating'])

			place_score = self.score(rating, distance)
			top_places[d_id] = place_score
		return top_places
		# returns a dictionary with each popular as a key and their score as a value

	# return the list of places as a json for the frontend
	def getBarsJson(self):
		return json.dumps(self.bars)

	def getTopRestaurantsJson(self):
		return json.dumps(self.restaurants)

	# get the top n elements of the dict generated by filterby top recomment the best
	def getTopBars(self, n, output='dict'): # self.bars/self.restaurants
		returnlst = list()

		places = self.filterby(self.bars)

		top = sorted(places.items(), key=lambda x: x[1])[-n:]
					
		for item in top:
			for i in range(len(self.bars)):
				if item[0] == self.bars[i]['place_id']:
					returnlst.append(self.bars[i])


		if output == 'json':
			return json.dumps(returnlst)
		else:
			return returnlst

	# my score functon is petty work on something better soon
	def newscore(self):
		# this is for when we have more parameters to fix
		pass



def main():
	if DEBUG:

		ex_lat = 40.7831
		ex_lng = 73.9712

		myobj = Filtering(ex_lat, ex_lng)
		myobj.getBars()


		places = myobj.filterby(myobj.bars)
		# [print("{}:\t{}".format(key,val)) for key,val in places.items()]

		print(myobj.getTopBars(3, output='json'))
		# print(places)

		# bars = places.getNYCBars()['results'] # bars is a list


		# print(bars[1]['id'])
		# sorted_by_score = sorted(bars, key=itemgetter('rating'))

		# # with open('example.json', 'w') as File:
		# # 	json.dump(bars, File)


if __name__ == '__main__':
	main()


