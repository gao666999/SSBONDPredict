#-*- coding: utf-8 -*-
import copy
import numpy as np
import httplib
import urllib2
import os
import sys

def listdirInMac(path):
    os_list = os.listdir(path)
    for item in os_list:
        if item.startswith('.') and os.path.isfile(os.path.join(path, item)):
            os_list.remove(item)
    return os_list

def getFilenames(file,datasetpath):
    with open(file) as f:
        lines=f.readlines()
        for line in lines:
            if line[:4].strip() == 'IDs':
                continue
            else:
                PdbID = line[:4].strip()
                print(PdbID)
                pdbfile=os.path.join(datasetpath,PdbID+str('.pdb'))
                if os.path.exists(pdbfile):
                    continue
                else:
                    url = 'https://files.rcsb.org/download/'+ PdbID +'.pdb'
                    try:
                        fpdb = urllib2.urlopen(url)
                        data = fpdb.readlines()
                        print(pdbfile)
                        with open(pdbfile, "wb") as code:
                            code.writelines(data)
                    except:
                        f2=open('./filenamefailed.txt','a+')
                        print >> f2, PdbID
                        f2.close()
if __name__ == '__main__':
    filepath=sys.argv[1]
    filename = 'cullpdb_pc40_res2.0_R0.25_d190801_chains15139'
    file = os.path.join(filepath,filename)
    datasetpath=sys.argv[2]
    getFilenames(file,datasetpath)

