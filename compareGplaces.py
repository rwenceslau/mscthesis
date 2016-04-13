#	Compares GPlaces and ISS data searching for ambiguities and resolving it.
#	-----------------------------------------------------------

__author__ = 'rodrigowenceslau'
from nltk.metrics import edit_distance

def compare_gplaces_iss(gPlacesEntities, issEntities):

	hits = 0

	# Comparing each entry from GPlaces with ISS data, trying to get a match between DBs.
	for gplacesEntry in gPlacesEntities:
		gplacesEntry = gplacesEntry.split(',')
		gplacesAddress = gplacesEntry[3]+gplacesEntry[4]	# Getting the address (first comparison point).
		gplacesAddress.upper()								# Converting it to uppercase, since ISS data is formatted this way.
		gplacesCNAE = gplacesEntry[:-1].split(' ')			# Getting CNAE ids of the entry.
		gplacesCNAE = map(int, gplacesCNAE)					# Transforming strings to integers.

		for issEntry in issEntities:
			issAddress = issEntry[1] + issEntry[2]			# ISS entry address.
			issMainCNAE = issEntry[3]						# ISS entry main CNAE.
			issSecCNAE = issEntry[4]						# ISS entry secondary CNAE.
			similarity = edit_distance(gplacesAddress, issAddress)		# Calculates similarity through Levenshtein distance.
			print similarity

			if issMainCNAE in gplacesCNAE:						# Checks if the activities are the same. The algorithm
				print "HIT!"									# considers the entities the same if CNAE and address are the same.
				hits += 1
			elif issSecCNAE in gplacesCNAE:
				print "HIT!"
				hits += 1





