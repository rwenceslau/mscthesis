#	Loads Google Places entries to memory.
#	-----------------------------------------------------------

__author__ = 'rodrigowenceslau'

fileGPlacesInput = '../Dados/gplaces/gplacesdata.csv'
fileGPlacesOutput = '../Dados/gplaces/gplacesOutputFull.csv'
fileGplacesISS = '../Dados/gplaces/GPlacesCategories.csv'

import csv
import re
import pudb
from geopy.geocoders import Nominatim
import sys
reload(sys)
sys.setdefaultencoding('utf-8') # ou Latin1 ou cp1552
import time

gPlacesCategoriesCounter = 0
gPlacesCategories = []
notServices = ['political', 'route', 'neighborhood', 'transit_station', 'post_box', 'intersection', 'bus_station', 'locality']
streetIndicators = ['Rua', 'Avenida', 'Pra\xc3a']
geolocator = Nominatim()

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Checks if a value is an address.
def check_string_for_street(s):
	for indicators in streetIndicators:
		if indicators in s:
			return True

# Loads the conversion table between GPlaces categories and its respective ISS translations.
def load_gplaces_translation_table():

	translationTable = {}

	with open(fileGplacesISS) as transFile:
		tableReader = csv.reader(transFile, delimiter = ',')
		next(tableReader)
		for row in tableReader:
			categoryGPlaces = row[0]
			categoryISS = int(row[1])

			translationTable[categoryGPlaces] = categoryISS


	return translationTable

# Translates categories loaded from GPlaces entries to ISS category ID. Returns a list of integers.
def translate_gplaces_iss_areas(placeCategories, translationTable):

	translatedCat = []
	#pu.db
	#print placeCategories
	for category in placeCategories:
		issCategory = translationTable[category]
		translatedCat.append(issCategory)

	return translatedCat


# Parses the list of categories which identifies the place. 
def parse_place_categories(areas):

	resultList = []
	isService = 1

	for area in areas:
		area = area.translate(None, "[] ")
		area = re.sub("u'","",area)
		area = area[:-1]

		if area in notServices:			# Checks if the place is really a service.
			isService = 0			

		#print area
		if isService:
			resultList.append(area)

	#print resultList
	return resultList

# Main function: Reads GPlaces file, translates its categories and saves it to a new file.
def read_translate_GPlaces():

	translationTable = load_gplaces_translation_table()
	translatedCategories = []
	idCounter = 0
	
	with open(fileGPlacesInput, 'r') as gplacesInput:
		gPlacesReader = csv.reader(gplacesInput, delimiter=';')
		next(gPlacesReader)
		with open(fileGPlacesOutput, 'a') as gplacesOutput:
			for row in gPlacesReader:
				#print row
				idCounter += 1													# Simple ID for easy access to dictonary entries.
				placeName = row[2]												# Place name (not address).
				placeCategories = parse_place_categories(row[4].split(','))		# Parsing place categories.
				coord_x = row[-2]
				coord_y = row[-3]
				
				#print coord_x, coord_y

				if placeCategories:
					#print pointId
					translatedCategories = translate_gplaces_iss_areas(placeCategories, translationTable)
					#gPlacesEntities[idCounter] = pointId, placeName, placeCategories, translatedCategories, placeAddress
					gplacesOutput.write('{}, {}, {}, {}'.format(idCounter, coord_x, coord_y, placeName))
					gplacesOutput.write(', ')
					gplacesOutput.write(','.join(placeCategories))
					gplacesOutput.write(', ')
					w = ''
					for cat in translatedCategories:
						w += "{} ".format(cat)
						gplacesOutput.write(w)
					gplacesOutput.write('\n')


# This function actually loads GPlaces data after preprocessing from 'read_translate_GPlaces'.
def load_GPlaces():

	gPlacesEntities = {}
	idCounter = 0

	with open(fileGPlacesOutput, 'r') as gplacesFile:
		gPlacesReader = csv.reader(gplacesFile, delimiter=',')
		for row in gPlacesReader:
			#print row[2]
			coord_x = row[1]
			coord_y = row[2]
			placeName = row[3]
			#pudb.set_trace()
		
			categories = row[-1].split(" ")
			uniqueSet = set(categories)		# Removing CNAE duplicates.
			categories = list(uniqueSet)
			del categories[0]
			#print categories
			gPlacesEntities[idCounter] = placeName, coord_x, coord_y, categories
			#print gPlacesEntities[idCounter]
			idCounter += 1
	return gPlacesEntities

def createFilePostGres(gPlacesEntities):

	with open('gplacesPG.csv', 'w') as gplacesFile:
		for key, value in gPlacesEntities.iteritems():
			#print key, value
			gplacesFile.write('{};{};{};{}'.format(key, value[0][1:], value[2][1:], value[1][1:]))
			gplacesFile.write(';')
			w = ''
			for cat in value[3]:
				if cat is not '0':
					w += "{};".format(cat)
					gplacesFile.write(w)
					#gplacesFile.write(';')
			gplacesFile.write('\n')
