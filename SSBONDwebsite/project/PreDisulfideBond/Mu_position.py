import rmsd
import numpy as np
import sys
# this function can produce the sixth position for redius who only have 5 atoms
def xyz5_position(i,lines):
    template1 = np.array([[-0.93454, 0.91954, 1.11786],
    [-0.01675, 0.03488, 0.58954],
    [ 1.10621, 0.72253,-0.004  ],
    [ 1.6148 , 1.14817,-0.57075],
    [-0.64719,-0.82998,-0.40926]])
    template2 = np.array([[-0.93454, 0.91954, 1.11786],
    [-0.01675, 0.03488, 0.58954],
    [ 1.10621, 0.72253,-0.004  ],
    [ 1.6148 , 1.14817,-0.57075],
    [-0.64719,-0.82998,-0.40926],
    [-1.12252,-1.99515,-0.72338]])
    amino_acid_position = []
    for k in range(i, i + 5, 1):
        try:
            x = lines[k][30:38]
            y = lines[k][38:46]
            z = lines[k][46:54]
            amino_acid_position.append(np.asarray([x, y ,z], dtype=float))
        except:
            sys.exit("Error parsing input for the following line: \n{0:s}".format(lines[k]))
    amino_acid_position = np.asarray(amino_acid_position)
    #print amino_acid_position
    a_acid_p = amino_acid_position - rmsd.centroid(amino_acid_position)
    template1 -= rmsd.centroid(template1)
    #centroid P2 into f
    template2 = template2 - rmsd.centroid(template2)
    rot = rmsd.kabsch(template1,a_acid_p)
    #pp is the rotated martix,Rotate matrix P2 unto Q
    new_position = np.dot(template2,rot)
    #translation the P2 into initial position after rotation
    new_position += rmsd.centroid(amino_acid_position)
    C = new_position.tolist()
    #print new_position
    #change the martix into list
    #lenthg = len(C)
    #print lenthg
    #for n in range(0,6,1):
    position = ('%8s'%str(float('%.3f'%C[5][0]))) + ('%8s'%str(float('%.3f'%C[5][1]))) + ('%8s'%str(float('%.3f'%C[5][2])))
    return position
#GLY line5
# this function can produce the fivth position for redius who only have 4 atoms,
def xyz4a_position(i,lines):
    template1 = np.array([[-0.93454, 0.91954, 1.11786],
    [-0.01675, 0.03488, 0.58954],
    [ 1.10621, 0.72253,-0.004  ],
    [ 1.6148 , 1.14817,-0.57075]])
    template2 = np.array([[-0.93454, 0.91954, 1.11786],
    [-0.01675, 0.03488, 0.58954],
    [ 1.10621, 0.72253,-0.004  ],
    [ 1.6148 , 1.14817,-0.57075],
    [-0.64719,-0.82998,-0.40926],
    [-1.12252,-1.99515,-0.72338]])
    amino_acid_position = []
    for k in range(i, i + 4, 1):
        try:
            x = lines[k][30:38]
            y = lines[k][38:46]
            z = lines[k][46:54]
            amino_acid_position.append(np.asarray([x, y ,z], dtype=float))
        except:
            sys.exit("Error parsing input for the following line: \n{0:s}".format(lines[k]))
    amino_acid_position = np.asarray(amino_acid_position)
    #print amino_acid_position
    a_acid_p = amino_acid_position - rmsd.centroid(amino_acid_position)
    template1 -= rmsd.centroid(template1)
    #centroid P2 into f
    template2 = template2 - rmsd.centroid(template2)
    #for debug
    print '*************8888888888888888'
    #print template1.shape#(4,3)
    #print a_acid_p.shape#(5,3)
    #print template2.shape#(6.3)
    rot = rmsd.kabsch(template1,a_acid_p)
    #pp is the rotated martix,Rotate matrix P2 unto Q
    new_position = np.dot(template2,rot)
    #translation the P2 into initial position after rotation
    new_position += rmsd.centroid(amino_acid_position)
    C = new_position.tolist()
    #print new_position
    #print lenthg
    #for n in range(0,6,1):
    position5 = ('%8s'%str(float('%.3f'%C[4][0]))) + ('%8s'%str(float('%.3f'%C[4][1]))) + ('%8s'%str(float('%.3f'%C[4][2])))
    position6 = ('%8s'%str(float('%.3f'%C[5][0]))) + ('%8s'%str(float('%.3f'%C[5][1]))) + ('%8s'%str(float('%.3f'%C[5][2])))
    print 'print the position of position 5 and position 6'
    return position5,position6
