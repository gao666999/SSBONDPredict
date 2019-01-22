# -*- coding: utf-8 -*-
from SSBOND import process_loadedpdb
from SSBOND import noSG_restore_fnn
import argparse
import json
import os
import sys
import chardet
import copy
import numpy as np
import calculate_energy
import sort_dict
import generate_mutated_pdb as GMP
def predict_pairs(datafile,PositionOfThisProject):
    # predict the residue pairs that can form disulfide bonds after mutations.
    result_dict = process_loadedpdb.process_pdb1(datafile,PositionOfThisProject)
    for key,value in result_dict.items():
            print key,value
    return result_dict

def predict_energy(datafile,PositionOfThisProject):
    filename = datafile
    result_dict = process_loadedpdb.process_pdb1(datafile,PositionOfThisProject)
    result_dict = calculate_energy.energy(datafile,result_dict)
    for key,value in result_dict.items():
            print key,value
    return result_dict
def save_result(datafile,PositionOfThisProject,filename):
    #filename = datafile
    result_dict1 = process_loadedpdb.process_pdb1(datafile,PositionOfThisProject)
    result_dict2 = calculate_energy.energy(datafile,result_dict1)
    resultPosition,basepath = sort_dict.sort_dict(PositionOfThisProject,filename,result_dict2)
    for key,value in result_dict2.items():
            print key,value
    print 'the predict result are saved in :',basepath
    return result_dict1,basepath

#def generate_mutated_pdb(datafile,PositionOfThisProject):


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', metavar='datafile', type=str, help='Structure in .pdb format')
    parser.add_argument('position', metavar='position', type=str, help='the position of this project in your computer')
    parser.add_argument('-g', '--generate', action='store_true', help=' generate the pdb files after mutation')
    args = parser.parse_args()
    #args = sys.argv[1:]
    #datafile = args[0]
    filename = args.datafile.split('/')[-1].strip()
    #PositionOfThisProject = args[1]
    #print 'Do you want generate the mutated pdb?（it may be need a little time,but believe that it is worthy）'
    #print'if you want please input\'Yes\' or input \'No\''
    #option = input('Please input \'Yes\' or\' No\':')
    #print option
    if args.generate:
        result,basepath = save_result(args.datafile,args.position,filename)
        #resultPosition,basepath = sort_dict.sort_dict(PositionOfThisProject,filename,result_dict2)
        GMP.generate_mutated_pdb(args.datafile,basepath,result)
    else:
        result,basepath = save_result(args.datafile,args.position,filename)

