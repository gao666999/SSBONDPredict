# Data code
## Inside this folder there some program to generate data
* *Download_PDB.py* is a script can download the pdb file from the Protein Data Bank
**Usage**
```
python Download_PDB.py cullpath datasetpath
cullpath is the path of cullpdb_pc40_res2.0_R0.25_d190801_chains15139
datasetpath is where you want to save the downloaded pdb files
```
* *create_positive_map.py* can extract the atom position matrixs about positive samples from the pdb files, return the array with shape (NumberOfSSbond,10,3), save the array in npy fromat.
**Usage**
```
python create_positive_map.py pdbpath resultpath resultfilename
pdbpath is the path of the pdbfiles to be processed
resultpath is where you want to save the result
resultfilename is the name of the result file you want to set,for example: 'positive_atom_position.npy'

```
* *create_negative_map.py* can extract the atom position matrixs about negative samples from the PDB files,return the array with shape (LengthOfAtom,10,3), save the array in npy fromat.
**Usage**
```
python create_negative_map.py pdbpath resultpath resultfilename
pdbpath is the path of the pdbfiles to be processed
resultpath is where you want to save the result
resultfilename means the name of the result file you want to set,for example: 'negative_atom_position.npy'

* *ssbond_distance_map.py* can turn the atom position array into distance map with shape(NumberOfSSBOND,10,10).
**Usage**
```
python ssbond_distance_map.py AtomPositionfile resultpath resultfilename
AtomPositionfile is the file saved negative or positive atom position array,resultpath is where you want to save the result, resultfilename is the name of result file you want to set,for example:'positive_distance_map.npy'
```

* *create_tfrecords.py* can turn the map of positive and negative sample into tensorflow data format
```
python create_tfrecords.py
and you can run python create_tfrecords.py --help Will display all parameters and features.
```
