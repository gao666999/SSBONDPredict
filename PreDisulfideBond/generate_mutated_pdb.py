import re,os
import rmsd
import create_position as CP
from Nepre import Nepre_v2
from Nepre import AminoAcid
def generate_mutated_pdb(datafile,basepath,result):
    path = basepath + 'mutatedpdb/'
    if os.path.exists(path) == False:
        os.makedirs(path)
    for pairs in result.keys():
        pairs = pairs.split('-')
        wildtype_name1 = pairs[0][:3].strip()
        idnumber1 = pairs[0][4:].strip()
        chainid1 = pairs[0][3:4]
        wildtype_name2 = pairs[1][:3].strip()
        idnumber2 = pairs[1][4:].strip()
        chainid2 = pairs[0][3:4]
        create_new_pdb(datafile, wildtype_name1,idnumber1,chainid1,wildtype_name2,idnumber2, chainid2, path)

def create_new_pdb(datafile, wildtype_name1,idnumber1,chainid1,wildtype_name2,idnumber2, chainid2, path):
    new_pdb = path + wildtype_name1 + '-' + wildtype_name2 + ".pdb"
    if os.path.exists(new_pdb):
        os.remove(new_pdb)
    f2 = open(new_pdb,'a+')
    with open(datafile, 'r') as f1:
        lines = f1.readlines()
        lenth = len(lines)
        i = 0
        while i < lenth:
            line_tag = lines[i][:6].strip()
            if line_tag == 'ATOM':
                #if lines[i][22:27].strip() == change_number1:
                if lines[i][17:20].strip() == wildtype_name1 and lines[i][20:22].strip() == chainid1 and lines[i][22:27].strip() == idnumber1:
                    if lines[i][17:20].strip() == "CYS":
                        f2.write(lines[i])
                        f2.write(lines[i + 1])
                        f2.write(lines[i + 2])
                        f2.write(lines[i + 3])
                        f2.write(lines[i + 4])
                        f2.write(lines[i + 5])
                        i += 6
                        continue
                    elif lines[i][17:20].strip() == "ALA":
                        position = CP.xyz5_position(i,lines)
                        line1 = lines[i].replace('ALA','CYS')
                        line2 = lines[i+1].replace('ALA','CYS')
                        line3 = lines[i+2].replace('ALA','CYS')
                        line4 = lines[i+3].replace('ALA','CYS')
                        line5 = lines[i+4].replace('ALA','CYS')
                        line6_s1 = lines[i+4][:30].replace('CB  ALA','SG  CYS')
                        line6_s2 = lines[i+4][54:].replace('C','S')
                        line6 = line6_s1 + position + line6_s2
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        # create line6 and add into the file
                        i += 5
                        continue
                    elif lines[i][17:20].strip() == "ARG":
                        line1 = lines[i].replace('ARG','CYS')
                        line2 = lines[i+1].replace('ARG','CYS')
                        line3 = lines[i+2].replace('ARG','CYS')
                        line4 = lines[i+3].replace('ARG','CYS')
                        line5 = lines[i+4].replace('ARG','CYS')
                        line_a = lines[i+5].replace('CG  ARG','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        #line6 = line_a.replace('C','S')
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 11
                        continue
                    elif lines[i][17:20].strip() == "ASN":
                        line1 = lines[i].replace('ASN','CYS')
                        line2 = lines[i+1].replace('ASN','CYS')
                        line3 = lines[i+2].replace('ASN','CYS')
                        line4 = lines[i+3].replace('ASN','CYS')
                        line5 = lines[i+4].replace('ASN','CYS')
                        line_a = lines[i+5].replace('CG  ASN','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 8
                        continue
                    elif lines[i][17:20].strip() == "ASP":
                        line1 = lines[i].replace('ASP','CYS')
                        line2 = lines[i+1].replace('ASP','CYS')
                        line3 = lines[i+2].replace('ASP','CYS')
                        line4 = lines[i+3].replace('ASP','CYS')
                        line5 = lines[i+4].replace('ASP','CYS')
                        line_a = lines[i+5].replace('CG  ASP','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 8
                        continue
                    elif lines[i][17:20].strip() == "GLN":
                        line1 = lines[i].replace('GLN','CYS')
                        line2 = lines[i+1].replace('GLN','CYS')
                        line3 = lines[i+2].replace('GLN','CYS')
                        line4 = lines[i+3].replace('GLN','CYS')
                        line5 = lines[i+4].replace('GLN','CYS')
                        line_a = lines[i+5].replace('CG  GLN','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 9
                        continue
                    elif lines[i][17:20].strip() == "GLU":
                        line1 = lines[i].replace('GLU','CYS')
                        line2 = lines[i+1].replace('GLU','CYS')
                        line3 = lines[i+2].replace('GLU','CYS')
                        line4 = lines[i+3].replace('GLU','CYS')
                        line5 = lines[i+4].replace('GLU','CYS')
                        line_a = lines[i+5].replace('CG  GLU','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 9
                        continue
                    elif lines[i][17:20].strip() == "GLY":
                        position5,position6 = CP.xyz4a_position(i,lines)
                        #position6 = pc.xyz4b_position(i,lines)
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
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 4
                        continue
                    elif lines[i][17:20].strip() == "HIS":
                        line1 = lines[i].replace('HIS','CYS')
                        line2 = lines[i+1].replace('HIS','CYS')
                        line3 = lines[i+2].replace('HIS','CYS')
                        line4 = lines[i+3].replace('HIS','CYS')
                        line5 = lines[i+4].replace('HIS','CYS')
                        line_a = lines[i+5].replace('CG  HIS','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 10
                        continue
                    elif lines[i][17:20].strip() == "ILE":
                        line1 = lines[i].replace('ILE','CYS')
                        line2 = lines[i+1].replace('ILE','CYS')
                        line3 = lines[i+2].replace('ILE','CYS')
                        line4 = lines[i+3].replace('ILE','CYS')
                        line5 = lines[i+4].replace('ILE','CYS')
                        line_a = lines[i+5].replace('CG1 ILE','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 8
                        continue
                    elif lines[i][17:20].strip() == "LEU":
                        line1 = lines[i].replace('LEU','CYS')
                        line2 = lines[i+1].replace('LEU','CYS')
                        line3 = lines[i+2].replace('LEU','CYS')
                        line4 = lines[i+3].replace('LEU','CYS')
                        line5 = lines[i+4].replace('LEU','CYS')
                        line_a = lines[i+5].replace('CG  LEU','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 8
                        continue
                    elif lines[i][17:20].strip() == "LYS":
                        line1 = lines[i].replace('LYS','CYS')
                        line2 = lines[i+1].replace('LYS','CYS')
                        line3 = lines[i+2].replace('LYS','CYS')
                        line4 = lines[i+3].replace('LYS','CYS')
                        line5 = lines[i+4].replace('LYS','CYS')
                        line_a = lines[i+5].replace('CG  LYS','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 9
                        continue
                    elif lines[i][17:20].strip() == "MET":
                        line1 = lines[i].replace('MET','CYS')
                        line2 = lines[i+1].replace('MET','CYS')
                        line3 = lines[i+2].replace('MET','CYS')
                        line4 = lines[i+3].replace('MET','CYS')
                        line5 = lines[i+4].replace('MET','CYS')
                        line_a = lines[i+5].replace('CG  MET','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 8
                        continue
                    elif lines[i][17:20].strip() == "PHE":
                        line1 = lines[i].replace('PHE','CYS')
                        line2 = lines[i+1].replace('PHE','CYS')
                        line3 = lines[i+2].replace('PHE','CYS')
                        line4 = lines[i+3].replace('PHE','CYS')
                        line5 = lines[i+4].replace('PHE','CYS')
                        line_a = lines[i+5].replace('CG  PHE','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 11
                        continue
                    elif lines[i][17:20].strip() == "PRO":
                        line1 = lines[i].replace('PRO','CYS')
                        line2 = lines[i+1].replace('PRO','CYS')
                        line3 = lines[i+2].replace('PRO','CYS')
                        line4 = lines[i+3].replace('PRO','CYS')
                        line5 = lines[i+4].replace('PRO','CYS')
                        line_a = lines[i+5].replace('CD  PRO','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 7
                        continue
                    elif lines[i][17:20].strip() == "SER":
                        line1 = lines[i].replace('SER','CYS')
                        line2 = lines[i+1].replace('SER','CYS')
                        line3 = lines[i+2].replace('SER','CYS')
                        line4 = lines[i+3].replace('SER','CYS')
                        line5 = lines[i+4].replace('SER','CYS')
                        line_a = lines[i+5].replace('OG  SER','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 6
                        continue
                    elif lines[i][17:20].strip() == "THR":
                        line1 = lines[i].replace('THR','CYS')
                        line2 = lines[i+1].replace('THR','CYS')
                        line3 = lines[i+2].replace('THR','CYS')
                        line4 = lines[i+3].replace('THR','CYS')
                        line5 = lines[i+4].replace('THR','CYS')
                        line_a = lines[i+5].replace('OG1 THR','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 7
                        continue
                    elif lines[i][17:20].strip() == "TRP":
                        line1 = lines[i].replace('TRP','CYS')
                        line2 = lines[i+1].replace('TRP','CYS')
                        line3 = lines[i+2].replace('TRP','CYS')
                        line4 = lines[i+3].replace('TRP','CYS')
                        line5 = lines[i+4].replace('TRP','CYS')
                        line_a = lines[i+5].replace('CG  TRP','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 14
                        continue
                    elif lines[i][17:20].strip() == "TYR":
                        line1 = lines[i].replace('TYR','CYS')
                        line2 = lines[i+1].replace('TYR','CYS')
                        line3 = lines[i+2].replace('TYR','CYS')
                        line4 = lines[i+3].replace('TYR','CYS')
                        line5 = lines[i+4].replace('TYR','CYS')
                        line_a = lines[i+5].replace('CG  TYR','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 12
                        continue
                    elif lines[i][17:20].strip() == "VAL":
                        line1 = lines[i].replace('VAL','CYS')
                        line2 = lines[i+1].replace('VAL','CYS')
                        line3 = lines[i+2].replace('VAL','CYS')
                        line4 = lines[i+3].replace('VAL','CYS')
                        line5 = lines[i+4].replace('VAL','CYS')
                        line_a = lines[i+5].replace('CG1 VAL','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 7
                        continue
                elif lines[i][17:20].strip() == wildtype_name2 and lines[i][20:22].strip() == chainid2 and lines[i][22:27].strip() == idnumber2:
                    if lines[i][17:20].strip() == "CYS":
                        f2.write(lines[i])
                        f2.write(lines[i + 1])
                        f2.write(lines[i + 2])
                        f2.write(lines[i + 3])
                        f2.write(lines[i + 4])
                        f2.write(lines[i + 5])
                        i += 6
                        continue
                    elif lines[i][17:20].strip() == "ALA":
                        position = CP.xyz5_position(i,lines)
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
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 5
                        continue
                    elif lines[i][17:20].strip() == "ARG":
                        line1 = lines[i].replace('ARG','CYS')
                        line2 = lines[i+1].replace('ARG','CYS')
                        line3 = lines[i+2].replace('ARG','CYS')
                        line4 = lines[i+3].replace('ARG','CYS')
                        line5 = lines[i+4].replace('ARG','CYS')
                        line_a = lines[i+5].replace('CG  ARG','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 11
                        continue
                    elif lines[i][17:20].strip() == "ASN":
                        line1 = lines[i].replace('ASN','CYS')
                        line2 = lines[i+1].replace('ASN','CYS')
                        line3 = lines[i+2].replace('ASN','CYS')
                        line4 = lines[i+3].replace('ASN','CYS')
                        line5 = lines[i+4].replace('ASN','CYS')
                        line_a = lines[i+5].replace('CG  ASN','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 8
                        continue
                    elif lines[i][17:20].strip() == "ASP":
                        line1 = lines[i].replace('ASP','CYS')
                        line2 = lines[i+1].replace('ASP','CYS')
                        line3 = lines[i+2].replace('ASP','CYS')
                        line4 = lines[i+3].replace('ASP','CYS')
                        line5 = lines[i+4].replace('ASP','CYS')
                        line_a = lines[i+5].replace('CG  ASP','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 8
                        continue
                    elif lines[i][17:20].strip() == "GLN":
                        line1 = lines[i].replace('GLN','CYS')
                        line2 = lines[i+1].replace('GLN','CYS')
                        line3 = lines[i+2].replace('GLN','CYS')
                        line4 = lines[i+3].replace('GLN','CYS')
                        line5 = lines[i+4].replace('GLN','CYS')
                        line_a = lines[i+5].replace('CG  GLN','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 9
                        continue
                    elif lines[i][17:20].strip() == "GLU":
                        line1 = lines[i].replace('GLU','CYS')
                        line2 = lines[i+1].replace('GLU','CYS')
                        line3 = lines[i+2].replace('GLU','CYS')
                        line4 = lines[i+3].replace('GLU','CYS')
                        line5 = lines[i+4].replace('GLU','CYS')
                        line_a = lines[i+5].replace('CG  GLU','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 9
                        continue
                    elif lines[i][17:20].strip() == "GLY":
                        #a = i
                        #number5 = pc.xyz4_position(a)
                        position5,position6= CP.xyz4a_position(i,lines)
                        #position6 = pc.xyz4b_position(i,lines)
                        line1 = lines[i].replace('GLY','CYS')
                        line2 = lines[i+1].replace('GLY','CYS')
                        line3 = lines[i+2].replace('GLY','CYS')
                        line4 = lines[i+3].replace('GLY','CYS')
                        line5_s1 = lines[i+3][:30].replace('O   GLY','CB  CYS')
                        line5_s2 = lines[i+3][54:].replace('O','C')
                        line5 = line5_s1 +position5 +line5_s2
                        #create line6
                        line6_s1 = lines[i+3][:30].replace('SG  GLY','CB  CYS')
                        line6_s2 = lines[i+3][54:].replace('O','S')
                        #print s1,s2
                        line6 = line6_s1 + position6 + line6_s2
                        #print s3
                        #f3.write(s3)
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 4
                        continue
                    elif lines[i][17:20].strip() == "HIS":
                        line1 = lines[i].replace('HIS','CYS')
                        line2 = lines[i+1].replace('HIS','CYS')
                        line3 = lines[i+2].replace('HIS','CYS')
                        line4 = lines[i+3].replace('HIS','CYS')
                        line5 = lines[i+4].replace('HIS','CYS')
                        line_a = lines[i+5].replace('CG  HIS','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 10
                        continue
                    elif lines[i][17:20].strip() == "ILE":
                        line1 = lines[i].replace('ILE','CYS')
                        line2 = lines[i+1].replace('ILE','CYS')
                        line3 = lines[i+2].replace('ILE','CYS')
                        line4 = lines[i+3].replace('ILE','CYS')
                        line5 = lines[i+4].replace('ILE','CYS')
                        line_a = lines[i+5].replace('CG1 ILE','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 8
                        continue
                    elif lines[i][17:20].strip() == "LEU":
                        line1 = lines[i].replace('LEU','CYS')
                        line2 = lines[i+1].replace('LEU','CYS')
                        line3 = lines[i+2].replace('LEU','CYS')
                        line4 = lines[i+3].replace('LEU','CYS')
                        line5 = lines[i+4].replace('LEU','CYS')
                        line_a = lines[i+5].replace('CG  LEU','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 8
                        continue
                    elif lines[i][17:20].strip() == "LYS":
                        line1 = lines[i].replace('LYS','CYS')
                        line2 = lines[i+1].replace('LYS','CYS')
                        line3 = lines[i+2].replace('LYS','CYS')
                        line4 = lines[i+3].replace('LYS','CYS')
                        line5 = lines[i+4].replace('LYS','CYS')
                        line_a = lines[i+5].replace('CG  LYS','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 9
                        continue
                    elif lines[i][17:20].strip() == "MET":
                        line1 = lines[i].replace('MET','CYS')
                        line2 = lines[i+1].replace('MET','CYS')
                        line3 = lines[i+2].replace('MET','CYS')
                        line4 = lines[i+3].replace('MET','CYS')
                        line5 = lines[i+4].replace('MET','CYS')
                        line_a = lines[i+5].replace('CG  MET','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 8
                        continue
                    elif lines[i][17:20].strip() == "PHE":
                        line1 = lines[i].replace('PHE','CYS')
                        line2 = lines[i+1].replace('PHE','CYS')
                        line3 = lines[i+2].replace('PHE','CYS')
                        line4 = lines[i+3].replace('PHE','CYS')
                        line5 = lines[i+4].replace('PHE','CYS')
                        line_a = lines[i+5].replace('CG  PHE','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 11
                        continue
                    elif lines[i][17:20].strip() == "PRO":
                        line1 = lines[i].replace('PRO','CYS')
                        line2 = lines[i+1].replace('PRO','CYS')
                        line3 = lines[i+2].replace('PRO','CYS')
                        line4 = lines[i+3].replace('PRO','CYS')
                        line5 = lines[i+4].replace('PRO','CYS')
                        line_a = lines[i+5].replace('CD  PRO','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 7
                        continue
                    elif lines[i][17:20].strip() == "SER":
                        line1 = lines[i].replace('SER','CYS')
                        line2 = lines[i+1].replace('SER','CYS')
                        line3 = lines[i+2].replace('SER','CYS')
                        line4 = lines[i+3].replace('SER','CYS')
                        line5 = lines[i+4].replace('SER','CYS')
                        line_a = lines[i+5].replace('OG  SER','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 6
                        continue
                    elif lines[i][17:20].strip() == "THR":
                        line1 = lines[i].replace('THR','CYS')
                        line2 = lines[i+1].replace('THR','CYS')
                        line3 = lines[i+2].replace('THR','CYS')
                        line4 = lines[i+3].replace('THR','CYS')
                        line5 = lines[i+4].replace('THR','CYS')
                        line_a = lines[i+5].replace('OG1 THR','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 7
                        continue
                    elif lines[i][17:20].strip() == "TRP":
                        line1 = lines[i].replace('TRP','CYS')
                        line2 = lines[i+1].replace('TRP','CYS')
                        line3 = lines[i+2].replace('TRP','CYS')
                        line4 = lines[i+3].replace('TRP','CYS')
                        line5 = lines[i+4].replace('TRP','CYS')
                        line_a = lines[i+5].replace('CG  TRP','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 14
                        continue
                    elif lines[i][17:20].strip() == "TYR":
                        line1 = lines[i].replace('TYR','CYS')
                        line2 = lines[i+1].replace('TYR','CYS')
                        line3 = lines[i+2].replace('TYR','CYS')
                        line4 = lines[i+3].replace('TYR','CYS')
                        line5 = lines[i+4].replace('TYR','CYS')
                        line_a = lines[i+5].replace('CG  TYR','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 12
                        continue
                    elif lines[i][17:20].strip() == "VAL":
                        line1 = lines[i].replace('VAL','CYS')
                        line2 = lines[i+1].replace('VAL','CYS')
                        line3 = lines[i+2].replace('VAL','CYS')
                        line4 = lines[i+3].replace('VAL','CYS')
                        line5 = lines[i+4].replace('VAL','CYS')
                        line_a = lines[i+5].replace('CG1 VAL','SG  CYS')
                        line6 = '%sS%s'%(line_a[:77],line_a[78:])
                        f2.write(line1)
                        f2.write(line2)
                        f2.write(line3)
                        f2.write(line4)
                        f2.write(line5)
                        f2.write(line6)
                        i += 7
                        continue
                else:
                    f2.write(lines[i])
                    i += 1
            elif line_tag == "END":
                f2.write(lines[i])
                break
            else:
                f2.write(lines[i])
                i += 1
    f2.close()
    return new_pdb