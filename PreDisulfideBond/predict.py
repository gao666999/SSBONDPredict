# -*- coding: utf-8 -*-
from SSBOND import process_loadedpdb
from SSBOND import noSG_restore_fnn
import argparse
import os
import sys
import numpy as np
import calculate_energy
import sort_dict
import generate_mutated_pdb as GMP
import warnings
import logging

logging.getLogger('tensorflow').setLevel(logging.FATAL)
def get_abspath():
    old_abspath=os.path.abspath(__file__).split('/')
    newpath=''
    for partpath in old_abspath[:-1]:
        newpath=newpath + partpath +'/'
    #new_abspath=os.path.jin(newpath,targetpath)
    return newpath

def predict_pairs(datafile,PositionOfThisProject):
    # predict the residue pairs that can form disulfide bonds after mutations.
    result_dict = process_loadedpdb.process_pdb(datafile,PositionOfThisProject)
    for key,value in result_dict.items():
            print (key,value)
    return result_dict

def predict_energy(datafile,PositionOfThisProject):
    filename = datafile
    energy_filename = os.path.join(PositionOfThisProject,'SSBONDPredict/PreDisulfideBond/Nepre/radius.npy')
    result_dict = process_loadedpdb.process_pdb(datafile,PositionOfThisProject)
    result_dict = calculate_energy.energy(datafile,result_dict, energy_filename)
    for key,value in result_dict.items():
            print (key,value)
    return result_dict
def save_result(datafile,PositionOfThisProject,filename, output_path='./'):
    #filename = datafile
    result_dict1 = process_loadedpdb.process_pdb(datafile,PositionOfThisProject)
    energy_filename = os.path.join(PositionOfThisProject,'SSBONDPredict/PreDisulfideBond/Nepre/radius.npy')
    result_dict2 = calculate_energy.energy(datafile,result_dict1, energy_filename)
    resultPosition,output_path = sort_dict.sort_dict(PositionOfThisProject,filename,result_dict1, output_path=output_path)
    for key,value in result_dict2.items():
            print (key,value)
    print ('the predict result are saved in :', output_path)
    return result_dict1,output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', metavar='datafile', type=str, help='Structure in .pdb format')
    parser.add_argument('position', metavar='position', type=str, help='The path to this SSBONDPredict (to the folder that contains PreDisulfideBond) ')
    parser.add_argument('output', metavar='output', type=str, default='./', help='the output folder')
    parser.add_argument('-g', '--generate', action='store_true', help=' generate the pdb files after mutation')
    args = parser.parse_args()
    filename = args.datafile.split('/')[-1].strip()
    output_path=args.output
    if args.generate:
        result,output_path = save_result(args.datafile,args.position,filename, output_path=output_path)
        #resultPosition,output_path = sort_dict.sort_dict(PositionOfThisProject,filename,result_dict2)
        GMP.generate_mutated_pdb(args.datafile,output_path,result)
    else:
        result,output_path = save_result(args.datafile,args.position,filename, output_path=output_path)

