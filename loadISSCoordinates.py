__author__ = 'rodrigowenceslau'

fileISS = '../Dados/iss/iss_co.csv'

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

invalidChars = ['\n', '']
def read_iss():

	issEntities = {}
	issCounter = 0
	# Open and load ISS data.
	with open(fileISS) as iss:
		next(iss)
		for line in iss:
			columns = line.split(';')
			mainCNAE = columns[0]
			coord_x = columns[-1]
			coord_y = columns[-2]
			coord_x = coord_x[:-1]

			if coord_x not in invalidChars or coord_y not in invalidChars:
				issEntities[issCounter] = mainCNAE, coord_x, coord_y
				#print issEntities[issCounter]
				issCounter += 1
	return issEntities
