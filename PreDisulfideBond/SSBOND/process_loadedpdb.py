# -*-coding:utf-8 -*-
# from __future__ import unicode_literals
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

from . import extract_unknown_map
from . import ssbond_distance_map as sdm
import tensorflow as tf
import sys
import argparse
import numpy as np
from . import noSG_restore_fnn
import operator
from collections import OrderedDict
import os
import warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings('ignore')
def process_pdb(args,PositionOfThisProject):
    name = args.split('/')[-1].split('.')[0]
    map_list, map_id ,mol_type_list=extract_unknown_map.find_map_element(args)
    if map_list == []:
        print ('no bonds')
        return False
    possible_ssbond, possible_ssbond_id = extract_unknown_map.make_ssbond_without_repeat(map_list, map_id, mol_type_list)
    full_distance_map = sdm.convert_to_nxn_map(np.array(possible_ssbond))
    print ('canditate bonds',len(full_distance_map))
    predict_path = np.array(full_distance_map)
    predict_ord_path = np.array(possible_ssbond_id)
    result_dict = noSG_restore_fnn.main([predict_path,predict_ord_path,name],PositionOfThisProject)
    #noSG_restore_fnn.set_pointdir(PositionOfThisProject)
    sorted_result_dict = sorted(result_dict.items(), key=operator.itemgetter(1), reverse=True)
    final_dict = sorted_result_dict
    final_dict = OrderedDict()
    for item in sorted_result_dict:
        final_dict[item[0]] = item[1]
    return final_dict
#read the result_dict and save it in a new file
