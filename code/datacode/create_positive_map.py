# -*-coding:utf-8 -*-


import os 
import time
import numpy as np
import sys

def run(root_dir,pdbfolder):
	t0 = time.time()
	#root_dir = os.path.dirname(os.path.abspath(args[0]))
	#pdbfolder = os.path.basename(args[0])
	print root_dir,pdbfolder
	pdb_list = os.listdir(pdbfolder)
	# pdb_list = os.listdir('/Users/dongxq/Desktop/disulfide/checkCA/pdb/')

	# print len(pdb_list)
	if pdb_list[0] =='.DS_Store':
		pdb_list = pdb_list[1:]
	print len(pdb_list)
	# np.save('pdb_name.npy', pdb_list)
	with open(root_dir+'/pdb_name.txt','w') as pdb_name:
		for pdb_n in pdb_list:
            #print (pdb_n)
			pdb_name.write(pdb_n + '\n')
		
	pdb_ssbond = 0
	all_ssbond = 0
	ssbond_list = []
	ssbonds_map = []
	# ssbonds_map = np.array(ssbonds_map)

	bigcount = 0
	smallcount = 0
	

	for pdb in pdb_list:
		flag = True
		SSBOND_flag = True
		search_list = []
		new_list = []
		count = 0
		ssbond_map = []
		flag_mol = False
		print pdb,SSBOND_flag,pdb[4:5]
		with open(pdbfolder + '/'+ pdb,'r') as f:
		# with open('/Users/dongxq/Desktop/disulfide/checkCA/pdb/%s'%pdb,'r') as f:
			for line in f:
				line_tag = line[:6].strip()
				SSchainid = line[15:16].strip()
				#print SSchainid,'lllllllllllll'
				if (line_tag != 'SSBOND') and (line_tag != 'ATOM'):
					continue
				if flag and line_tag == 'SSBOND':
					# print 'ssbond'
					flag = False
					pdb_ssbond += 1
                #only consider the SSBOND in the specific chain
				if line_tag == 'SSBOND'and SSchainid==pdb[4:5].strip():
					#print SSchainid,'lllllllllllll'

					all_ssbond += 1
					ssbond_list.append((pdb, line))
					search_list.append(line[11:14].strip()+line[15]+line[17:21].strip())
					search_list.append(line[25:28].strip()+line[29]+line[31:35].strip())
					continue
				if line_tag == 'ATOM' and SSBOND_flag:
					#print'ssssssssssssssss'
					# if (len(search_list)/2) == 1:
					# 	ssbond_map.append([])
					#print search_list
					ssbond_map = [ [ [] for i in range(5) ]for i in range(len(search_list))]
					#print ssbond_map,'ssssssssssssssss'
					# xyz_count = [ 0 for i in range(len(search_list/2))]
					SSBOND_flag = False
					# print ssbond_map
				search_mol = line[17:20].strip()+line[21] +line[22:26].strip()
				#print search_mol
				#print search_list
				# print search_mol
				# print search_mol

				if line_tag == 'ATOM' and search_mol in search_list:
					# print 'yse',line[12:16].strip()
					map_index = search_list.index(search_mol)
					#print map_index,'ssssssssssssssss'
					#print line[12:16].strip()
					#print ssbond_map
					#print ssbond_map[map_index][0]
					if line[12:16].strip() == 'N' and ssbond_map[map_index][0] == []:
						# print 'N',[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
						ssbond_map[map_index][0]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
						# flag_mol,mol_id = exmain_mol_list(ssbond_map,search_mol)
					elif line[12:16].strip() =='CA' and ssbond_map[map_index][1] == []:
						# print 'CA',[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
						ssbond_map[map_index][1]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
						# flag_mol,mol_id = exmain_mol_list(ssbond_map,search_mol)
					elif line[12:16].strip()  =='C' and ssbond_map[map_index][2] == []:
						# print 'C',[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
						ssbond_map[map_index][2]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
						# flag_mol,mol_id = exmain_mol_list(ssbond_map,search_mol)
					elif line[12:16].strip()  =='O' and ssbond_map[map_index][3] == []:
						# print 'O',[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
						ssbond_map[map_index][3]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
						# flag_mol,mol_id = exmain_mol_list(ssbond_map,search_mol)
					elif line[12:16].strip()  =='CB' and ssbond_map[map_index][4] == []:
						# print 'CB',[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
						ssbond_map[map_index][4]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
						# flag_mol,mol_id = exmain_mol_list(ssbond_map,search_mol)
					continue
				if line_tag == 'ENDMDL' :
					break
			for i in range(len(ssbond_map)):
				if ssbond_map[i][0] == [] and search_list[i]==search_list[search_list.index(search_list[i])]:
					# print 'copy'
					with open(root_dir+'/copy.txt','a') as wcopyf:
						wcopyf.write(pdb + ' ' + search_list[i] + '  '+ search_list[search_list.index(search_list[i])]+ '\n')
					ssbond_map[i] = ssbond_map[search_list.index(search_list[i])]
			# print search_list
			# print ssbond_map
			for i in range(len(ssbond_map)):
				a = []
				correct_mol_flag = True
				if i%2 == 1:
					continue
				# print i
				
				for j1 in ssbond_map[i]:
					if len(j1) > 3:
						bigcount += 1
						print j1
						correct_mol_flag = False
						with open(root_dir+'/ssbond_remove.txt', 'a' ) as wf:
							wf.write('bigcount ' + pdb + ' , ' + str(j1) + '\n ')
					elif len(j1) < 3:
						smallcount += 1
						print j1
						correct_mol_flag = False
						with open(root_dir+'/ssbond_remove.txt', 'a' ) as wf:
							wf.write('smallcount '+ pdb + ' , ' + str(ssbond_map[i]) + '\n ')
				for j2 in ssbond_map[i+1]:
					if len(j2) > 3:
						bigcount += 1
						print j2
						correct_mol_flag = False
						with open(root_dir+'/ssbond_remove.txt', 'a' ) as wf:
							wf.write('bigcount ' + pdb + ' , ' + str(j2) + '\n ')
					elif len(j2) < 3:
						smallcount += 1
						print j2
						correct_mol_flag = False
						with open(root_dir+'/ssbond_remove.txt', 'a' ) as wf:
							wf.write('smallcount '+ pdb + ' , ' + str(ssbond_map[i]) + '\n ')
				if correct_mol_flag:
					a.extend(ssbond_map[i])
					a.extend(ssbond_map[i+1])
					# print 'a',a 
					# print a 
					new_list.append(a)

					# print new_list
			
		ssbonds_map.extend(new_list)


		# break
	# print ssbonds_map
	print len(ssbonds_map)
	# ssbonds_map = np.array(ssbonds_map)
	np.save(root_dir+'/positive_ssbond_map.npy',ssbonds_map)

# print ssbonds_map
if __name__ == '__main__':
	#args = sys.argv[1:]
	root_dir='/Users/dongxq/Desktop/SSBOND_supplement/rootpath40'
	pdbfolder='/Users/dongxq/Desktop/SSBOND_supplement/newdataset40'
	run(root_dir,pdbfolder)

