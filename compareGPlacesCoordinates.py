#	Compares GPlaces and ISS data searching for ambiguities and resolving it.
#	-----------------------------------------------------------

__author__ = 'rodrigowenceslau'

from geopy.distance import vincenty
import pudb
import csv

persistenceIndexFile = 'persistentIndexes'
proximityThreshold = 150
filterLevel = 7
updateFrequency = 100
#indexGplaces = 0
#indexISS = 0
#hits = 0
hitCNAEStats = {}		# Counts the CNAE categories which got hit.
hitPlaceStats = {}		# Stores the places which got hit.


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

# Writes CNAE and Places stats to a external csv file.
def write_stats_csv():

	writer = csv.writer(open('placesHit.csv', 'wb'))
	for key, value in hitPlaceStats.items():
   		writer.writerow([key, value])

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
	previousPlaceName = '0'
	savingCounter = 0
	
	with open('matchsByCategory', 'a') as matchFile, open('nonMatchsByCategory', 'a') as nonMatchFile:
		for i in xrange(indexGplaces, len(gPlacesEntities.keys())):

			if savingCounter == updateFrequency:
				print 'Updating Matching File ...'
				write_index_position()
				savingCounter = 0
				print 'Updated!'

			gplacesEntry = gPlacesEntities[i]
			#print gplacesEntry
			# Comparing each entry from GPlaces with ISS data, trying to get a match between DBs.
			#for gplacesEntry, gplacesValues in gPlacesEntities.iteritems():
			#print gplacesValues
			placeName = str(gplacesEntry[0])
			#print placeName, previousPlaceName
			if placeName is not previousPlaceName:
				previousPlaceName = placeName
				gp_coordX = float(gplacesEntry[2])
				#print gp_coordX
				gp_coordY = float(gplacesEntry[1])
				#print gp_coordY
				gpCoord = (gp_coordX, gp_coordY)

				#print "Current entry: {}, {}".format(placeName, gp_coordX, gp_coordY)

				gplacesCNAE = gplacesEntry[-1]

				global indexGplaces
				indexGplaces = i
				hadMatch = 0

				for j in xrange(0, len(issEntities.keys())):
					if hadMatch:
						break
					issEntry = issEntities[j]
				#for issEntry, issValues in issEntities.iteritems():
					#print issEntry[1]
					iss_coordX = float(issEntry[1])
					#print iss_coordX
					iss_coordY = float(issEntry[2])
					#print iss_coordY
					issCoord = (iss_coordX, iss_coordY)

					issMainCNAE = issEntry[0]
					#print issMainCNAE
					#issSecCNAE = issEntry[2]
					#print issSecCNAE
					#print "{} x {}".format(gplacesAddress, issAddress)
					proximity = vincenty(gpCoord, issCoord).meters
					#print gpCoord, issCoord
					#print proximity
					if proximity <= proximityThreshold:
						#pudb.set_trace()
						#print "Candidate detected!"
						#print gplacesCNAE
						#print issMainCNAE
						#print issSecCNAE	
						#if issMainCNAE in gplacesCNAE or issSecCNAE in gplacesCNAE:		# Checks if the activities are the same. The algorithm
						for entry in gplacesCNAE:
							if issMainCNAE[:filterLevel] in entry:							# Filter tolerance level.
								print "Proximity: ", proximity
								print "HIT!"												# considers the entities the same if CNAE and address are the same.
								global hits
								hits += 1
								hadMatch = 1
								print "MATCH: {} {}".format(placeName, gplacesCNAE)
								print "ISS CNAE: ", issMainCNAE
								matchFile.write(issMainCNAE+";"+";"+placeName+"\n")
								hitPlaceStats[placeName] = issMainCNAE, gpCoord
								print "Place added to stats."
								
			
					global indexISS
					indexISS = j

				if not hadMatch:
						for cnae in gplacesCNAE:
							nonMatchFile.write(cnae+";")
						nonMatchFile.write("\n")
			
			savingCounter += 1			

		write_index_position()
		write_stats_csv()



