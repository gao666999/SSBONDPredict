import os
import sys
import chardet
import copy
import numpy as np
import calculate_energy
import sort_dict
import generate_mutated_pdb as GMP

def get_abspath():
    old_abspath=os.path.abspath(__file__).split('/')
    newpath=''
    for partpath in old_abspath[:-2]:
        newpath=newpath + partpath +'/'
    #new_abspath=os.path.jin(newpath,targetpath)
    return newpath

if __name__ == '__main__':
    path= get_abspath()
    print path