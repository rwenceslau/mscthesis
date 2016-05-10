#	Main part of the algorithm, which loads ISS data to memory.
#	-----------------------------------------------------------

__author__ = 'rodrigowenceslau'

fileFoursquareI = '../Dados/foursquare/foursquare_coletacompleta/foursquare_Primeiracoleta.json'
fileFoursquareII = '../Dados/foursquare/foursquare_coletacompleta/foursquare_segundacoleta.json'
fileGPlaces = '../Dados/gplaces/gplacesdata.csv'

import pudb
import loadGplaces
import compareGplaces
import loadISS
import disambiguateGplaces

print "\nReading ISS file ...\n"
issEntities = loadISS.read_iss()
#print len(issEntities.keys())
# Loads Google Place data.

print "Converting Google Places entries ...\n"
#loadGplaces.read_translate_GPlaces()

print "Reading Google Places file ...\n"
gPlacesEntities = loadGplaces.load_GPlaces()
#print len(gPlacesEntities.keys())

print "Removing Google Places file duplicates ...\n"
gPlacesEntities = disambiguateGplaces.disambiguate_GPlaces_entries(gPlacesEntities)

print "Comparing ISS x Google Places data ...\n"
#print len(gPlacesEntities.keys())
compareGplaces.compare_gplaces_iss(gPlacesEntities, issEntities)
