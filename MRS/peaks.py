#! /usr/bin/python

# functions for detecting peaks and modeling 

import os
import numpy as np
import scipy
import matplotlib.pyplot as plt
import sys
from scipy.ndimage.filters import maximum_filter1d
from pylab import *
import array
import scipy.linalg as la
from MRS.utils import *

def lorentzian(l,w,x):
	"""
	the lorentzian function used by Soher 1996

	creates a Lorentzian lineshape centered at w
	"""
        return l/(l**2+(x-w)**2)

def conv_lorentz(x_idx,data):
	"""
	convolve with lorentz function
	
	Parameters
	----------
	x_idx = where to place lorentzian lineshapes (e.g. timepoints), 
	data = Y (e.g. raw spectra)
	
	"""

	# for each unique peak found before, construct delta function
	deltas=np.zeros((len(x_idx),len(data)))
	for i in range(len(x_idx)):
		deltas[i][int(x_idx[i])]=1 # set delta at index of peak

	## plot to check if lorentzians coincide with peaks
	figure(2)
	# first plot peak locations on new fig
	for idx in range(len(x_idx)): # plot location of each peak with red circle
		plot(x_idx[idx],data[int(x_idx[idx])], 'ro')

	# convolve with lorentzian
	X = np.zeros((len(x_idx),len(data)))
	for i in range(len(x_idx)):
		lor = array.array('f')
		for j in range(len(data)):
			lor.append(lorentzian(0.4,int(x_idx[i]),j)) # first param is arbitrary, 2nd is the mean
		X[i]=lor # create new row for each peak
		plot(X[i])
	return X



def peakdetect(data):
	"""
	detects peaks in data
	"""
	# if using numpy array, replace with array.array	
	tmp = array.array('f')
	for idx in range(len(data)):
		tmp.append(data[idx])
	data = tmp 

	local_max = maximum_filter1d(data,100)
	unique_max = list(set(local_max))
	# find index of maxima in data
	peak_x=array.array('f') 
	for idx in range(len(unique_max)): # for every max, find the index
		peak_x.append(data.index(unique_max[idx]))
	# if indices are very close together, take the max of that cluster
	maxmax = array.array('f') # maxmax = maximum of (very) local maxima
	for idx in range(len(peak_x)): # for every max, find clusters of points less than 1/25 of range apart
		cluster=array.array('f')
		[cluster.append(peak_x[i]) for i in range(len(peak_x)) if peak_x[idx]-len(data)/25<peak_x[i]<peak_x[idx]+len(data)/25] 
		max_x=array.array('f')
		for idx in range(len(cluster)): # for every cluster, find the values at each index
			max_x.append(data[int(cluster[idx])])
		maxmax.append(max(max_x)) # find the maximum in each cluster and add to array
	uniquemaxmax = list(set(maxmax))
	unique_peak=array.array('f')
	for idx in range(len(uniquemaxmax)): # find indices of peaks that "survived"
		unique_peak.append(data.index(uniquemaxmax[idx]))
	return unique_peak

def peak_nearest(point, peaks):
	"""
	given set of local maxima, finds the INDEX of the one nearest given point (in ppm)
	
	Parameters
	----------
	point: in ppm, where you want to find the nearest peak
	peaks: locations of local maxima (also in ppm)

	"""
	diff = array.array('f')
	for i in range(len(peaks)):
		diff.append(abs(peaks[i] - point))
	closest = min(diff)
	if closest>0.05:
		print 'Difference in ppm was > 0.05: %f' % (closest)
	# find index of closest peak
	idx = diff.index(closest)
	print str(peaks[idx]) + 'ppm'
	return idx # returns index of peak in the array you gave it
	#return peaks[idx] # return position of peak in ppm