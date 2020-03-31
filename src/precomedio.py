import csv
from nltk.metrics import edit_distance

bairros = {}
nomesBairros = []

def check_similarity_and_insert(nomeBairro, precomedio, coord_x, coord_y):

	if len(nomesBairros) == 0:
		nomesBairros.append(nomeBairro)
		bairros[nomeBairro] = coord_x, coord_y, precomedio

	else:
		inserted = False

		for bairro in nomesBairros:
			if edit_distance(bairro, nomeBairro) <= 2:
				#print bairro
				newAvg = (bairros[bairro][2] + precomedio) / 2
				#bairros[bairro][2] = newAvg
				#nomesBairros.append(nomeBairro)
				bairros[bairro] = coord_x, coord_y, newAvg
				inserted = True

		if not inserted:
			bairros[nomeBairro] = coord_x, coord_y, precomedio
			nomesBairros.append(nomeBairro)	

				
print 'Reading input file ...'
with open('../Dados/imoveis/precoabs.csv', 'r') as precomedio:
	tableReader = csv.reader(precomedio, delimiter = ',')
	next(tableReader)
	for row in tableReader:
		nomeBairro = row[0]
		precomedio = float(row[1])
		coord_x = row[2]
		coord_y = row[3]
		check_similarity_and_insert(nomeBairro, precomedio, coord_x, coord_y)

#print len(bairros.keys())
#print len(nomesBairros)
#print nomesBairros

print 'Writing output file ...'
with open('../Dados/imoveis/precoabsnovo.csv', 'w') as precomedioW:
	for key, value in bairros.items():
		precomedioW.write('{};{};{};{}\n'.format(key, value[0], value[1], value[2]))

print 'Done!'