#	Main part of the algorithm, which loads ISS data to memory and compares it to Foursquare data.
#	-----------------------------------------------------------

__author__ = 'rodrigowenceslau'


import pudb
import loadISS
import readFoursquare
import disambiguate


print "\nReading ISS file ...\n"
#issEntities = loadISS.read_iss()
#print len(issEntities.keys())

# Loads Foursquare data.

print "Translating Foursquare categories ...\n"
#loadGplaces.read_translate_GPlaces()

print "Reading Foursquare file ...\n"
foursquareEntities = readFoursquare.load_foursquare()
print len(foursquareEntities.keys())

print "Removing Foursquare file duplicates ...\n"
foursquareEntities = disambiguate.disambiguate_foursquare_entries(foursquareEntities)
print len(foursquareEntities.keys())

#foursquareCategories = set()
#for key, value in foursquareEntities.items():
	#foursquareCategories.add(value[2])

#with open('../Dados/foursquare/foursquareCategories.csv', 'w') as categoriesFoursquare:
	#for category in foursquareCategories:
	#	categoriesFoursquare.write(category+'\n')
