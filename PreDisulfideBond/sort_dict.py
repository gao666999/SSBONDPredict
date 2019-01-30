import os
from time import time,localtime,strftime
import pandas as pd
def sort_dict(path,filename,dict1, output_path='./'):
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
    basepath = output_path + '/SSBOND-Result-'+filename[:4] + '/'
    if os.path.exists(basepath):
        Position = basepath + 'result.xlsx'
    else:
        os.makedirs(basepath)
        Position = basepath + 'result.xlsx'
    Position = basepath + 'result.xlsx'
    writer = pd.ExcelWriter(Position)
    df_pb.to_excel(writer, sheet_name = 'probability')
    df_ep.to_excel(writer, sheet_name = 'entropy')
    df_en.to_excel(writer, sheet_name = 'energy')
    writer.save()
    os.rename(os.path.join(basepath,'result.xlsx'),os.path.join(basepath,filename + '.xlsx'))
    resultPosition = basepath + filename +'.xlsx'
    # 'the result are saved in :',resultPosition
    return resultPosition,basepath
    #print df_pb
