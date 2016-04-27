#	Compares GPlaces and ISS data searching for ambiguities and resolving it.
#	-----------------------------------------------------------

__author__ = 'rodrigowenceslau'

from nltk.metrics import edit_distance

persistenceIndexFile = 'persistentIndexes'
streetIndicators = ['Rua', 'Avenida', 'Pra\xc3a']
similarityThreshold = 4
#indexGplaces = 0
#indexISS = 0
#hits = 0

def check_string_for_street(s):
	for indicators in streetIndicators:
		if indicators in s:
			return True

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
	indexFile.close()

def write_index_position():

	with open(persistenceIndexFile, 'w') as indexFile:
		indexFile.write('{} {} {} '.format(indexGplaces, indexISS, hits))
	indexFile.close()

def compare_gplaces_iss(gPlacesEntities, issEntities):

	read_index_position()

	try:
		for i in range(indexGplaces, len(gPlacesEntities.keys())):
			gplacesEntry = gPlacesEntities[i]
			print gplacesEntry
		# Comparing each entry from GPlaces with ISS data, trying to get a match between DBs.
		#for gplacesEntry, gplacesValues in gPlacesEntities.iteritems():
			#print gplacesValues
			placeName = str(gplacesEntry[0])
			streetName = str(gplacesEntry[1])

			if not check_string_for_street(streetName):		# If the field doesn't provide a valid street name,
				streetName = str(gplacesEntry[2])			    # it belongs to a commercial building, so the
															# information is in the next entry position.
			print indexGplaces
			#print streetName
			#print streetNumber, streetName
			#gplacesAddress = streetName + streetNumber
			gplacesAddress = streetName
			gplacesAddress = gplacesAddress.upper()
			#print gplacesAddress
			gplacesCNAE = gplacesEntry[-1]

			for j in range(indexISS, len(issEntities.keys())):
				issEntry = issEntities[j]
			#for issEntry, issValues in issEntities.iteritems():
				streetName = str(issEntry[0])
				#print streetName
				issAddress = streetName
				issMainCNAE = issEntry[2]
				issSecCNAE = issEntry[3]
				#print gplacesAddress, issAddress
				similarity = edit_distance(gplacesAddress, issAddress)
				#print similarity
				if similarity <= similarityThreshold:
					print "Candidate detected!"
					if issMainCNAE in gplacesCNAE:						# Checks if the activities are the same. The algorithm
						print "HIT!"									# considers the entities the same if CNAE and address are the same.
						global hits
						hits += 1
						print placeName, gplacesCNAE
						print issMainCNAE
					elif issSecCNAE in gplacesCNAE:
						print "HIT!"
						global hits 
						hits += 1
						print placeName, gplacesCNAE
						print issMainCNAE

				global indexISS
				indexISS = j
			global indexGplaces
			indexGplaces = i
	except (KeyboardInterrupt, SystemExit):
		print '\n\nProcessing interrupted. Saving persistent file ...'
		write_index_position()



