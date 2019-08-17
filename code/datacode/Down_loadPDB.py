#-*- coding: utf-8 -*-
'''
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import JsonResponse
from backend import process_loadedpdb
import json
import os
from django.views.decorators import csrf
from django.http import FileResponse
import chardet
'''
import copy
import numpy as np
import httplib
import urllib2
import os

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
                    #url = 'https://www.rcsb.org/structure/'+PdbID+'.pdb'
                    try:
                        fpdb = urllib2.urlopen(url)
                        data = fpdb.readlines()
                        #pdbfile = os.path.join(datasetpath,PdbID+str('.pdb'))
                        #downloadpdb = "media/%s.pdb"%PdbID#add the name into the filename
                        print(pdbfile)
                        with open(pdbfile, "wb") as code:
                            code.writelines(data)
                        #'https://www.rcsb.org/structure/1AGJ'
                    except:
                        f2=open('./filename30.txt','a+')
                        print >> f2, PdbID
                        f2.close()
if __name__ == '__main__':
    filepath ='/Users/dongxq/Desktop/SSBOND_supplement/'
    #filename ='cullpdb_pc30_res2.0_R0.25_d190801_chains12021'
    filename = 'filename40.txt'
    file = os.path.join(filepath,filename)
    datasetpath='/Users/dongxq/Desktop/SSBOND_supplement/Dataset40'
    getFilenames(file,datasetpath)

