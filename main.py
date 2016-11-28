#	Main part of the algorithm, which loads ISS data to memory and compares it to Google Places data.
#	-----------------------------------------------------------

__author__ = 'rodrigowenceslau'

fileGPlaces = '../Dados/gplaces/gplacesdata.csv'

import pudb
#import loadGplaces
import loadGPlacesCoordinates
#import compareGplaces
import compareGPlacesCoordinates
#import loadISS
import loadISSCoordinates

#import disambiguate

print "\nReading ISS file ...\n"
issEntities = loadISSCoordinates.read_iss()
print len(issEntities.keys())
# Loads Google Place data.

#print "Converting Google Places entries ...\n"
#loadGPlacesCoordinates.read_translate_GPlaces()

print "Reading Google Places file ...\n"
gPlacesEntities = loadGPlacesCoordinates.load_GPlaces()
#print len(gPlacesEntities.keys())

loadGPlacesCoordinates.createFilePostGres(gPlacesEntities)

#print "Removing Google Places file duplicates ...\n"
#gPlacesEntities = disambiguate.disambiguate_GPlaces_entries(gPlacesEntities)
#print len(gPlacesEntities.keys())

print "Comparing ISS x Google Places data ...\n"
#print len(gPlacesEntities.keys())
compareGPlacesCoordinates.compare_gplaces_iss(gPlacesEntities, issEntities)
