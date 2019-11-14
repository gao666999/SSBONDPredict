# -*-coding:utf-8-*-
import numpy as np
from scipy.spatial.distance import pdist
import scipy.spatial.distance as ssd
import sys


def convert_to_nxn_map(ssbonds_map):
    errorcount = 0
    ssbonds_distance_map = []
    pos = 0
    for smapi in range(len(ssbonds_map)):
        try:
            Y = pdist(ssbonds_map[smapi], 'euclidean')
            ssbonds_distance_map.append(ssd.squareform(Y))
        except ValueError:
            errorcount += 1
            with open('ssbond_map_error.txt','a') as wf:
                wf.write(str(ssbonds_map[smapi]))
                wf.write('\n')
            for xyz in ssbonds_map[smapi]:
                if abs(len(xyz[0])-len(xyz[1])) <= 1:
                    continue
                if len(xyz[0]) > len(xyz[1]):
                    pos = 0
                else:
                    pos = 1
                temp = xyz[pos].split('-')
                if pos == 0:
                    xyz[pos+2] = xyz[pos+1]
                    if temp[0] == '':
                        xyz[pos] = float('-'+temp[1])
                        xyz[pos+1] = float('-'+temp[2])
                    else:
                        xyz[pos] = float(temp[0])
                        xyz[pos+1] = float('-'+temp[1])
                else:
                    if temp[0] == '':
                        xyz[pos] = float('-'+temp[1])
                        xyz[pos+1] = float('-'+temp[2])
                    else:
                        xyz[pos] = float(temp[0])
                        xyz[pos+1] = float('-'+temp[1])
            with open('ssbond_map_correct_error.txt','a') as wcf:
                wcf.write(str(ssbonds_map[smapi]))
                wcf.write('\n')
                wcf.write('***************************************\n')
            Y = pdist(ssbonds_map[smapi], 'euclidean')
            ssbonds_distance_map.append(ssd.squareform(Y))
    return ssbonds_distance_map

if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    name = args[0].split('/')[-1].split('.')[0]
    root_path = '/Users/dongxq/Desktop/disulfide/new-nossbond-map/'
    ssbonds_map = np.load(root_path + name + '.npy')
    ssbonds_distance_map = convert_to_nxn_map(ssbonds_map)
    np.save('%s_distance.npy'%name,ssbonds_distance_map)
