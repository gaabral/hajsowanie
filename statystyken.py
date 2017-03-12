#wlaze do mst z tyciacem plikow, losuje x plikow, wypisujesz ich nazwy
import os
from random import randint
import csv
from hajsowanie import funduszowy_demon, statystyki_demona
import Gnuplot

array = os.listdir("mstfun")
indexes = set()
first_day = 100
days = 50


while len(indexes) < 50:
	x = randint(0, len(array)-1)
	indexes.add(x)
suma = {} 
suma_prosta = 0 
g_data = []
for it in indexes:	
	data = []
	with open('mstfun/' + array[it],'r') as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] != "<TICKER>":
				data += [float(row[5])]
	data = data[first_day:first_day+days]
	wynik = statystyki_demona(data, 100, 3)
	#wynik_prosty = data[-1] - data[0]
	#print array[it], wynik	
	g_data.append(Gnuplot.Data(range(0, len(data)), data, with_="lines lt rgb 'red'"))
	for key in wynik.keys():
		if suma.get(key) == None:
			suma[key] = wynik[key]
		else:
			local_val = suma[key]
			suma[key] = (local_val[0]+wynik[key][0], local_val[1]+wynik[key][1])	
	
	#suma_prosta += wynik_prosty
	
#print 'suma =',suma
#print 'suma prosta =', suma_prosta
lista_ilosci_wystapien = []
lista_zyskow = []
for it in range (0, max(suma.keys())):
	lista_ilosci_wystapien.append(suma.get(it, (0,0))[0])
	lista_zyskow.append(suma.get(it, (0,0))[1])
	

gp = Gnuplot.Gnuplot()
g_data = Gnuplot.Data(range(0, len(lista_ilosci_wystapien)), lista_ilosci_wystapien, with_="linespoints lt rgb 'green'")
g_data2 = Gnuplot.Data(range(0, len(lista_zyskow)), lista_zyskow, with_="linespoints lt rgb 'blue'")
gp.plot(g_data, g_data2)

raw_input()

