import os 
import time
import numpy as np
import math
import re

def correct_xyz(line_temp):
	# print len(line_temp[6]),len(line_temp[7])
	if len(line_temp[6])-len(line_temp[7]) > 3:
		pos = 6
	else:
		pos = 7
	print pos
	temp = line_temp[pos].split('-')
	if len(temp) == 1:
		print "wrong line!"
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

def ifmolleneq6(pdb, mol_map):
	for j1 in mol_map:
		if len(j1) > 3:
			# bigcount += 1
			# print j1
			with open('ssbond_remove.txt', 'a' ) as wf:
				wf.write('bigcount ' + pdb + ' , ' + str(j1) + '\n ')
			return False
		elif len(j1) < 3:
			# smallcount += 1
			# print j1
			with open('ssbond_remove.txt', 'a' ) as wf:
				wf.write('smallcount '+ pdb + ' , ' + str(mol_map) + '\n ')
			return False
	return True


# t0 = time.time()
pdb_list = os.listdir('/Users/dongxq/Desktop/SSBOND_supplement/newdataset30/')
print 'pdb numbers',len(pdb_list)
if pdb_list[0] =='.DS_Store': 
	pdb_list = pdb_list[1:]
# print 'pdb numbers',len(pdb_list)
pdb_namefile=os.path.join('/Users/dongxq/Desktop/SSBOND_supplement/rootpath30','pdb_name_noss.txt')
with open(pdb_namefile,'w') as pdb_name:
	for pdb_n in pdb_list:
		pdb_name.write(pdb_n + '\n')

nossbond_map = []
all_ssbond = 0
mol_list_all =[]
# bigcount = 0
# smallcount = 0

for pdb in pdb_list:
	print pdb
	flag = True
	SSBOND_flag = True
	search_list = []
	count = 0
	CA_list = []
	ssbond_mol_map = []
	current_ssbond = 0
	# mol_pos = 5

	with open('/Users/dongxq/Desktop/SSBOND_supplement/newdataset30/%s'%pdb,'r') as f:
		PDBchainid=pdb[4:5].strip()
		for line in f:
			line = line.strip()
			line_temp = line.split()
			SSchainid=line[15:16].strip()
			# firsts = line_temp[2]+line_temp[3]
			
			
			temp = line_temp[0]
            
			if (temp != 'SSBOND') and (temp != 'ATOM'):
				# print temp,
				continue
			# if flag and temp == 'SSBOND':
			# 	# print 'ssbond'
			# 	flag = False
			# 	pdb_ssbond += 1
			if temp == 'SSBOND' and SSchainid==PDBchainid:
				# print line_temp
				# print line_temp
				if line_temp[4][-1].isalpha():
					# print 'alpha'
					if ord(line_temp[4][-1]) == 65:
						firstsn0 = int(line_temp[4][:-1]) - 1
						# if 
						firstsn1 = line_temp[4][:-1] + chr(ord(line_temp[4][-1])+1)
					elif ord(line_temp[4][-1]) == 90:
						firstsn0 = line_temp[4][:-1] + chr(ord(line_temp[4][-1]) - 1)
						# if 
						firstsn1 = int(line_temp[4][:-1]) - 1
					elif ord(line_temp[4][-1]) > 65 and ord(line_temp[4][-1]) < 90:
						firstsn0 = line_temp[4][:-1] + chr(ord(line_temp[4][-1])-1)
						firstsn1 = line_temp[4][:-1] + chr(ord(line_temp[4][-1])+1)
				else:
					firstsn0 = int(line_temp[4])-1 
					firstsn1 = int(line_temp[4])+1 
				if line_temp[7][-1].isalpha():
					# print 'alpha'
					if ord(line_temp[7][-1]) == 65:
						secondn0 = int(line_temp[7][:-1]) - 1
						# if 
						secondn1 = line_temp[7][:-1] + chr(ord(line_temp[7][-1])+1)
					elif ord(line_temp[7][-1]) == 90:
						secondn0 = line_temp[7][:-1] + chr(ord(line_temp[7][-1]) - 1)
						# if 
						secondn1 = int(line_temp[7][:-1]) - 1
					elif ord(line_temp[7][-1]) > 65 and ord(line_temp[7][-1]) < 90:
						secondn0 = line_temp[7][:-1] + chr(ord(line_temp[7][-1])-1)
						secondn1 = line_temp[7][:-1] + chr(ord(line_temp[7][-1])+1)
				else:
					secondn0 = int(line_temp[7])-1
					secondn1 = int(line_temp[7])+1

				# if line_temp[4][-1] == 'B':
				# 	firstsn0 = line_temp[4][:-1]+'A'
				# 	# print 'first mol',firstsn0
				# 	firstsn1 = int(line_temp[4][:-1]) + 1
				# 	with open('special_molpos.txt','a') as wsf:
				# 		wsf.write(pdb+'\n')
				# 		wsf.write(line)
				# elif line_temp[4][-1] == 'A':
				# 	firstsn0 = line_temp[4][:-1]
				# 	# print 'first mol',firstsn0
				# 	firstsn1 = line_temp[4][:-1] + 'B'
				# 	with open('special_molpos.txt','a') as wsf:
				# 		wsf.write(pdb+'\n')
				# 		wsf.write(line)
				# elif line_temp[4][-1] == 'D':
				# 	firstsn0 = line_temp[4][:-1]+'C'
				# 	# print 'first mol',firstsn0
				# 	firstsn1 = int(line_temp[4][:-1])+1
				# 	with open('special_molpos.txt','a') as wsf:
				# 		wsf.write(pdb+'\n')
				# 		wsf.write(line)
				# elif line_temp[4][-1] == 'F':
				# 	firstsn0 = line_temp[4][:-1]+'E'
				# 	# print 'first mol',firstsn0
				# 	firstsn1 = line_temp[4][:-1]+'G'
				# 	with open('special_molpos.txt','a') as wsf:
				# 		wsf.write(pdb+'\n')
				# 		wsf.write(line)
				# else:
				# 	firstsn0 = int(line_temp[4])-1 
				# 	firstsn1 = int(line_temp[4])+1 
				# if line_temp[7][-1] == 'B':
				# 	secondfn0 = line_temp[7][:-1]+'A'
				# 	with open('special_molpos.txt','a') as wsf:
				# 		wsf.write(pdb+'\n')
				# 		wsf.write(line)
				# 	# print 'second mol',secondn0
				# 	secondfn1 = int(line_temp[7][:-1]) + 1
				# elif line_temp[7][-1] == 'A':
				# 	secondfn0 = line_temp[7][:-1]
				# 	with open('special_molpos.txt','a') as wsf:
				# 		wsf.write(pdb+'\n')
				# 		wsf.write(line)
				# 	# print 'second mol',secondn0
				# 	secondfn1 = line_temp[7][:-1] + 'B'
				# elif line_temp[7][-1] == 'D':
				# 	secondfn0 = line_temp[7][:-1] + 'C'
				# 	with open('special_molpos.txt','a') as wsf:
				# 		wsf.write(pdb+'\n')
				# 		wsf.write(line)
				# 	# print 'second mol',secondn0
				# 	secondfn1 = int(line_temp[7][:-1]) + 1
				# elif line_temp[7][-1] == 'F':
				# 	secondfn0 = line_temp[7][:-1] + 'E'
				# 	with open('special_molpos.txt','a') as wsf:
				# 		wsf.write(pdb+'\n')
				# 		wsf.write(line)
				# 	# print 'second mol',secondn0
				# 	secondfn1 = line_temp[7][:-1] + 'G'
				
				# else:
				# 	secondn0 = int(line_temp[7])-1
				# 	secondn1 = int(line_temp[7])+1
				# seconds = line_temp[5]+line_temp[6]

				
				all_ssbond += 1
				current_ssbond += 1
				# ssbond_list.append((pdb, line_temp))
				search_list.append(line_temp[3]+str(firstsn0))
				search_list.append(line_temp[3]+str(firstsn1))
				search_list.append(line_temp[6]+str(secondn0))
				search_list.append(line_temp[6]+str(secondn1))
				# print 'search list: ', search_list


				# print search_list
				continue
			if line[:5].strip() == 'ATOM'and SSBOND_flag:

				ssbond_mol_map = [ [ [] for i in range(5)] for i in range(len(search_list))]
				CA_list = [ [ [] for i in range(4)] for i in range(len(search_list)/4)]
				# mol_list = [ [False for i in range(6)] for i in range(len(search_list))]
				# xyz_count = [ 0 for i in range(len(search_list/2))]
				SSBOND_flag = False
				# print ssbond_map
			if len(line_temp[2]) == 7:
				mol_pos = 4
				line_temp3 = line_temp[2][3:]
				line_temp[2] = line_temp[2][:3]
				line_temp.insert(3,line_temp3)
				with open('line_temp.txt','a') as wlf:
					wlf.write('pdb name: '+pdb +'\n')
					wlf.write(str(line_temp) +'\n')
			if len(line_temp[4]) == 5:
				line_temp5 = line_temp[4][1:]
				line_temp[4] = line_temp[4][0]
				line_temp.insert(5,line_temp5)
				with open('line_temp.txt','a') as wlf:
					wlf.write('pdb name: '+pdb +'\n')
					wlf.write(str(line_temp) +'\n')

			search_mol = line_temp[4]+ line_temp[5]

			# print mol_pos
			# print line_temp[mol_pos]
			# print str(line_temp[mol_pos]) in search_list
			if temp == 'ATOM' and search_mol in search_list:
				# print CA_list
				# print search_list
				# print line_temp
				# print 'mol_pos',mol_pos
				if line_temp[3] == 'PRO' or line_temp[3] == 'GLY':
					# with open('PRO-GLY.txt','a') as wf:
					# 	wf.write('pdb name :' + pdb + ' has PRO or GLY near the ssbond\n')
					continue
				# if len(line_temp[3]) == 4 and line_temp[3][0] == 'A':
				# 	search_mol = search_mol[1:]
				# 	print search_mol
				num = search_list.index(search_mol)
				# print 'num',num
				if line_temp[2] == 'CA':
					a2 = num/4#current_ssbond
					a3 = num%4#current_ssbond
					# print a2,a3
					# CA_list.append((num,[line_temp[6],line_temp[7],line_temp[8]]))
					if abs(len(line_temp[6])-len(line_temp[7])) <= 3:
						CA_list[a2][a3]=[line_temp[6],line_temp[7],line_temp[8]]
					else:	
						x,y,z=correct_xyz(line_temp)
						CA_list[a2][a3]=[x,y,z]
				
				if abs(len(line_temp[6])-len(line_temp[7])) <= 3:
					# print line_temp
					if line_temp[2] == 'N' and ssbond_mol_map[num][0] ==[]:
						ssbond_mol_map[num][0].append(float(line_temp[6]))
						ssbond_mol_map[num][0].append(float(line_temp[7]))
						ssbond_mol_map[num][0].append(float(line_temp[8]))
						# ssbond_map[map_index][0] = float(line_temp[mol_pos+1])
						# ssbond_map[map_index][1] = float(line_temp[mol_pos+2])
					elif line_temp[2] =='CA' and ssbond_mol_map[num][1] == []:
						ssbond_mol_map[num][1].append(float(line_temp[6]))
						ssbond_mol_map[num][1].append(float(line_temp[7]))
						ssbond_mol_map[num][1].append(float(line_temp[8]))
					elif line_temp[2] =='C' and ssbond_mol_map[num][2] == []:
						ssbond_mol_map[num][2].append(float(line_temp[6]))
						ssbond_mol_map[num][2].append(float(line_temp[7]))
						ssbond_mol_map[num][2].append(float(line_temp[8]))
					elif line_temp[2] =='O' and ssbond_mol_map[num][3] == []:
						ssbond_mol_map[num][3].append(float(line_temp[6]))
						ssbond_mol_map[num][3].append(float(line_temp[7]))
						ssbond_mol_map[num][3].append(float(line_temp[8]))
					elif line_temp[2] =='CB' and ssbond_mol_map[num][4] == []:
						ssbond_mol_map[num][4].append(float(line_temp[6]))
						ssbond_mol_map[num][4].append(float(line_temp[7]))
						ssbond_mol_map[num][4].append(float(line_temp[8]))
					'''
					elif ssbond_mol_map[num][4] != [] and line_temp[2] != 'H' and ssbond_mol_map[num][5] == []:
						ssbond_mol_map[num][5].append(float(line_temp[6]))
						ssbond_mol_map[num][5].append(float(line_temp[7]))
						ssbond_mol_map[num][5].append(float(line_temp[8]))
					'''
				else:
				
					x,y,z=correct_xyz(line_temp)
					if line_temp[2] == 'N' and ssbond_mol_map[num][0] == []:
						ssbond_mol_map[num][0].append([x,y,z])
						print ssbond_mol_map[num][0]
					elif line_temp[2] =='CA' and ssbond_mol_map[num][1] == []:
						ssbond_mol_map[num][1].append([x,y,z])
						print ssbond_mol_map[num][1]
					elif line_temp[2] =='C' and ssbond_mol_map[num][2] == []:
						ssbond_mol_map[num][2].append([x,y,z])
						print ssbond_mol_map[num][2]
					elif line_temp[2] =='O' and ssbond_mol_map[num][3] == []:
						ssbond_mol_map[num][3].append([x,y,z])
						print ssbond_mol_map[num][3]
					elif line_temp[2] =='CB' and ssbond_mol_map[num][4] == []:
						ssbond_mol_map[num][4].append([x,y,z])
						print ssbond_mol_map[num][4]
					'''
					elif ssbond_mol_map[num][4] != [] and line_temp[2] != 'H' and ssbond_mol_map[num][5] == []:
						ssbond_mol_map[num][5].append([x,y,z])
						print ssbond_mol_map[num][5]
					'''
						# print line_temp
						# ssbond_mol_map[num].append(x)
						# ssbond_mol_map[num].append(y)
						# ssbond_mol_map[num].append(z)
					# print '********************'
					

				# print map_index
				# xyz_count[map_index] += 1
				# print line_temp
				# print len(search_list)
			if temp == 'ENDMDL' :
				break
		for i in range(len(ssbond_mol_map)):
			if ssbond_mol_map[i][0] == [] and search_list[i]==search_list[search_list.index(search_list[i])]:
				# print 'copy'
				with open('copy.txt','a') as wcopyf:
					wcopyf.write(pdb + ' ' + search_list[i] + '  '+ search_list[search_list.index(search_list[i])]+ '\n')
				ssbond_mol_map[i] = ssbond_mol_map[search_list.index(search_list[i])]
		for i in range(len(ssbond_mol_map)):
			if len(ssbond_mol_map[i]) > 6:
				# print 'length more than 18'
				with open('molBigthan6.txt','a') as wmf:
					wmf.write('pdb name: ' +pdb + ' ,mol length:' + str(len(ssbond_mol_map[i])) + '\n')
				# print i
				
				# break
			elif len(ssbond_mol_map[i]) < 6:
				# print 'length less than 18'
				# print i
				with open('mollessthan6.txt','a') as wmf:
					wmf.write('pdb name: ' +pdb + ' ,mol length:' + str(len(ssbond_mol_map[i])) + '\n')
				# print ssbond_mol_map[i]
				
		# print 'CA_list length : ',len(CA_list)
		# print 'length of the ssbond_mol_map',len(ssbond_mol_map)
		# if CA_list
		for i in range(current_ssbond): # find all nossbond near the ssbond
			distance = [0,0,0,0]
			if CA_list[i][0] != []:
				if CA_list[i][2] != []:
					sumCA = 0
					for xyz in range(3):
						sumCA += pow((float(CA_list[i][0][xyz])-float(CA_list[i][2][xyz])), 2)
					distance[0] = math.sqrt(sumCA)
				if CA_list[i][3] != []:
					sumCA = 0
					for xyz in range(3):
						sumCA += pow((float(CA_list[i][0][xyz])-float(CA_list[i][3][xyz])), 2)
					distance[1] = math.sqrt(sumCA)
			if CA_list[i][1] != []:
				if CA_list[i][2] != []:
					sumCA = 0
					for xyz in range(3):
						sumCA += pow((float(CA_list[i][1][xyz])-float(CA_list[i][2][xyz])), 2)
					distance[2] = math.sqrt(sumCA)
				if CA_list[i][3] != []:
					sumCA = 0
					for xyz in range(3):
						sumCA += pow((float(CA_list[i][1][xyz])-float(CA_list[i][3][xyz])), 2)
					distance[3] = math.sqrt(sumCA)
			minDistance = distance.index(min(distance))
			distance[distance.index(min(distance))] = 10000000
			min2Distance = distance.index(min(distance))
			# print 'distance',distance
			# print 'maxDistance',maxDistance
			b1 = minDistance/2 #mol near the first mol in the ssbond
			b2 = minDistance%2 + 2 #mol near the second mol in the ssbond
			b3 = min2Distance/2 #mol near the first mol in the ssbond,second min
			b4 = min2Distance%2 + 2 #mol near the second mol in the ssbond.second min

			# print 'b1',b1
			# print 'b2',b2
			# print ssbond_mol_map
			# print i*4+b1
			# print ssbond_mol_map[i*4+b1]
			# print ssbond_mol_map[i*4+b2]
			# print ssbond_mol_map[i*4+b1]+ssbond_mol_map[i*4+b2]

			if ifmolleneq6(pdb,ssbond_mol_map[i*4+b1]) and ifmolleneq6(pdb,ssbond_mol_map[i*4+b2]):
				with open('build_disufide.txt','a') as wdf:
					wdf.write(pdb + '\n' )
					wdf.write(str(ssbond_mol_map[i*4+b1]))
					wdf.write('\n')
					wdf.write(str(ssbond_mol_map[i*4+b2]))
				temp_nossbond = ssbond_mol_map[i*4+b1]+ssbond_mol_map[i*4+b2]
				nossbond_map.append(temp_nossbond)
			if ifmolleneq6(pdb,ssbond_mol_map[i*4+b3]) and ifmolleneq6(pdb,ssbond_mol_map[i*4+b4]):
				with open('build_disufide.txt','a') as wdf:
					wdf.write(pdb + '\n' )
					wdf.write(str(ssbond_mol_map[i*4+b3]))
					wdf.write('\n')
					wdf.write(str(ssbond_mol_map[i*4+b4]))
				temp_nossbond = ssbond_mol_map[i*4+b3]+ssbond_mol_map[i*4+b4]
				nossbond_map.append(temp_nossbond)

			# ssbond_mol_map=np.array(ssbond_mol_map)
			# print ssbond_mol_map
			# print distance
			# print temp_nossbond
			# if temp_nossbond != []:
			# 	count += 1
			# 	with open('nossbond.txt','a') as wnf:
			# 		wnf.write(pdb+'\n')
				
nossbond_map = np.array(nossbond_map)
print nossbond_map
resultnpy='/Users/dongxq/Desktop/SSBOND_supplement/rootpath30/nossbonds_map.npy'
np.save(resultnpy,nossbond_map)
print nossbond_map.shape
print all_ssbond

# nossbond_map_final = []
# 	nossbond_map_final.append(nossbond_map[i])
# nossbond_map_final = np.array(nossbond_map_final)
# nossbond_map_final = nossbond_map_final.reshape(len(nossbond_map_final),12,3)


# c = 0
# ca = 0
# n = 0
# cb = 0
# o = 0
# cg = 0
# for i in range(len(mol_list_all)):
# 	for j in range(len(mol_list_all[i])):
# 		if mol_list_all[i][j][0] == True:
# 			ca += 1
# 		if mol_list_all[i][j][1] == True:
# 			n += 1
# 		if mol_list_all[i][j][2] == True:
# 			c += 1
# 		if mol_list_all[i][j][3] == True:
# 			o += 1
# 		if mol_list_all[i][j][4] == True:
# 			cb += 1
# 		if mol_list_all[i][j][5] == True:
# 			cg += 1 
# no_ssbond_map = np.array(nossbond_map)
# no_ssbond_map.reshape(len(nossbond_map),12,3)
# print nossbond_map_final
# print nossbond_map
# print len(nossbond_map)
# print bigcount
# print smallcount
# print all_ssbond
# print nossbond_map_final.shape
# print 'CA :%d,N :%d,C :%d,O :%d,CB :%d,CG :%d'%(ca,n,c,o,cb,cg)

# np.save('nossbond_map_final.npy',nossbond_map_final)



