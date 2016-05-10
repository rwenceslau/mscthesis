#	Compares GPlaces and ISS data searching for ambiguities and resolving it.
#	-----------------------------------------------------------

__author__ = 'rodrigowenceslau'

from nltk.metrics import edit_distance
import pudb

persistenceIndexFile = 'persistentIndexes'
similarityThreshold = 3
#indexGplaces = 0
#indexISS = 0
#hits = 0
hitCNAEStats = {}		# Counts the CNAE categories which got hit.
hitPlaceStats = {}		# Stores the places which got hit.

# Checks if the CNAE is already in the dict and counts it.
def cnae_sum(cnae):

	if cnae in hitCNAEStats.keys():
		oldCounter = hitCNAEStats[cnae]
		hitCNAEStats[cnae] = oldCounter + 1
	else:
		hitCNAEStats[cnae] = 1

# Reads the file which stores the point where the analysis stopped.
def read_index_position():

	with open(persistenceIndexFile, 'r') as indexFile:
		for line in indexFile:
			line = line.split(' ')
			global indexGplaces
			indexGplaces =  int(line[0])
			global indexISS
			indexISS = int(line[1])
			global hits
			hits = int(line[2])
			break
	indexFile.close()

# Write last index position on file so it persists on next run.
def write_index_position():

	with open(persistenceIndexFile, 'w') as indexFile:
		indexFile.write('{} {} {} '.format(indexGplaces, indexISS, hits))
	indexFile.close()

# Compares each entry of GPlaces file with ISS file, and tries to match it.
def compare_gplaces_iss(gPlacesEntities, issEntities):

	read_index_position()
	sorted(gPlacesEntities)
	sorted(issEntities)
	
	try:
		for i in xrange(indexGplaces, len(gPlacesEntities.keys())):
			gplacesEntry = gPlacesEntities[i]
			#print gplacesEntry
		# Comparing each entry from GPlaces with ISS data, trying to get a match between DBs.
		#for gplacesEntry, gplacesValues in gPlacesEntities.iteritems():
			#print gplacesValues
			placeName = str(gplacesEntry[0])
			streetName = str(gplacesEntry[1])
			print "Current entry: {}, {}".format(placeName, streetName)

			#if not check_string_for_street(streetName):		# If the field doesn't provide a valid street name,
			#	streetName = str(gplacesEntry[2])		    # it belongs to a commercial building, so the
															# information is in the next entry position.
			#print indexGplaces
			#print streetName
			#print streetNumber, streetName
			#gplacesAddress = streetName + streetNumber
			gplacesAddress = streetName
			gplacesAddress = gplacesAddress.upper()
			#print gplacesAddress
			gplacesCNAE = gplacesEntry[-1]

			global indexGplaces
			indexGplaces = i

			for j in xrange(0, len(issEntities.keys())):
				issEntry = issEntities[j]
			#for issEntry, issValues in issEntities.iteritems():
				streetName = str(issEntry[0])
				#print streetName
				issAddress = streetName
				issMainCNAE = issEntry[1]
				#print issMainCNAE
				issSecCNAE = issEntry[2]
				#print issSecCNAE
				#print "{} x {}".format(gplacesAddress, issAddress)
				similarity = edit_distance(gplacesAddress, issAddress)
				if similarity <= similarityThreshold:
					#pudb.set_trace()
					print "Candidate detected!"
					#print gplacesCNAE
					#print issMainCNAE
					#print issSecCNAE	
					if issMainCNAE in gplacesCNAE or issSecCNAE in gplacesCNAE:		# Checks if the activities are the same. The algorithm
						print "Similarity: ", similarity
						print "HIT!"												# considers the entities the same if CNAE and address are the same.
						global hits
						hits += 1
						print "MATCH: {} {}".format(placeName, gplacesCNAE)
						print "ISS CNAE: ", issMainCNAE
						cnae_sum(issMainCNAE)										# Adds CNAE to hit stats.
						cnae_sum(issSecCNAE)
						print "CNAE added to stats."
						hitPlaceStats[placeName] = streetName
						print "Place added to stats."
						break

				global indexISS
				indexISS = j
	except (KeyboardInterrupt, SystemExit):
		print '\n\nProcessing interrupted. Saving persistent file ...'
		write_index_position()

	write_index_position()



