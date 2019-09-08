import os
import time
import numpy as np
import math
import re
import sys

def correct_xyz(line_temp):
    if len(line_temp[6])-len(line_temp[7]) > 3:
        pos = 6
    else:
        pos = 7
    print pos
    temp = line_temp[pos].split('-')
    if len(temp) == 1:
        print "wrong line!"
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
            with open('ssbond_remove.txt', 'a' ) as wf:
                wf.write('bigcount ' + pdb + ' , ' + str(j1) + '\n ')
            return False
        elif len(j1) < 3:
            with open('ssbond_remove.txt', 'a' ) as wf:
                wf.write('smallcount '+ pdb + ' , ' + str(mol_map) + '\n ')
            return False
    return True


def create_map(pdbpath):
    pdb_list = os.listdir(pdbpath)
    print 'pdb numbers',len(pdb_list)
    if pdb_list[0] =='.DS_Store':
        pdb_list = pdb_list[1:]
    pdb_namefile=os.path.join(pdbpath,'pdb_name_noss.txt')
    with open(pdb_namefile,'w') as pdb_name:
        for pdb_n in pdb_list:
            pdb_name.write(pdb_n + '\n')
    nossbond_map = []
    all_ssbond = 0
    mol_list_all =[]
    for pdb in pdb_list:
        print pdb
        flag = True
        SSBOND_flag = True
        search_list = []
        count = 0
        CA_list = []
        ssbond_mol_map = []
        current_ssbond = 0
        pdbfile=os.path.join(pdbpath,pdb)
        with open(pdbfile,'r') as f:
            PDBchainid=pdb[4:5].strip()
            for line in f:
                line = line.strip()
                line_temp = line.split()
                SSchainid=line[15:16].strip()
                temp = line_temp[0]
                if (temp != 'SSBOND') and (temp != 'ATOM'):
                    continue
                if temp == 'SSBOND' and SSchainid==PDBchainid:
                    if line_temp[4][-1].isalpha():
                        if ord(line_temp[4][-1]) == 65:
                            firstsn0 = int(line_temp[4][:-1]) - 1
                            firstsn1 = line_temp[4][:-1] + chr(ord(line_temp[4][-1])+1)
                        elif ord(line_temp[4][-1]) == 90:
                            firstsn0 = line_temp[4][:-1] + chr(ord(line_temp[4][-1]) - 1)
                            firstsn1 = int(line_temp[4][:-1]) - 1
                        elif ord(line_temp[4][-1]) > 65 and ord(line_temp[4][-1]) < 90:
                            firstsn0 = line_temp[4][:-1] + chr(ord(line_temp[4][-1])-1)
                            firstsn1 = line_temp[4][:-1] + chr(ord(line_temp[4][-1])+1)
                    else:
                        firstsn0 = int(line_temp[4])-1
                        firstsn1 = int(line_temp[4])+1
                    if line_temp[7][-1].isalpha():
                        if ord(line_temp[7][-1]) == 65:
                            secondn0 = int(line_temp[7][:-1]) - 1
                            secondn1 = line_temp[7][:-1] + chr(ord(line_temp[7][-1])+1)
                        elif ord(line_temp[7][-1]) == 90:
                            secondn0 = line_temp[7][:-1] + chr(ord(line_temp[7][-1]) - 1)
                            secondn1 = int(line_temp[7][:-1]) - 1
                        elif ord(line_temp[7][-1]) > 65 and ord(line_temp[7][-1]) < 90:
                            secondn0 = line_temp[7][:-1] + chr(ord(line_temp[7][-1])-1)
                            secondn1 = line_temp[7][:-1] + chr(ord(line_temp[7][-1])+1)
                        else:
                            secondn0 = int(line_temp[7])-1
                            secondn1 = int(line_temp[7])+1
                        all_ssbond += 1
                        current_ssbond += 1
                        search_list.append(line_temp[3]+str(firstsn0))
                        search_list.append(line_temp[3]+str(firstsn1))
                        search_list.append(line_temp[6]+str(secondn0))
                        search_list.append(line_temp[6]+str(secondn1))
                        continue
                    if line[:5].strip() == 'ATOM'and SSBOND_flag:
                        ssbond_mol_map = [ [ [] for i in range(5)] for i in range(len(search_list))]
                        CA_list = [ [ [] for i in range(4)] for i in range(len(search_list)/4)]
                        SSBOND_flag = False
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
                    if temp == 'ATOM' and search_mol in search_list:
                        if line_temp[3] == 'PRO' or line_temp[3] == 'GLY':
                            continue
                        num = search_list.index(search_mol)
                        if line_temp[2] == 'CA':
                            a2 = num/4#current_ssbond
                            a3 = num%4#current_ssbond
                            if abs(len(line_temp[6])-len(line_temp[7])) <= 3:
                                CA_list[a2][a3]=[line_temp[6],line_temp[7],line_temp[8]]
                            else:
                                x,y,z=correct_xyz(line_temp)
                                CA_list[a2][a3]=[x,y,z]
                        if abs(len(line_temp[6])-len(line_temp[7])) <= 3:
                            if line_temp[2] == 'N' and ssbond_mol_map[num][0] ==[]:
                                ssbond_mol_map[num][0].append(float(line_temp[6]))
                                ssbond_mol_map[num][0].append(float(line_temp[7]))
                                ssbond_mol_map[num][0].append(float(line_temp[8]))
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
                    if temp == 'ENDMDL' :
                        break
                for i in range(len(ssbond_mol_map)):
                    if ssbond_mol_map[i][0] == [] and search_list[i]==search_list[search_list.index(search_list[i])]:
                        with open('copy.txt','a') as wcopyf:
                            wcopyf.write(pdb + ' ' + search_list[i] + '  '+ search_list[search_list.index(search_list[i])]+ '\n')
                        ssbond_mol_map[i] = ssbond_mol_map[search_list.index(search_list[i])]
                for i in range(len(ssbond_mol_map)):
                    if len(ssbond_mol_map[i]) > 6:
                        with open('molBigthan6.txt','a') as wmf:
                            wmf.write('pdb name: ' +pdb + ' ,mol length:' + str(len(ssbond_mol_map[i])) + '\n')
                    elif len(ssbond_mol_map[i]) < 6:
                        with open('mollessthan6.txt','a') as wmf:
                            wmf.write('pdb name: ' +pdb + ' ,mol length:' + str(len(ssbond_mol_map[i])) + '\n')
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
                    b1 = minDistance/2 #mol near the first mol in the ssbond
                    b2 = minDistance%2 + 2 #mol near the second mol in the ssbond
                    b3 = min2Distance/2 #mol near the first mol in the ssbond,second min
                    b4 = min2Distance%2 + 2 #mol near the second mol in the ssbond.second min
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
    nossbond_map = np.array(nossbond_map)
    return nossbond_map
if __name__ == "__main__":
    pdbpath=sys.argv[1]
    resultpath=sys.argv[2]
    resultfilename=sys.argv[3]
    resultnpy=os.path.join(resultpath,resultfilename)
    nossbond_map = create_map(pdbpath)
    np.save(resultnpy,nossbond_map)





