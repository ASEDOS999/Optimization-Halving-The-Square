# -*- coding: utf-8 -*-

import sys
sys.path.append("/Tests_functions")

from time import time
import matplotlib.pyplot as plt
import numpy as np
import random
from test_functions import sinuses
from test_functions import quadratic_function as qf
from method_functions import main_solver
from method_functions import gradient_descent
import math

#Tests for iterations number
def num_iter_tests(epsilon):
	results = []
	num = 0
	Q = [0, 1, 0, 1]
	for i in np.linspace(1.1, 1.9, 5).tolist():
		for j in np.linspace(1.1, 1.9, 5).tolist():
			a = [[0.1, 0.1], [0.1, 0.1, 0.1]]
			m, n = 1, 2
			while m != -1:
				f = sinuses(a, [i, j])
				for eps in epsilon:
					solver = main_solver(f, Q, eps)
					solver.init_help_function(stop_func = 'true')
					N = solver.halving_square()
					results.append((N[1], eps, f.L))
				m, n = 1, 2
				while m != -1 and a[m][n] == 1:
					a[m][n] = 0.1
					n = n - 1
					if n < 0:
						m = m - 1
						if m > 0:
							n = 2
						else:
							n = 1
				a[max(m, 0)][n] *= 10
			num += 1
	plt.plot([math.log(i[2] / i[1] / math.sqrt(2), 2) for i in results], [i[0] for i in results], 'ro')
	plt.plot([0, 17], [0, 17], 'b')
	plt.title("Iterations number")
	plt.grid()
	plt.legend(('Tests functions', r'Line $N = \log \frac{La}{\sqrt{2}\epsilon}$'))
	plt.ylabel(r'$N$')
	plt.xlabel(r'$\log \frac{La}{\sqrt{2}\epsilon}$')
	plt.show()

#Сompetion: Gradient Descent vs New method
#Sinuses
def comparison_GD_HS_sinuses(epsilon):
	results = []
	num = 0
	Q = [0, 1, 0, 1]
	for i in np.linspace(1.1, 1.9, 5).tolist():
		for j in np.linspace(1.1, 1.9, 5).tolist():
			a = [[0.1, 0.1], [0.1, 0.1, 0.1]]
			m, n = 1, 2
			while m != -1:
				f = sinuses(a, [i, j])
				for eps in epsilon:
					m1 = time()
					res_1 = gradient_descent(f.calculate_function, [0, 1, 0, 1], f.gradient, eps, 0.25, f.min)
					m2 = time()
					solver = main_solver(f, Q, eps)
					solver.init_help_function(stop_func = 'true')
					res_2 = solver.halving_square()
					m3 = time()
					results.append((eps, res_1[1], res_2[1], m2 - m1, m3 - m2))
				m, n = 1, 2
				while m != -1 and a[m][n] == 1:
					a[m][n] = 0.1
					n = n - 1
					if n < 0:
						m = m - 1
						if m > 0:
							n = 2
						else:
							n = 1
				a[max(m, 0)][n] *= 10
			num += 1
	
	p = 1.05
	
	data = (len([i[0] for i in results
			 	if i[1] >= 0 and i[2] < 0]),
			len([i[0] for i in results
			 	if i[1] >= 0 and i[2] >= 0 and i[4] > p * i[3]]),
			len([i[0] for i in results
			 	if i[1] >= 0 and i[2] >= 0 and (1/p * i[3]) <= i[4] and i[4] <= (p * i[3])]),
			len([i[0] for i in results
			 	if i[1] >= 0 and i[2] >= 0 and i[4] < 1/p * i[3]]),
			len([i[0] for i in results
			 	if i[1] < 0 and i[2] >= 0]))
	ind = np.arange(5)
	width = 0.35
	p1 = plt.bar(ind, data, width)
	plt.grid()
	plt.ylabel('Number of tasks')
	plt.xticks(ind, ('T1', 'T2', 'T3', 'T4', 'T5'))
	plt.show()


#Quadratic functions
def comparison_GD_HS_QFunc(epsilon):
	results = []
	num = 0
	N = 1000
	n = 0
	while len(results) < 3 * N:
			n += 1
			param = np.random.uniform(-10, 10, 6)
			param[2] =  abs(param[2])
			f = qf(param)
			size_1, size_2 = random.uniform(0.5, 1), random.uniform(0.5, 1)
			x_1, y_1 = f.solution[0], f.solution[1]
			Q = [x_1 - (1-size_1), x_1 + (1+size_1), y_1 - (1-size_2), y_1 + (1+size_2)]
			for eps in epsilon:
				m1 = time()
				res_1 = gradient_descent(f.calculate_function, Q, f.gradient, eps, 0.25, f.min)
				m2 = time()
				solver = main_solver(f, Q, eps)
				solver.init_help_function(stop_func = 'const_est')
				res_2 = solver.halving_square()
				m3 = time()
				results.append((eps, res_1[1], res_2[1], m2 - m1, m3 - m2))
	
	p = 1.05
	
	data = (len([i[0] for i in results
			 	if i[1] >= 0 and i[2] < 0]),
			len([i[0] for i in results
			 	if i[1] >= 0 and i[2] >= 0 and i[4] > p * i[3]]),
			len([i[0] for i in results
			 	if i[1] >= 0 and i[2] >= 0 and (1/p * i[3]) <= i[4] and i[4] <= (p * i[3])]),
			len([i[0] for i in results
			 	if i[1] >= 0 and i[2] >= 0 and i[4] < 1/p * i[3]]),
			len([i[0] for i in results
			 	if i[1] < 0 and i[2] >= 0]),
			len([i[0] for i in results
			 	if i[1] < 0 and i[2] < 0]))
	ind = np.arange(6)
	width = 0.35
	p1 = plt.bar(ind, data, width)
	plt.title('QF')
	plt.grid()
	plt.ylabel('Number of tasks')
	plt.xticks(ind, ('T1', 'T2', 'T3', 'T4', 'T5', 'T6'))
	plt.show()

if __name__ == "__main__":
	eps = [0.1**(i) for i in range(7)]
	num_iter_tests(eps)
	comparison_GD_HS_sinuses(eps)
	comparison_GD_HS_QFunc(eps)