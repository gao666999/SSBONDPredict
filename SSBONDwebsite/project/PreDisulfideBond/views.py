# -*- coding: utf-8 -*-
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
import copy
import numpy as np
import httplib
import urllib2
import createMU_AA as CA
import sort_dict

def index(request):
    return render(request, 'index.html')

def simple_upload(request):
    return render(request, 'simple_upload.html')

def xlsx_download(request):
    f = open('filename.txt','r')
    lines = f.readlines()
    #lines = lines.split('\n')
    #print lines
    last_line = lines[-1]
    name = str(last_line).strip()
    #print last_line
    #print name
    filename = './media/result/result.xlsx'
    file=open(filename,'rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'#stand for binary data
    response['Content-Disposition']='attachment;filename=result.xlsx'#the name is not a variable,so we cann't change
    f.close()
    return response

def result(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        bdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        father_path=os.path.abspath(os.path.dirname(bdir)+os.path.sep+".")
        result_dict1 = process_loadedpdb.process_pdb1(father_path + uploaded_file_url)
        #print father_path + uploaded_file_url
        result_dict1 = CA.energy2(father_path + uploaded_file_url,result_dict1)
        ppp = sort_dict.sort_dict(result_dict1)
        for key,value in result_dict1.items():
            print key,value
        if result_dict1 == False:
            wrongmsg = True
            print wrongmsgs
            return render(request, 'simple_upload.html', {
                'wrongmsg': json.dumps(wrongmsg),
            })
        return render(request, 'base_result.html', {
            'uploaded_file_url': json.dumps(uploaded_file_url),
            'result_dict1': json.dumps(result_dict1),
        })
    elif request.method == 'GET':
        PdbID = request.GET['a']
        url = 'https://files.rcsb.org/download/'+ PdbID +'.pdb'
        f = urllib2.urlopen(url)
        data = f.readlines()
        downloadpdb = "media/%s.pdb"%PdbID
        #add the name into the filename
        with open(downloadpdb, "wb") as code:
            code.writelines(data)
        result_dict2 = process_loadedpdb.process_pdb1(downloadpdb)
        result_dict2 = CA.energy2(downloadpdb,result_dict2)
        ppp = sort_dict.sort_dict(result_dict2)
        for key,value in result_dict2.items():
            print key,value
        if result_dict2 == False:
            wrongmsg1 = True
            print wrongmsg1
            return render(request, 'simple_upload.html', {
                # 'reslut_dict': reslut_dict
                'wrongmsg1': json.dumps(wrongmsg1),
            })

        return render(request, 'base_result.html', {
            'uploaded_file_url': json.dumps('/'+downloadpdb),
            # 'reslut_dict': reslut_dict
            'result_dict1': json.dumps(result_dict2),
        })


def comments_upload(request):
    if request.method == 'POST':
        print "it's a test"                            #用于测试
        print request.POST['name']           #测试是否能够接收到前端发来的name字段
        print request.POST['password']     #用途同上

        return HttpResponse("表单测试成功")     #最后返会给前端的数据，如果能在前端弹出框中显示我们就成功了
    else:
        return render(request,'test.html')

def integration(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print myfile, myfile.name, upload_file_url
        # process_loadedpdb.process_pdb()
        # print uploaded_file_url
        # return HttpResponse("文件上传成功")
        # return JsonResponse(uploaded_file_url, safe=False)
        resp = "文件上传成功"
        HttpResponse(json.dumps(resp), content_type="application/json")
    # return render(request, 'simple_upload.html')
    return render(request, 'integration.html')

def result_base(request):
    List = ['自强学堂', '渲染Json到模板']
    Dict = {'site': 12.232, 'author': 13.23450}

    result_dict= process_loadedpdb.process_pdb('/Users/dongxq/Sites/project/media/brilM.pdb')
    with open('brilm1'+'.json','a') as outfile1:
        json.dump(dict1,outfile1,ensure_ascii=False)
        outfile1.write('\n')
    with open('brilm'+'.json','a') as outfile:
        json.dump(result_dict,outfile,ensure_ascii=False)
        outfile.write('\n')
    return render(request, 'result_base.html', {
            'List': json.dumps(Dict),
            'result_dict': json.dumps(result_dict),
    })
