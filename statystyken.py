#wlaze do mst z tyciacem plikow, losuje x plikow, wypisujesz ich nazwy
import os
from random import randint
import csv
from hajsowanie import funduszowy_demon 
import Gnuplot

array = os.listdir("mstfun")
indexes = set()
first_day = 100
days = 50
srednia_suma = 0
for i in range(0,100):
	while len(indexes) < 5:
		x = randint(0, len(array)-1)
		indexes.add(x)
	suma = 0 
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
		wynik = funduszowy_demon(data, 100, 3)
		wynik_prosty = data[-1] - data[0]
		#print array[it], wynik	
		g_data.append(Gnuplot.Data(range(0, len(data)), data, with_="lines lt rgb 'red'"))
		suma += wynik
		suma_prosta += wynik_prosty
	srednia_suma += suma
print 'sredni wynik= ', srednia_suma/100
#print 'suma =',suma
#print 'suma prosta =', suma_prosta
#na wykresie ostatnia iteracja
gp = Gnuplot.Gnuplot()
gp.plot(g_data[0], g_data[1], g_data[2], g_data[3], g_data[4])

raw_input()

