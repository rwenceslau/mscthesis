#	Reads foursquare places data.
#	-----------------------------------------------------------

__author__ = 'rodrigowenceslau'
import sys
reload(sys)
import json

sys.setdefaultencoding('utf-8') # ou Latin1 ou cp1552
foursquareInput = '../Dados/foursquare/foursquare_coletacompleta/foursquare_coleta.json'
foursquareData = {}
streetIndicators = ['Rua', 'Avenida', 'Av.', 'R.']

# Checks if a value is an address.
def check_string_for_street(s):

	for indicator in streetIndicators:
		if indicator in s:
			return True

def load_foursquare():
	entryId = 0

	with open(foursquareInput) as file:
		for line in file:
			include = 0
			line = line.split(';')
			data = json.loads(line[1])
			#print data
			#print entryId
			if data['response']:
				if data['response']['venues']:
					response = json.loads(json.dumps(data['response']['venues'][0]))
					placeName = response["name"]
					if response["location"]["formattedAddress"]:
						address = response["location"]['formattedAddress'][0]
						#print address
						addressTreat = address.split(',')
						address = addressTreat[0]
						#print address
						if check_string_for_street(address):
							include = 1				
						#print placeName, address
						if response['categories']:
							category = response['categories'][0]['shortName']
							# Only include if entry has a valid address.
							if include:
								foursquareData[entryId] = placeName, address, category
								#print entryId
								#print '{}, {} - {}'.format(placeName, address, category)
			entryId = entryId + 1
	return foursquareData