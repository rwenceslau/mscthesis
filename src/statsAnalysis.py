__author__ = 'rodrigowenceslau'
import operator

nmCategories = {}
mCategories = {}
<<<<<<< HEAD
mNames = []

#Counts unique matches by business name.
# with open('Results1/matchsByCategoryFull', 'r') as matchs:
# 	for row in matchs:
# 		tokens = row.split(';')
# 		businessName = tokens[-1]

# 		if businessName not in mNames:
# 			mNames.append(businessName)

# 	print  'Unique Matchs #: {}'.format(len(mNames))

with open('Results1/nonMatchsByCategoryFull', 'r') as nonMatchs:

	previousRow = ''
	for row in nonMatchs:
		if row is not previousRow:
			tokens = row.split(';')
			tokens = tokens[:-1]
			
			for entry in tokens:
				if entry not in nmCategories.keys():
					nmCategories[entry] = 1
				else:
					nmCategories[entry] += 1
		previousRow = row
=======

with open('nonMatchsByCategoryFull', 'r') as nonMatchs:
	for row in nonMatchs:
		tokens = row.split(';')
		tokens = tokens[:-1]
		
		for entry in tokens:
			if entry not in nmCategories.keys():
				nmCategories[entry] = 1
			else:
				nmCategories[entry] += 1
>>>>>>> 8b58769fa814d00954d6d88cd777b448c476b773

sortedNonMatchs = sorted(nmCategories.items(), key=operator.itemgetter(1), reverse = True)

#for key, value in sortedNonMatchs:
#	print key, value

print 'Non Matchs Top Categories'
<<<<<<< HEAD
for i in range (0, 8):
		print sortedNonMatchs[i]

with open('Results1/matchsByCategoryFull', 'r') as matchs:

	previousRow = ''
	for row in matchs:
		if row is not previousRow:
			tokens = row.split(';')
			tokens = tokens[:1]
			
			for entry in tokens:
				if entry is not '':
					if entry not in mCategories.keys():
						mCategories[entry] = 1
					else:
						mCategories[entry] += 1
		previousRow = row
=======
for i in range (0, 5):
	print sortedNonMatchs[i]

with open('matchsByCategoryFull', 'r') as matchs:
	for row in matchs:
		tokens = row.split(';')
		tokens = tokens[:-2]
		
		for entry in tokens:
			if entry not in mCategories.keys():
				mCategories[entry] = 1
			else:
				mCategories[entry] += 1
>>>>>>> 8b58769fa814d00954d6d88cd777b448c476b773

sortedMatchs = sorted(mCategories.items(), key=operator.itemgetter(1), reverse = True)

#for key, value in sortedMatchs:
#	print key, value

print '\nMatchs Top Categories'
for i in range (0, 5):
	print sortedMatchs[i]