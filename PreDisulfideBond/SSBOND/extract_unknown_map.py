# -*-coding:utf-8-*-
import os
import time
import numpy as np
import sys
from . import ssbond_distance_map as sdm
import math
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
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


def exmain_mol_list(mol_list,line):
    if mol_list[0]!=[] and mol_list[1]!=[] and mol_list[2]!=[] and mol_list[3]!=[] and mol_list[4]!=[]:
        return True,line[17:20].strip()+line[21]
    else:
        return False,line[17:20].strip()+line[21]
#I have change some program from here
def find_map_element(filename):
    mol_map_list = []
    flag_mol = False
    mol_id = None
    mol_id_list = []
    mol_name_temp = None
    last_mol = None
    mol_type_list = []
    count = 0
    break_count = 0
    with open(filename,'r') as f:
        for line in f:
            break_count += 1
            line_tag = line[:6].strip()
            if line_tag != 'ATOM':
                continue
            if line[17:20].strip() == 'PRO':
                continue
            if line_tag == 'ENDMDL' :
                break
            residue = line[17:20].strip()+line[21]+line[22:26].strip()
            if line_tag == 'ATOM' and mol_name_temp == None:
                mol_name_temp = residue
                mol_list = [ [] for i in range(5)]
            elif line_tag == 'ATOM' and mol_name_temp!=residue:
                mol_name_temp = residue
                mol_list = [ [] for i in range(5)]
                count += 1
            if line_tag == 'ATOM':
                if line[12:16].strip() == 'N' and mol_list[0] ==[]:
                    mol_list[0]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
                    flag_mol,mol_id = exmain_mol_list(mol_list, line)
                elif line[12:16].strip() =='CA' and mol_list[1] == []:
                    mol_list[1]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
                    flag_mol,mol_id = exmain_mol_list(mol_list, line)
                elif line[12:16].strip()  =='C' and mol_list[2] == []:
                    mol_list[2]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
                    flag_mol,mol_id = exmain_mol_list(mol_list, line)
                elif line[12:16].strip()  =='O' and mol_list[3] == []:
                    mol_list[3]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
                    flag_mol,mol_id = exmain_mol_list(mol_list, line)
                elif line[12:16].strip()  =='CB' and mol_list[4] == []:
                    mol_list[4]=[line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]
                    flag_mol,mol_id = exmain_mol_list(mol_list, line)
                if flag_mol == True:
                    mol_map_list.append(mol_list)
                    mol_id_list.append(mol_id)
                    mol_type_list.append(residue)
                    flag_mol = False
    return mol_map_list,mol_id_list,mol_type_list

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
                temp.extend(map_list[j])
                possible_ssbond.append(temp)
                possible_ssbond_id.append((mol_type_list[i],mol_type_list[j]))
            else:
                continue

    return possible_ssbond,possible_ssbond_id

if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    name = args[0].split('/')[-1].split('.')[0]
    map_list, map_id ,mol_type_list= find_map_element(filename)
    print ('length of the map_list',len(map_list))
    possible_ssbond, possible_ssbond_id = make_ssbond_without_repeat(map_list, map_id, mol_type_list)
    full_distance_map = sdm.convert_to_nxn_map(np.array(possible_ssbond))
    np.save('%s_ca_noSG_ssbond_nr.npy'%name,possible_ssbond)
    np.save('%s_ca_full_noSG_ssbond_nr.npy'%name,full_distance_map)
    np.save('%s_ca_noSG_ssbond_id_nr.npy'%name,possible_ssbond_id)
