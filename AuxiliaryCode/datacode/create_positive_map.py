# -*-coding:utf-8 -*-
import os
import time
import numpy as np
import sys

def run(root_dir,pdbfolder):
    t0 = time.time()
    print root_dir,pdbfolder
    pdb_list = os.listdir(pdbfolder)
    if pdb_list[0] =='.DS_Store':
        pdb_list = pdb_list[1:]
    print len(pdb_list)
    with open(root_dir+'/pdb_name.txt','w') as pdb_name:
        for pdb_n in pdb_list:
            pdb_name.write(pdb_n + '\n')
    pdb_ssbond = 0
    all_ssbond = 0
    ssbond_list = []
    ssbonds_map = []
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
            for line in f:
                line_tag = line[:6].strip()
                SSchainid = line[15:16].strip()
                if (line_tag != 'SSBOND') and (line_tag != 'ATOM'):
                    continue
                if flag and line_tag == 'SSBOND':
                    flag = False
                    pdb_ssbond += 1
                if line_tag == 'SSBOND'and SSchainid==pdb[4:5].strip():
                    all_ssbond += 1
                    ssbond_list.append((pdb, line))
                    search_list.append(line[11:14].strip()+line[15]+line[17:21].strip())
                    search_list.append(line[25:28].strip()+line[29]+line[31:35].strip())
                    continue
                if line_tag == 'ATOM' and SSBOND_flag:
                    ssbond_map = [ [ [] for i in range(5) ]for i in range(len(search_list))]
                    SSBOND_flag = False
                search_mol = line[17:20].strip()+line[21] +line[22:26].strip()
                if line_tag == 'ATOM' and search_mol in search_list:
                    map_index = search_list.index(search_mol)
                    if line[12:16].strip() == 'N' and ssbond_map[map_index][0] == []:
                        ssbond_map[map_index][0]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
                    elif line[12:16].strip() =='CA' and ssbond_map[map_index][1] == []:
                        ssbond_map[map_index][1]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
                    elif line[12:16].strip()  =='C' and ssbond_map[map_index][2] == []:
                        ssbond_map[map_index][2]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
                    elif line[12:16].strip()  =='O' and ssbond_map[map_index][3] == []:
                        ssbond_map[map_index][3]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
                    elif line[12:16].strip()  =='CB' and ssbond_map[map_index][4] == []:
                        ssbond_map[map_index][4]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
                    continue
                if line_tag == 'ENDMDL' :
                    break
            for i in range(len(ssbond_map)):
                if ssbond_map[i][0] == [] and search_list[i]==search_list[search_list.index(search_list[i])]:
                    with open(root_dir+'/copy.txt','a') as wcopyf:
                        wcopyf.write(pdb + ' ' + search_list[i] + '  '+ search_list[search_list.index(search_list[i])]+ '\n')
                    ssbond_map[i] = ssbond_map[search_list.index(search_list[i])]
            for i in range(len(ssbond_map)):
                a = []
                correct_mol_flag = True
                if i%2 == 1:
                    continue
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
                    new_list.append(a)
        ssbonds_map.extend(new_list)
    print len(ssbonds_map)
    np.save(resultfile,ssbonds_map)

if __name__ == '__main__':
    args = sys.argv[1:]
    pdbpath = args[1]
    resultpath = args[2]
    resultfilename = args[3]
    resultfile=os.path.join(resultpath,resultfilename)
    run(resultfile,pdbpath)

