import os
import math
import numpy as np
import AminoAcid as AA
import gc
import sys
import math
import csv
#import matplotlib.pyplot as plt
#from matplotlib.pyplot import savefig


def pearson(rmsd,energy):
    size = np.shape(rmsd)[0]
    x = np.empty(shape=[2,size])
    for i in range(size):
        x[0][i] = rmsd[i]
    for j in range(size):
        x[1][j] = energy[j]
    y = np.corrcoef(x)
    return y[0][1]


def load_EnergyMatrix():
    aaDict={"ALA":{},"VAL":{},"LEU":{},"ILE":{},"PHE":{},\
            "TRP":{},"MET":{},"PRO":{},"GLY":{},"SER":{},\
            "THR":{},"CYS":{},"TYR":{},"ASN":{},"GLN":{},\
            "HIS":{},"LYS":{},"ARG":{},"ASP":{},"GLU":{},}

    List = aaDict.keys()
    List.sort()

    f1 = open("./project/PreDisulfideBond/Nepre/radius.npy")
    #f1 = open("/Users/xg666/Desktop/xqdongV2/project/project/PreDisulfideBond/Nepre/radius.npy")
    for amino1 in List:
        for amino2 in List:
            aaDict[amino1][amino2] = np.load(f1)
    f1.close()
    return aaDict


def extract_Data(line):
    """
    This part will extracted data from line according to the standard
    PDB file format(Version 3.3.0, Nov.21, 2012)
    """
    res = []
    #delete the space in the begin and end
    line = line.strip()
    #record_name
    res.append(line[0:4].strip(' '))

    #atom_serial
    res.append(line[6:11].strip(' '))

    #atom_name
    res.append(line[12:16].strip(' '))

    #alternate_indicator
    res.append(line[16])

    #residue_name
    res.append(line[17:20].strip(' '))

    #chain_id
    res.append(line[21].strip(' '))

    #residue_num
    res.append(line[22:26].strip(' '))

    #xcor
    res.append(line[30:38].strip(' '))

    #ycor
    res.append(line[38:46].strip(' '))

    #zcor
    res.append(line[46:54].strip(' '))

    return res


def process_pdb_file(pdbfile,matrix):

    CurrentAANitrogen = None
    CurrentAACA = None
    Currentresidue_num = None
    EachAA = []
    CurrentAA = None
    f = open(pdbfile)
    lines = f.readlines()
    f.close()
    #pdbfile = lines
    for line in lines:
        if (line[0:4] != "ATOM"):
            continue
        element_list = extract_Data(line)
        record_name = element_list[0]
        atom_name = element_list[2]
        residue_name = element_list[4]
        alternate_indicator = element_list[3]
        residue_num = element_list[-4]
        chain_id = element_list[-5]
        xcor = float(element_list[-3])
        ycor = float(element_list[-2])
        zcor = float(element_list[-1])

        if (atom_name == "H"):
            continue
        if (residue_name not in matrix):
            continue

        if (CurrentAA == None):
            CurrentAA = AA.AminoAcid(residue_name, residue_num, chain_id)
            Currentresidue_num = residue_num
            if (atom_name == "N" or atom_name == "CA"):
                if (alternate_indicator == "B"):
                    continue
                if (atom_name == "N"):
                    CurrentAANitrogen = np.array([xcor, ycor, zcor])
                else:
                    CurrentAACA = np.array([xcor, ycor, zcor])
            if (residue_name == "GLY" or atom_name not in {"N", "CA", "C", "O", "O1", "02"}):
                if (alternate_indicator != " "):
                    # If cases like "AASN or BASN" appears, we only add A
                    if (alternate_indicator == "A"):
                        CurrentAA.SumCenters(xcor, ycor, zcor)
                    else:
                        continue
                else:
                    CurrentAA.SumCenters(xcor, ycor, zcor)
        else:
            # If another amino acid begins
            if (residue_num != Currentresidue_num):
                state = CurrentAA.CalculateCenter()
                if (state == False):
                    CurrentAA = AA.AminoAcid(residue_name, residue_num, chain_id)
                    Currentresidue_num = residue_num
                    continue

                CurrentAA.InputCAN(CurrentAANitrogen, CurrentAACA)
                CurrentAA.EstablishCoordinate()
                # Amino Acid check
                EachAA.append(CurrentAA)
                del CurrentAA
                CurrentAA = AA.AminoAcid(residue_name, residue_num, chain_id)

                Currentresidue_num = residue_num
                if (atom_name == "N" or atom_name == "CA"):
                    if (alternate_indicator == "B"):
                        continue
                    if (atom_name == "N"):
                        CurrentAANitrogen = np.array([xcor, ycor, zcor])
                    else:
                        CurrentAACA = np.array([xcor, ycor, zcor])
                if (residue_name == "GLY" or atom_name not in {"N", "CA", "C", "O", "O1", "02"}):
                    if (alternate_indicator != " "):
                        # If cases like "AASN or BASN" appears, we only add A
                        if (alternate_indicator == "A"):
                            CurrentAA.SumCenters(xcor, ycor, zcor)
                        else:
                            continue
                    else:
                        CurrentAA.SumCenters(xcor, ycor, zcor)
            # If still the same amino acid
            else:
                if (atom_name == "N" or atom_name == "CA"):
                    if (alternate_indicator == "B"):
                        continue
                    if (atom_name == "N"):
                        CurrentAANitrogen = np.array([xcor, ycor, zcor])
                    else:
                        CurrentAACA = np.array([xcor, ycor, zcor])
                if (residue_name == "GLY" or atom_name not in {"N", "CA", "C", "O", "O1", "02"}):
                    if (alternate_indicator != " "):
                        # If cases like "AASN or BASN" appears, we only add A
                        if (alternate_indicator == "A"):
                            CurrentAA.SumCenters(xcor, ycor, zcor)
                        else:
                            continue
                    else:
                        CurrentAA.SumCenters(xcor, ycor, zcor)

    state = CurrentAA.CalculateCenter()
    if (state != False):
        #CurrentAA.CalculateCenter()
        CurrentAA.InputCAN(CurrentAANitrogen, CurrentAACA)
        CurrentAA.EstablishCoordinate()
        EachAA.append(CurrentAA)
    return EachAA

def process_AA2(AA_information,matrix):
    CurrentAA = None
    CurrentAANitrogen = None
    CurrentAACA = None
    Currentresidue_num = None
    #for debug
    lines = AA_information

    for line in lines:
        if(line[0:4] != "ATOM"):
            continue
        element_list = extract_Data(line)
        record_name = element_list[0]
        atom_name = element_list[2]
        residue_name = element_list[4]
        alternate_indicator = element_list[3]
        #do some change
        residue_num = element_list[-4]
        #add chain_id
        chain_id = element_list[-5]
        xcor = float(element_list[-3])
        ycor = float(element_list[-2])
        zcor = float(element_list[-1])

        if(atom_name == "H"):
            continue
        if(residue_name not in matrix):
            continue

        if(CurrentAA == None):
            CurrentAA = AA.AminoAcid(residue_name,residue_num,chain_id)
            Currentresidue_num = residue_num
            if(atom_name == "N" or atom_name == "CA"):
                if(alternate_indicator == "B"):
                    continue
                if(atom_name == "N"):
                    CurrentAANitrogen = np.array([xcor,ycor,zcor])
                else:
                    CurrentAACA = np.array([xcor,ycor,zcor])
            if(residue_name == "GLY" or atom_name not in {"N","CA","C","O","O1","02"}):
                if(alternate_indicator != " "):
                    #If cases like "AASN or BASN" appears, we only add A
                    #if(alternate_indicator == "A" and line[15] == "1"):
                    if(alternate_indicator == "A"):
                        CurrentAA.SumCenters(xcor,ycor,zcor)
                    else:
                        continue
                else:
                    CurrentAA.SumCenters(xcor,ycor,zcor)
        else:
            #If another amino acid begins
            if(residue_num != Currentresidue_num):
                state = CurrentAA.CalculateCenter()
                if(state == False):
                    CurrentAA = AA.AminoAcid(residue_name,residue_num,chain_id)
                    Currentresidue_num = residue_num
                    #continue

                CurrentAA.InputCAN(CurrentAANitrogen,CurrentAACA)
                #residue_name='ALA'
                #all_amino_acids.append(CurrentAA)
                del CurrentAA
                CurrentAA = AA.AminoAcid(residue_name,residue_num,chain_id)

                Currentresidue_num = residue_num
                if(atom_name == "N" or atom_name == "CA"):
                    if(alternate_indicator == "B"):
                        continue
                    if(atom_name == "N"):
                        CurrentAANitrogen = np.array([xcor,ycor,zcor])
                    else:
                        CurrentAACA = np.array([xcor,ycor,zcor])
                if(residue_name == "GLY" or atom_name not in {"N","CA","C","O","O1","02"}):
                    if(alternate_indicator != " "):
                    #If cases like "AASN or BASN" appears, we only add A
                        #if(alternate_indicator == "A" and line[15] == "1"):
                        if(alternate_indicator == "A"):
                            CurrentAA.SumCenters(xcor,ycor,zcor)
                        else:
                            continue
                    else:
                        CurrentAA.SumCenters(xcor,ycor,zcor)
            #If still the same amino acid
            else:
                if(atom_name == "N" or atom_name == "CA"):
                    if(alternate_indicator == "B"):
                        continue
                    if(atom_name == "N"):
                        CurrentAANitrogen = np.array([xcor,ycor,zcor])
                    else:
                        CurrentAACA = np.array([xcor,ycor,zcor])
                if(residue_name == "GLY" or atom_name not in {"N","CA","C","O","O1","02"}):
                    if(alternate_indicator != " "):
                    #If cases like "AASN or BASN" appears, we only add A
                        #if(alternate_indicator == "A" and line[15] == "1"):
                        if(alternate_indicator == "A"):
                            CurrentAA.SumCenters(xcor,ycor,zcor)
                        else:
                            continue
                    else:
                        CurrentAA.SumCenters(xcor,ycor,zcor)
    CurrentAA.CalculateCenter()
    CurrentAA.InputCAN(CurrentAANitrogen, CurrentAACA)
    #CurrentAA.EstablishCoordinate()
    return CurrentAA


def calculate_Energy_change_from_list(aa_list, all_amino_acids, matrix):
    Ewild = 0
    Emut = 0
    for ii, chainid, aa_wildtype, aa_mutant,mutation_inf in aa_list:
        n = 0
        for currentResidue in all_amino_acids:
            n += 1
            curidnumber = currentResidue.idnumber
            curchainid = currentResidue.chainID
            curname = currentResidue.name
            if currentResidue.idnumber == ii and currentResidue.chainID == chainid and currentResidue.name == aa_wildtype:
                #mut_AA = process_AA(mutation_inf, matrix)
                mut_AA = process_AA2(mutation_inf, matrix)
                #currentResidue.EstablishCoordinate()
                mut_AA.EstablishCoordinate()
                n = 0
                for Rediue_nn in all_amino_acids:
                    n += 1
                    if(currentResidue == Rediue_nn):
                        continue
                    else:
                        diswild = currentResidue.DistanceBetweenAA(Rediue_nn.center)
                        dismut = mut_AA.DistanceBetweenAA(Rediue_nn.center)

                        if(diswild <= 6.0):
                            rho_w,theta_w,phi_w = currentResidue.ChangeCoordinate(Rediue_nn.center)
                            #print diswild,dismut,currentResidue.center,mut_AA.center,Rediue_nn.center
                            #print 'hhshshshhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
                            theta_w = min(int(math.floor(theta_w*20/np.pi)),19)
                            phi_w = min(int(math.floor(phi_w*10/np.pi) + 10),19)

                            rho_w2,theta_w2,phi_w2 = Rediue_nn.ChangeCoordinate(currentResidue.center)
                            theta_w2 = min(int(math.floor(theta_w2*20/np.pi)),19)
                            phi_w2 = min(int(math.floor(phi_w2*10/np.pi) + 10),19)
                            Ewild += matrix[currentResidue.name][Rediue_nn.name][theta_w][phi_w] / rho_w
                            Ewild += matrix[Rediue_nn.name][currentResidue.name][theta_w2][phi_w2] / rho_w2
                            #dE += matrix[aa_mutant][Rediue_nn.name][theta_w][phi_w] / rho_w
                            #dE += matrix[Rediue_nn.name][aa_mutant][theta_w2][phi_w2] / rho_w2
                            #Ewild += matrix[currentResidue.name][Rediue_nn.name][theta_w][phi_w] / rho_w
                        if(dismut <= 6.0):
                            #print'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
                            #print diswild,dismut,currentResidue.center,mut_AA.center,Rediue_nn.center
                            rho_m,theta_m,phi_m = mut_AA.ChangeCoordinate(Rediue_nn.center)
                            #print diswild,dismut,currentResidue.center,mut_AA.center,Rediue_nn.center
                            theta_m = min(int(math.floor(theta_m*20/np.pi)),19)
                            phi_m = min(int(math.floor(phi_m*10/np.pi) + 10),19)

                            rho_m2,theta_m2,phi_m2 = Rediue_nn.ChangeCoordinate(mut_AA.center)
                            theta_m2 = min(int(math.floor(theta_m2*20/np.pi)),19)
                            phi_m2 = min(int(math.floor(phi_m2*10/np.pi) + 10),19)
                            Emut += matrix[mut_AA.name][Rediue_nn.name][theta_m][phi_m] / rho_m
                            Emut += matrix[Rediue_nn.name][mut_AA.name][theta_m2][phi_m2] / rho_m2

                break
            else:
                continue
    #dE = Ewild - Emut
    dE = Emut - Ewild
    return dE


def get_energy(pdbfile,mut_list):
    energymatrix = load_EnergyMatrix()
    #radiusDict = LoadRadius()
    all_amino_acids = process_pdb_file(pdbfile, energymatrix)
    all_energy = []
    for mutationlist in mut_list:
        this_dE = calculate_Energy_change_from_list(mutationlist,all_amino_acids,energymatrix)
        all_energy.append(this_dE)
    return all_energy




if __name__ == "__main__":

    args = sys.argv[1:]
    pdb = args[0]
    matrix = load_EnergyMatrix()
    if len(args) == 1:
        E = calculate_energy_for_pdbfile(pdb,matrix)
        print "Nepre Potential Energy(Radius)"
        print pdb,E
    if len(args) == 2:
        n_sites = 1
        n_mutations = int(args[1])
        calculate_energy_for_pdbfile_with_mutations(pdb,matrix, n_sites=n_sites, n_mutations=n_mutations)
    if len(args) == 3:
        n_sites = int(args[1])
        n_mutations = int(args[2])
        calculate_energy_for_pdbfile_with_mutations(pdb,matrix, n_sites=n_sites, n_mutations=n_mutations)
