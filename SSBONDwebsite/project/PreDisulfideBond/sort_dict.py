import os
import shutil
from time import time,localtime,strftime
import pandas as pd
def sort_dict(dict1):
    keys = dict1.keys()
    value = dict1.values()
    pb = []
    ep = []
    en = []
    for i in value:
        pb.append(float(i.split(' ')[0]))
        ep.append(float(i.split(' ')[1]))
        en.append(float(i.split(' ')[2]))
    s0 = pd.Series(keys)
    s1 = pd.Series(pb)
    s2 = pd.Series(ep)
    s3 = pd.Series(en)
    df = pd.DataFrame({"key":s0,"probability":s1,"entropy":s2,"energy":s3})
    cols = ["key", "probability", "entropy", "energy"]
    df = df.ix[:,cols]
    #print df
    df_pb = df.sort_values(by = "probability", axis = 0, ascending = False)
    df_ep = df.sort_values(by = "entropy", axis = 0, ascending = False)
    df_en = df.sort_values(by = "energy", axis = 0, ascending = False)
    path = './media/result/'
    #del_file(path)
    shutil.rmtree(path)
    os.mkdir(path)
    writer = pd.ExcelWriter('./media/result/result.xlsx')
    #writer = pd.ExcelWriter('/Users/xg666/Desktop/xqdongV2/project/media/result/result.xlsx')

    df_pb.to_excel(writer, sheet_name = 'probability')
    df_ep.to_excel(writer, sheet_name = 'entropy')
    df_en.to_excel(writer, sheet_name = 'energy')
    writer.save()
    #base_path ="media/result"
    #path = '/Users/xg666/Desktop/xqdongV2/project/media/result/'
    #for file in os.listdir(path):
    #os.rename(os.path.join(path,'result.xlsx'),os.path.join(path,filename + '.xlsx'))
    #print df_pb
    return 1

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

