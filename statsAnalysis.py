__author__ = 'rodrigowenceslau'
import operator

nmCategories = {}
mCategories = {}

with open('nonMatchsByCategoryFull', 'r') as nonMatchs:
	for row in nonMatchs:
		tokens = row.split(';')
		tokens = tokens[:-1]
		
		for entry in tokens:
			if entry not in nmCategories.keys():
				nmCategories[entry] = 1
			else:
				nmCategories[entry] += 1

sortedNonMatchs = sorted(nmCategories.items(), key=operator.itemgetter(1), reverse = True)

#for key, value in sortedNonMatchs:
#	print key, value

print 'Non Matchs Top Categories'
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

sortedMatchs = sorted(mCategories.items(), key=operator.itemgetter(1), reverse = True)

#for key, value in sortedMatchs:
#	print key, value

print '\nMatchs Top Categories'
for i in range (0, 5):
	print sortedMatchs[i]