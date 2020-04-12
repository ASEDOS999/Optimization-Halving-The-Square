# -*- coding: utf-8 -*-

import threading

from Solvers import GradientMethods, Ellipsoids, HalvCube

def create_methods_dict(f, start_x_fgm, R_fgm, Q, eps, history):
	methods = dict()
	fgm = GradientMethods.FGM_external
	methods["FGM"] = lambda : fgm(f, start_x_fgm, R_fgm, Q, eps = eps, history = history)
	
	ellipsoids = Ellipsoids.delta_ellipsoid
	methods["Ellipsoids"] = lambda: ellipsoids(f, Q, eps = eps, history = history)
	
	dichotomy = HalvCube.Dichotomy(history = history)
	methods["Dichotomy"] = lambda: dichotomy.Halving(f, Q, eps)
	return methods
	
def method_comparison(methods = None):
	t = []
	for key in methods:
		t.append(threading.Thread(target = methods[key], name = key))
	for i in t:
		i.start()
	for i in t:
		i.join()

