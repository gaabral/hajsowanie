import csv
import Gnuplot
from math import exp

def avg_weights(arr):
	sum_weight = 0
	weight = 0
	for it in range(0, len(arr)):
		sum_weight += (exp(it)+1)*arr[it]
		weight += (exp(it)+1)

	return sum_weight/weight

data = []

with open('pko.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		if row[0] != "<TICKER>":
			data += [float(row[5])]
first_day = 0
data = data[first_day:first_day+350]



money = data[0]
shares = 0
sum_of_goods = []
avg = []
avg_size = 3

for it in range(0, len(data)):
	beg = max(0, it-(2*avg_size))
	cur = max(0, it-avg_size)

	avg.append(sum(data[beg:it+1])/(it+1-beg))

	if it > 0:
		if (avg[cur]-avg[cur-1])/avg[cur-1] > 0.002 and money > 0:
			shares = money / data[it]
			money = 0
		elif (avg[cur]-avg[cur-1])/avg[cur-1] < 0.001 and shares > 0:
			money = shares * data[it]
			shares = 0

	sum_of_goods.append(money + shares * data[it])


gp = Gnuplot.Gnuplot()
g_data = Gnuplot.Data(range(0, len(data)), data, with_="linespoints lt rgb 'red'")
g_data2 = Gnuplot.Data(range(0, len(avg)), avg, with_="lines lt rgb 'blue'")
#g_data3 = Gnuplot.Data(range(0, len(avg2)), avg2, with_="lines lt rgb 'green'")
g_data3 = Gnuplot.Data(range(0, len(sum_of_goods)), sum_of_goods, with_="lines lt rgb 'green'")
gp.plot(g_data, g_data2, g_data3)

raw_input()

def funduszowy_demon(data, money, avg_size):
	cur_money = money
	shares = 0

	last_buying_factor = -1

	for it in range(0, len(data)):
		beg = max(0, it-avg_size)

		avg = avg_weights(data[beg:it+1])

		cur_buying_factor = data[it] - avg
		if last_buying_factor * cur_buying_factor < 0:
			if last_buying_factor < 0 and cur_money > 0:
				shares = cur_money / data[it]
				cur_money = 0
			elif shares > 0:
				cur_money = shares * data[it]
				shares = 0

		last_buying_factor = cur_buying_factor

	return cur_money + shares * data[-1] -money

#print funduszowy_demon(data, 100, 3)



def statystyki_demona(data, money, avg_size):
	statsy = {}
	ostatni_zakup = 0
	hajs_ostatni_zakup = 0
	cur_money = money
	shares = 0

	last_buying_factor = -1

	for it in range(0, len(data)):
		beg = max(0, it-avg_size)

		avg = avg_weights(data[beg:it+1])

		cur_buying_factor = data[it] - avg
		if last_buying_factor * cur_buying_factor < 0:
			if last_buying_factor < 0 and cur_money > 0:
				shares = cur_money / data[it]
				ostatni_zakup = it
				hajs_ostatni_zakup = cur_money
				cur_money = 0
			elif shares > 0:
				cur_money = shares * data[it]
				shares = 0
				dlugosc_transakcji = it - ostatni_zakup
				zysk = (cur_money - hajs_ostatni_zakup)/hajs_ostatni_zakup * 100
				if statsy.get(dlugosc_transakcji) == None:
					statsy[dlugosc_transakcji] = (1,zysk)
				else:
					local_val = statsy[dlugosc_transakcji]
					statsy[dlugosc_transakcji] = (local_val[0]+1, local_val[1]+zysk)

		last_buying_factor = cur_buying_factor

	return statsy

