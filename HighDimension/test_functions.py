#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
class QuadraticFunction:
	def __init__(self, n = None, C = 0, mu = 0.1, L_max = 1, L_min = 0.1, way = 'random'):
		if n is None:
			n = 100
		if way == 'random':
			A = np.random.uniform(-1, 1, (n,n))
			A = A.T.dot(A)+ np.eye(n)*C
		if way == 'control':
			a = np.random.uniform(L_min, L_max, (n,))
			a[np.argmax(a)] = L_max
			a[np.argmin(a)] = L_min
			Q, _ = np.linalg.qr(np.random.uniform(-1, 1, (n,n)))
			L = np.diag(np.array(a))
			A = Q@L@Q.T
		self.A_ = A
		self.eig_value = np.linalg.eig(A)[0]
		self.eig_value.sort()
		b = np.random.uniform(-10, 10, (n,))

		self.A = A
		self.b = b
		self.n = n
		self.L_full_grad = self.eig_value[-1]
		self.mu_full = self.eig_value[0]
		self.L, self.mu, self.grad = [], [], []
		self.grad = [lambda x:self.get_grad(x)[ind] for ind in range(self.n)]
		print(self.L_full_grad/self.mu_full, self.mu_full)
		self.get_params()
		
	def get_params(self):
		for ind in range(self.n):
			A = np.delete(np.delete(self.A, ind, 0), ind, 1)
			eig = np.linalg.eig(A)[0]
			eig.sort()
			#self.mu.append(self.mu_full)
			#self.L.append((self.L_full_grad, self.L_full_grad))
			self.mu.append(eig[0])
			self.L.append((2*np.linalg.norm(self.A[ind,:]), 2 * eig[-1])) 

	def func_value(self, x):
		#return np.linalg.norm(self.A_.dot(x) - self.b)**2
		return x.T@self.A@x - 2*self.b.T@x
	
	def get_grad(self, x, without = None, only_ind = None):
		g = list()
		if without is None and only_ind is None:
			return 2 *self.A.dot(x) - 2 * self.b
		if not only_ind is None:
			for ind in only_ind:
				g.append(2*self.A[ind,:].dot(x) - 2*self.b[ind])
			return np.array(g)
		if without is None:
			without = []
		indexes = [i for i,_ in enumerate(x) if not i in without]
		for ind in indexes:
			g.append(2*self.A[ind,:].dot(x) - 2*self.b[ind])
		return np.array(g)

	def get_square(self):
		lim = 2 * np.linalg.norm(self.b)/self.mu_full
		return [[-lim, lim] for i in range(self.n)]

	def get_start_point(self, ind, new_Q):
		b = np.delete(self.b+self.A[ind,:], ind)
		A = np.delete(np.delete(self.A, ind, 0), ind, 1)
		eig = np.linalg.eig(A)[0]
		eig.sort()
		lmin = eig[0]
		lim = 2 * np.linalg.norm(b)/lmin
		s = 0
		for i in new_Q:
			if type(i)==type(list()):
				s += (i[0]-i[1])**2
		return np.zeros((self.n-1,)), lim
		
