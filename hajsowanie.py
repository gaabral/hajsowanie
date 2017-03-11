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
data = data[first_day:first_day+250]

max_profit = -100
max_profit_avg_size = 0
for avg_size in range(1,5):
	money = data[0]
	shares = 0
	sum_of_goods = []

	avg = []
	avg2 = []
	beg = 0

	last_buying_factor = -1

	for it in range(0, len(data)):
		#print it
		beg = max(0, it-avg_size)

		#avg.append(sum(data[beg:it+1])/ (it-beg+1))
		avg.append(avg_weights(data[beg:it+1]))

		cur_buying_factor = data[it] - avg[it]
		if last_buying_factor * cur_buying_factor < 0:
			if last_buying_factor < 0 and money > 0:
				shares = money / data[it]
				money = 0
				#print "k shares=", shares, "money=", money
			elif shares > 0:
				money = shares * data[it]
				shares = 0
				#print "s shares=", shares, "money=", money

		last_buying_factor = cur_buying_factor
		sum_of_goods.append(money + shares * data[it])

		#raw_input()
	cur_profit = (sum_of_goods[-1]-sum_of_goods[0])/sum_of_goods[0] * 100
	if cur_profit > max_profit:
		max_profit = cur_profit
		max_profit_avg_size = avg_size

print "max_profit =", max_profit, "at size", max_profit_avg_size

print "money at start", sum_of_goods[0]
print "money at end  ", sum_of_goods[-1]
print "profit        ", (sum_of_goods[-1]-sum_of_goods[0])/sum_of_goods[0] * 100,"%"

print "shares at start", data[0]
print "shares at end  ", data[-1]
print "profit        ", (data[-1]-data[0])/data[0] * 100,"%"

gp = Gnuplot.Gnuplot()
g_data = Gnuplot.Data(range(0, len(data)), data, with_="linespoints lt rgb 'red'")
g_data2 = Gnuplot.Data(range(0, len(avg)), avg, with_="lines lt rgb 'blue'")
#g_data3 = Gnuplot.Data(range(0, len(avg2)), avg2, with_="lines lt rgb 'green'")
g_data3 = Gnuplot.Data(range(0, len(sum_of_goods)), sum_of_goods, with_="lines lt rgb 'green'")
gp.plot(g_data, g_data2, g_data3)

raw_input()



