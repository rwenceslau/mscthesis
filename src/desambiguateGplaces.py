__author__ = 'rodrigowenceslau'

def disambiguate_GPlaces_entries(gplacesEntities):

	results = {}

	for key, value in gplacesEntities.items():
		if value[0] not in result.values():
			result[key] = value