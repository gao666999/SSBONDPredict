import re,os
import Nepre
import rmsd
import Mu_position as Mp
from Nepre import Nepre_v3
from Nepre import AminoAcid
def energy2(pdbfile,dict1):

    mu_list = []
    for pairs in dict1.keys():
        pairs_list = []
        pairs = pairs.split('-')
        wildtype_name1 = pairs[0][:3].strip()
        if wildtype_name1 != 'CYS':
            mutationtype_name1 = 'CYS'
            idnumber1 = pairs[0][4:].strip()
            chainid1 = pairs[0][3:4]
            mutation_information1 = create_new_AA(pdbfile,wildtype_name1,idnumber1,chainid1)
            pairs_list.append( (idnumber1, chainid1,wildtype_name1, mutationtype_name1, mutation_information1) )

        wildtype_name2 = pairs[1][:3].strip()
        if wildtype_name2 != 'CYS':
            mutationtype_name2 = 'CYS'

            idnumber2 = pairs[1][4:].strip()
            chainid2 = pairs[0][3:4]
            mutation_information2 = create_new_AA(pdbfile,wildtype_name2,idnumber2,chainid2)
            pairs_list.append((idnumber2,chainid2,wildtype_name2,mutationtype_name2, mutation_information2))

        mu_list.append(pairs_list)

    energy_list = Nepre.Nepre_v3.get_energy(pdbfile,mu_list)
    lenth = len(energy_list)
    n = 0
    for i in dict1.keys():
        value = dict1[i]
        E = energy_list[n]
        Ev = '%.4f'%E
        dict1[i] = value + ' ' +  str(Ev)
        n += 1
    return dict1


def create_new_AA(pdbfile,wildtype_name,idnumber,chainid):
    mutation_AA = []
    with open (pdbfile,'r') as f:
        lines = f.readlines()
        #print lines
        lenth = len(lines)
        #print lenth
        #print 'i am length '
        i = 0
        while i<lenth:
            #print lines[i]
            #print lenth
            #print i
            #print ' iiiiiiiiiiiii'
            line_tag = lines[i][:6].strip()
            if line_tag == 'ATOM':
                if lines[i][17:20].strip() == wildtype_name and lines[i][20:22].strip() == chainid and lines[i][22:27].strip() == idnumber:
                    if lines[i][17:20].strip() == "CYS":
                        mutation_AA = []
                        mutation_AA.append(lines[i])
                        mutation_AA.append(lines[i + 1])
                        mutation_AA.append(lines[i + 2])
                        mutation_AA.append(lines[i + 3])
                        mutation_AA.append(lines[i + 4])
                        mutation_AA.append(lines[i + 5])
                        break
                        #i += 6
                        #continue
                    elif lines[i][17:20].strip() == "ALA":
                        mutation_AA = []
                        position = Mp.xyz5_position(i,lines)
                        #print position
                        #print 'this is position'
                        line1 = lines[i].replace('ALA','CYS')
                        line2 = lines[i+1].replace('ALA','CYS')
                        line3 = lines[i+2].replace('ALA','CYS')
                        line4 = lines[i+3].replace('ALA','CYS')
                        line5 = lines[i+4].replace('ALA','CYS')
                        line6_s1 = lines[i+4][:30].replace('CB  ALA','SG  CYS')
                        line6_s2 = lines[i+4][54:].replace('C','S')
                        line6 = line6_s1 + position + line6_s2
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break
                        # create line6 and add into the file
                        # mutation_AA.append(line_6)
                    elif lines[i][17:20].strip() == "ARG":
                        mutation_AA = []
                        line1 = lines[i].replace('ARG','CYS')
                        line2 = lines[i+1].replace('ARG','CYS')
                        line3 = lines[i+2].replace('ARG','CYS')
                        line4 = lines[i+3].replace('ARG','CYS')
                        line5 = lines[i+4].replace('ARG','CYS')
                        line_a = lines[i+5].replace('CG  ARG','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        #line6 = line_a.replace('C','S')
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break
                    elif lines[i][17:20].strip() == "ASN":
                        mutation_AA = []
                        line1 = lines[i].replace('ASN','CYS')
                        line2 = lines[i+1].replace('ASN','CYS')
                        line3 = lines[i+2].replace('ASN','CYS')
                        line4 = lines[i+3].replace('ASN','CYS')
                        line5 = lines[i+4].replace('ASN','CYS')
                        line_a = lines[i+5].replace('CG  ASN','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break
                    elif lines[i][17:20].strip() == "ASP":
                        mutation_AA = []
                        line1 = lines[i].replace('ASP','CYS')
                        line2 = lines[i+1].replace('ASP','CYS')
                        line3 = lines[i+2].replace('ASP','CYS')
                        line4 = lines[i+3].replace('ASP','CYS')
                        line5 = lines[i+4].replace('ASP','CYS')
                        line_a = lines[i+5].replace('CG  ASP','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "GLN":
                        mutation_AA = []
                        line1 = lines[i].replace('GLN','CYS')
                        line2 = lines[i+1].replace('GLN','CYS')
                        line3 = lines[i+2].replace('GLN','CYS')
                        line4 = lines[i+3].replace('GLN','CYS')
                        line5 = lines[i+4].replace('GLN','CYS')
                        line_a = lines[i+5].replace('CG  GLN','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "GLU":
                        mutation_AA = []
                        line1 = lines[i].replace('GLU','CYS')
                        line2 = lines[i+1].replace('GLU','CYS')
                        line3 = lines[i+2].replace('GLU','CYS')
                        line4 = lines[i+3].replace('GLU','CYS')
                        line5 = lines[i+4].replace('GLU','CYS')
                        line_a = lines[i+5].replace('CG  GLU','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "GLY":
                        mutation_AA = []
                        position5,position6 = Mp.xyz4a_position(i,lines)
                        line1 = lines[i].replace('GLY','CYS')
                        line2 = lines[i+1].replace('GLY','CYS')
                        line3 = lines[i+2].replace('GLY','CYS')
                        line4 = lines[i+3].replace('GLY','CYS')
                        #create line5
                        line5_s1 = lines[i+3][:30].replace('O   GLY','CB  CYS')
                        line5_s2 = lines[i+3][54:].replace('O','C')
                        line5 = line5_s1 +position5 +line5_s2
                        #create line6
                        line6_s1 = lines[i+3][:30].replace('SG  GLY','CB  CYS')
                        line6_s2 = lines[i+3][54:].replace('O','S')
                        #print s1,s2
                        line6 = line6_s1 + position6 + line6_s2

                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "HIS":
                        mutation_AA = []
                        line1 = lines[i].replace('HIS','CYS')
                        line2 = lines[i+1].replace('HIS','CYS')
                        line3 = lines[i+2].replace('HIS','CYS')
                        line4 = lines[i+3].replace('HIS','CYS')
                        line5 = lines[i+4].replace('HIS','CYS')
                        line_a = lines[i+5].replace('CG  HIS','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "ILE":
                        mutation_AA = []
                        line1 = lines[i].replace('ILE','CYS')
                        line2 = lines[i+1].replace('ILE','CYS')
                        line3 = lines[i+2].replace('ILE','CYS')
                        line4 = lines[i+3].replace('ILE','CYS')
                        line5 = lines[i+4].replace('ILE','CYS')
                        line_a = lines[i+5].replace('CG1 ILE','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break
                    elif lines[i][17:20].strip() == "LEU":
                        mutation_AA = []
                        line1 = lines[i].replace('LEU','CYS')
                        line2 = lines[i+1].replace('LEU','CYS')
                        line3 = lines[i+2].replace('LEU','CYS')
                        line4 = lines[i+3].replace('LEU','CYS')
                        line5 = lines[i+4].replace('LEU','CYS')
                        line_a = lines[i+5].replace('CG  LEU','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "LYS":
                        mutation_AA = []
                        line1 = lines[i].replace('LYS','CYS')
                        line2 = lines[i+1].replace('LYS','CYS')
                        line3 = lines[i+2].replace('LYS','CYS')
                        line4 = lines[i+3].replace('LYS','CYS')
                        line5 = lines[i+4].replace('LYS','CYS')
                        line_a = lines[i+5].replace('CG  LYS','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "MET":
                        mutation_AA = []
                        line1 = lines[i].replace('MET','CYS')
                        line2 = lines[i+1].replace('MET','CYS')
                        line3 = lines[i+2].replace('MET','CYS')
                        line4 = lines[i+3].replace('MET','CYS')
                        line5 = lines[i+4].replace('MET','CYS')
                        line_a = lines[i+5].replace('CG  MET','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "PHE":
                        mutation_AA = []
                        line1 = lines[i].replace('PHE','CYS')
                        line2 = lines[i+1].replace('PHE','CYS')
                        line3 = lines[i+2].replace('PHE','CYS')
                        line4 = lines[i+3].replace('PHE','CYS')
                        line5 = lines[i+4].replace('PHE','CYS')
                        line_a = lines[i+5].replace('CG  PHE','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break
                    elif lines[i][17:20].strip() == "PRO":
                        mutation_AA = []
                        line1 = lines[i].replace('PRO','CYS')
                        line2 = lines[i+1].replace('PRO','CYS')
                        line3 = lines[i+2].replace('PRO','CYS')
                        line4 = lines[i+3].replace('PRO','CYS')
                        line5 = lines[i+4].replace('PRO','CYS')
                        line_a = lines[i+5].replace('CD  PRO','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "SER":
                        mutation_AA = []
                        line1 = lines[i].replace('SER','CYS')
                        line2 = lines[i+1].replace('SER','CYS')
                        line3 = lines[i+2].replace('SER','CYS')
                        line4 = lines[i+3].replace('SER','CYS')
                        line5 = lines[i+4].replace('SER','CYS')
                        line_a = lines[i+5].replace('OG  SER','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "THR":
                        mutation_AA = []
                        line1 = lines[i].replace('THR','CYS')
                        line2 = lines[i+1].replace('THR','CYS')
                        line3 = lines[i+2].replace('THR','CYS')
                        line4 = lines[i+3].replace('THR','CYS')
                        line5 = lines[i+4].replace('THR','CYS')
                        line_a = lines[i+5].replace('OG1 THR','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "TRP":
                        mutation_AA = []
                        line1 = lines[i].replace('TRP','CYS')
                        line2 = lines[i+1].replace('TRP','CYS')
                        line3 = lines[i+2].replace('TRP','CYS')
                        line4 = lines[i+3].replace('TRP','CYS')
                        line5 = lines[i+4].replace('TRP','CYS')
                        line_a = lines[i+5].replace('CG  TRP','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "TYR":
                        mutation_AA = []
                        line1 = lines[i].replace('TYR','CYS')
                        line2 = lines[i+1].replace('TYR','CYS')
                        line3 = lines[i+2].replace('TYR','CYS')
                        line4 = lines[i+3].replace('TYR','CYS')
                        line5 = lines[i+4].replace('TYR','CYS')
                        line_a = lines[i+5].replace('CG  TYR','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break

                    elif lines[i][17:20].strip() == "VAL":
                        mutation_AA = []
                        line1 = lines[i].replace('VAL','CYS')
                        line2 = lines[i+1].replace('VAL','CYS')
                        line3 = lines[i+2].replace('VAL','CYS')
                        line4 = lines[i+3].replace('VAL','CYS')
                        line5 = lines[i+4].replace('VAL','CYS')
                        line_a = lines[i+5].replace('CG1 VAL','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        mutation_AA.append(line1)
                        mutation_AA.append(line2)
                        mutation_AA.append(line3)
                        mutation_AA.append(line4)
                        mutation_AA.append(line5)
                        mutation_AA.append(line6)
                        break
                   #mutation_AA.close()
            i += 1
    return mutation_AA
