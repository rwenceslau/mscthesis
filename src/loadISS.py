__author__ = 'rodrigowenceslau'

fileISS = '../Dados/iss/iss.csv'

# Check if CNAE string is really a number.
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_date(s):
	if "/" in s:
		return True
	else:
		return False

def read_iss():

	issEntities = {}
	issCategoryCounter = 0		# Number of categories in ISS data.
	issCategories = []			# Categories id's in ISS data.
	issCounter = 0
	# Open and load ISS data.
	with open(fileISS) as iss:
		next(iss)
		for line in iss:
			columns = line.split(';')
			#placeId = int(columns[0].strip("\""))							# ISS internal ID.
			#pu.db
			placeDescription = columns[1].strip("\"")						# Address description (St., Ave., etc.).
			placeName = columns[2].strip("\"")								# Address name.
			#placeNumber = columns[3].strip("\"")							# Address number.
			#placeComplement = columns[4].strip("\"")						# Address complement.
			#address = placeDescription+' '+placeName+' '+placeNumber		# Making the whole address as one variable.
			address = placeDescription+' '+placeName
			neighborhoodName = columns[6].strip("\"")						# Neighborhood/Region name.
			mainCNAE = columns[7].strip("\"")								# First CNAE.
			#mainCNAE = mainCNAE[:-5]										# Just getting the first two digits of CNAE.

			if is_number(mainCNAE):		# Avoids wrong data errors.
				int(mainCNAE)
				if not mainCNAE in issCategories:
					issCategories.append(mainCNAE)
					issCategoryCounter += 1

			startDate = columns[8].strip("\"")								# Company's activation date.

			if not is_date(columns[9]):
				secCNAE = columns[9].strip("\"")								# Secondary CNAE.
			else:
				secCNAE = ""

			#issEntities[placeId] = address, mainCNAE, secCNAE, startDate
			issEntities[issCounter] = address, mainCNAE, secCNAE, startDate
			#print issEntities[issCounter]
			issCounter += 1
	return issEntities
