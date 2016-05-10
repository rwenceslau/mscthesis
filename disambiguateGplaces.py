__author__ = 'rodrigowenceslau'

# Gets rid of all duplicates entries in the GPlaces dictonary.
def disambiguate_GPlaces_entries(gplacesEntities):

	result = {}
	idCounter = 0

	for key, value in gplacesEntities.items():
		if value not in result.values():
			result[idCounter] = value
			idCounter += 1

	return result