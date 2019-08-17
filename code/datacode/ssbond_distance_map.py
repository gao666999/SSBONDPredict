# -*-coding:utf-8-*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from scipy.spatial.distance import pdist
import scipy.spatial.distance as ssd
import sys
import os

def convert_to_nxn_map(ssbonds_map):
	print(ssbonds_map.shape)
	errorcount = 0
	# Y = pdist(ssbonds_map, 'euclidean')
	ssbonds_distance_map = []#np.array([])
	pos = 0
	for smapi in range(len(ssbonds_map)):
		# print smapi
		# print ssbonds_map[smapi]
		try:
			#print(ssbonds_map[smapi])
			Y = pdist(ssbonds_map[smapi], 'euclidean')
			print(Y.shape,'yyyyyyyyyyyyyyyyyy')
			ssbonds_distance_map.append(ssd.squareform(Y))
			print(ssd.squareform(Y).shape)
			#ssbonds_distance_map.append(Y)
			# ssbonds_distance_map = np.append(ssbonds_distance_map,Y)
			# print Y.shape
		except ValueError:
			# print smapi
			# print ssbonds_map[smapi]
			errorcount += 1
			with open('ssbond_map_error.txt','a') as wf:
				wf.write(str(ssbonds_map[smapi]))
				wf.write('\n')
			
			for xyz in ssbonds_map[smapi]:
				if abs(len(xyz[0])-len(xyz[1])) <= 1:
					continue
				# print len(xyz[0]),len(xyz[1])
				if len(xyz[0]) > len(xyz[1]):
					pos = 0
				else:
					pos = 1
				# print pos
				temp = xyz[pos].split('-')
				if pos == 0:
					xyz[pos+2] = xyz[pos+1]
					if temp[0] == '':
						xyz[pos] = float('-'+temp[1])
						xyz[pos+1] = float('-'+temp[2])
					else:
						xyz[pos] = float(temp[0])
						xyz[pos+1] = float('-'+temp[1])
				else:
					if temp[0] == '':
						xyz[pos] = float('-'+temp[1])
						xyz[pos+1] = float('-'+temp[2])
					else:
						xyz[pos] = float(temp[0])
						xyz[pos+1] = float('-'+temp[1])
				# print ssbonds_map[smapi]
			with open('ssbond_map_correct_error.txt','a') as wcf:
				wcf.write(str(ssbonds_map[smapi]))
				wcf.write('\n')
				wcf.write('***************************************\n')
			Y = pdist(ssbonds_map[smapi], 'euclidean')
			#ssbonds_distance_map.append(ssd.squareform(Y))
			# print 'hi',ssd.squareform(Y).shape
			ssbonds_distance_map.append(Y)
			# ssbonds_distance_map = np.append(ssbonds_distance_map,Y)

	# print ssbonds_distance_map
	print('errorcount:',errorcount)
	print(len(ssbonds_distance_map))
	return ssbonds_distance_map

if __name__ == '__main__':
	args = sys.argv[1:]
	filename = args[0]
	name=filename.split('_')[0]
	#name = args[0].split('_')[1].split('.')[0]
	#name='positive'
	print(name)
	root_path = '/Users/dongxq/Desktop/SSBOND_supplement/rootpath30/'
	file=os.path.join(root_path,filename)
	ssbonds_map = np.load(file)
	ssbonds_map = ssbonds_map
	print(ssbonds_map.shape,'IIIIIIIII')
	ssbonds_distance_map = convert_to_nxn_map(ssbonds_map)
	print(ssbonds_distance_map[1])
	print(len(ssbonds_distance_map))
	np.save(root_path+'%s_distance.npy'%name,ssbonds_distance_map)
