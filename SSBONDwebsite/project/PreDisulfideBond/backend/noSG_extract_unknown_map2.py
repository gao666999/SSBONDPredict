# -*-coding:utf-8 -*-
############################################################
# This python code can extract raw pdb ssbond_distance 
# map. It's means that didn't add any mutation.
# 
#
#
#
#
#
############################################################
# from __future__ import unicode_literals
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import time
import numpy as np
import sys
from . import ssbond_distance_map as sdm
import math

remove_pairs = open('small_ca_remove.txt','w')
def compare_CA_distance(A_CA,B_CA,nameA,nameB):
	sumCA = 0
	for xyz in range(3):
		sumCA += pow((float(A_CA[xyz])-float(B_CA[xyz])), 2)
	distance = math.sqrt(sumCA)
	if 3<distance < 7:
		return True
	else:
		remove_pairs.write(nameA+','+nameB+':'+str(distance) +'\n')
		return False

def exmain_mol_list(mol_list,line_temp):
	if mol_list[0]!=[] and mol_list[1]!=[] and mol_list[2]!=[] and mol_list[3]!=[] and mol_list[4]!=[]:
		# flag_mol = True
		# mol_id = line_temp[5]

		return True,line_temp[3]+line_temp[4]+line_temp[5]
	else:
		# print('no,no mol')
		return False,line_temp[3]+line_temp[4]+line_temp[5]

def correct_xyz(line_temp):
	# print len(line_temp[6]),len(line_temp[7])
	if len(line_temp[5])-len(line_temp[6]) > 3:
		pos = 6
	else:
		pos = 7
	# print(pos)
	temp = line_temp[pos].split('-')
	# if len(temp) == 1:
		# print("wrong line!")
	# print temp
	# print line_temp
	x=0
	y=0
	z=0
	if pos == 6:
		z = float(line_temp[pos+1])
		if temp[0] == '':
			x = float('-'+temp[1])
			y = float('-'+temp[2])
		else:
			x = float(temp[0])
			y = float('-'+temp[1])
	else:
		if temp[0] == '':
			x = float('-'+temp[1])
			y = float('-'+temp[2])
		else:
			x = float(temp[0])
			y = float('-'+temp[1])
	return x,y,z
		
		
def find_map_element(filename):
	f = open(filename,'r')
	mol_map_list = []
	flag_mol = False
	mol_id = None
	mol_id_list = []
	mol_name_temp = None
	last_mol = None
	mol_type_list = []
	count = 0
	lines = f.readlines()
	break_count = 0
	for i in range(len(lines)):
		# line = lines[i]
		break_count += 1
		line_temp = lines[i].split()
		
		
		if line_temp[0] != 'ATOM':
			continue
		if line_temp [3] == 'PRO':
			continue
		# print(lines[i])
		# print(break_count)
		# if i == 18:
		# 	break
		
		if line_temp[0] == 'ENDMDL' :
			break
		# print(line_temp)
		if len(line_temp[2]) == 7:
			mol_pos = 4
			line_temp3 = line_temp[2][3:]
			line_temp[2] = line_temp[2][:3]
			line_temp.insert(3,line_temp3)
			# with open('line_temp.txt','a') as wlf:
			# 	wlf.write('pdb name: '+pdb +'\n')
			# 	wlf.write(str(line_temp) +'\n')
		if len(line_temp[4]) == 5:
			line_temp5 = line_temp[4][1:]
			line_temp[4] = line_temp[4][0]
			line_temp.insert(5,line_temp5)
			# with open('line_temp.txt','a') as wlf:
			# 	wlf.write('pdb name: '+pdb +'\n')
			# 	wlf.write(str(line_temp) +'\n')

		if line_temp[0] == 'ATOM' and mol_name_temp == None:
			mol_name_temp = line_temp[3]+line_temp[4]+line_temp[5]
			mol_list = [ [] for i in range(5)]
		elif line_temp[0] == 'ATOM' and mol_name_temp!=line_temp[3]+line_temp[4]+line_temp[5]:

			mol_name_temp = line_temp[3]+line_temp[4]+line_temp[5]
			mol_list = [ [] for i in range(5)]
			# count += 1
			
		if abs(len(line_temp[6])-len(line_temp[7])) <= 3:
			# print('hi')
			if line_temp[2] == 'N' and mol_list[0] ==[]:
				mol_list[0].append(float(line_temp[6]))
				mol_list[0].append(float(line_temp[7]))
				mol_list[0].append(float(line_temp[8]))
				
				flag_mol,mol_id = exmain_mol_list(mol_list,line_temp)
			elif line_temp[2] =='CA' and mol_list[1] == []:
				mol_list[1].append(float(line_temp[6]))
				mol_list[1].append(float(line_temp[7]))
				mol_list[1].append(float(line_temp[8]))
				
				flag_mol,mol_id = exmain_mol_list(mol_list,line_temp)
			elif line_temp[2] =='C' and mol_list[2] == []:
				mol_list[2].append(float(line_temp[6]))
				mol_list[2].append(float(line_temp[7]))
				mol_list[2].append(float(line_temp[8]))
				flag_mol,mol_id = exmain_mol_list(mol_list,line_temp)
			elif line_temp[2] =='O' and mol_list[3] == []:
				mol_list[3].append(float(line_temp[6]))
				mol_list[3].append(float(line_temp[7]))
				mol_list[3].append(float(line_temp[8]))
				
				flag_mol,mol_id = exmain_mol_list(mol_list,line_temp)
			elif line_temp[2] =='CB' and mol_list[4] == []:
				mol_list[4].append(float(line_temp[6]))
				mol_list[4].append(float(line_temp[7]))
				mol_list[4].append(float(line_temp[8]))
				
				flag_mol,mol_id = exmain_mol_list(mol_list,line_temp)

		else:
				
			x,y,z=correct_xyz(line_temp)
			if line_temp[2] == 'N' and mol_list[0] == []:
				mol_list[0].append([x,y,z])
				flag_mol,mol_id = exmain_mol_list(mol_list,line_temp)
				# print mol_list[0]
			elif line_temp[2] =='CA' and mol_list[1] == []:
				mol_list[1].append([x,y,z])
				flag_mol,mol_id = exmain_mol_list(mol_list,line_temp)
				# print mol_list[1]
			elif line_temp[2] =='C' and mol_list[2] == []:
				mol_list[2].append([x,y,z])
				flag_mol,mol_id = exmain_mol_list(mol_list,line_temp)
				# print mol_list[2]
			elif line_temp[2] =='O' and mol_list[3] == []:
				mol_list[3].append([x,y,z])
				flag_mol,mol_id = exmain_mol_list(mol_list,line_temp)
				# print ssbond_mol_map[num][3]
			elif line_temp[2] =='CB' and mol_list[4] == []:
				mol_list[4].append([x,y,z])
				flag_mol,mol_id = exmain_mol_list(mol_list,line_temp)

				
		# print(mol_list)
		# print(flag_mol,line_temp[3]+line_temp[4]+line_temp[5])
		if flag_mol == True:
			# print(flag_mol)
			# print(line_temp[0])
			# print(line_temp[3]+line_temp[4])
			mol_map_list.append(mol_list)
			mol_id_list.append(mol_id)
			mol_type_list.append(line_temp[3]+line_temp[4]+line_temp[5])
			flag_mol = False
			
			
	# print('test',len(mol_map_list),len(mol_id_list))
	# print(mol_id_list)
	# print(mol_type_list)
	# print(count)

	return mol_map_list,mol_id_list,mol_type_list

def make_ssbond(map_list, map_id, mol_type_list):
	if len(map_list) != len(map_id):
		# print('map list length is not equal to map id list!')
		sys.exit()

	possible_ssbond = []
	possible_ssbond_id = []
	for i in range(len(map_list)):
		for j in range(len(map_list)):
			if i == j:
				continue
			elif mol_type_list[i][1:] == mol_type_list[j][1:]:
				continue
			else:
				# print(i,j)
				# a = map_list[i].extend(map_list[j])
				# print(a)
				
				temp = map_list[i][:]
				# temp.append(map_list[i])
				temp.extend(map_list[j])
				# print(temp)
				# print('hi')
				# print(map_list[i])
				possible_ssbond.append(temp)
				possible_ssbond_id.append((map_id[i],map_id[j]))
	return possible_ssbond,possible_ssbond_id

def make_ssbond_without_repeat(map_list, map_id, mol_type_list):
	if len(map_list) != len(map_id):
		# print('map list length is not equal to map id list!')
		sys.exit()

	possible_ssbond = []
	possible_ssbond_id = []
	for i in range(len(map_list)-1):
		for j in range(i+1,len(map_list)):
			if i == j:
				continue
			elif mol_type_list[i][1:] == mol_type_list[j][1:]:
				continue
			elif compare_CA_distance(map_list[i][1],map_list[j][1],mol_type_list[i],mol_type_list[j]):
				temp = map_list[i][:]
				# temp.append(map_list[i])
				temp.extend(map_list[j])
				# print(temp)
				# print('hi')
				# print(map_list[i])
				possible_ssbond.append(temp)
				possible_ssbond_id.append((map_id[i],map_id[j]))
			else:
				continue
			# else:
			# 	# print(i,j)
			# 	# a = map_list[i].extend(map_list[j])
			# 	# print(a)
				
			# 	temp = map_list[i][:]
			# 	# temp.append(map_list[i])
			# 	temp.extend(map_list[j])
			# 	# print(temp)
			# 	# print('hi')
			# 	# print(map_list[i])
			# 	possible_ssbond.append(temp)
			# 	possible_ssbond_id.append((map_id[i],map_id[j]))
	return possible_ssbond,possible_ssbond_id

if __name__ == '__main__':
	args = sys.argv[1:]
	print args
	filename = args[0]
	name = args[0].split('/')[-1].split('.')[0]
	map_list, map_id ,mol_type_list= find_map_element(filename)

	# print('length of the map_list',len(map_list))
	possible_ssbond, possible_ssbond_id = make_ssbond_without_repeat(map_list, map_id, mol_type_list)
	# possible_ssbond = np.array(possible_ssbond)
	# possible_ssbond_id = np.array(possible_ssbond_id)
	# print(possible_ssbond_id)
	# print('****************************')
	# print(len(possible_ssbond[0]),len(possible_ssbond[0]))

	full_distance_map = sdm.convert_to_nxn_map(np.array(possible_ssbond))
	# print(full_distance_map)
	np.save('%s_ca_noSG_ssbond_nr.npy'%name,possible_ssbond)
	np.save('%s_ca_full_noSG_ssbond_nr.npy'%name,full_distance_map)
	np.save('%s_ca_noSG_ssbond_id_nr.npy'%name,possible_ssbond_id)
