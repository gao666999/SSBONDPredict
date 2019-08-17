# Data code  
## Inside this folder there some program to generate data  
* Down_loadPDB.py is a script can download the pdb file from the Protein Data Bank  
* create_positive_map.py can extract the positive sample from the pdb file then turn  
  the feature into a map saved in npy fromat  
* create_negative_map.py can extract the negative sample from the PDB file then turn  
  the feature into a map saved in npy fromat  
* ssbond_distance_map.py can turn the sample's map to a matrix with the shape 10*10  
* create_tfrecords.py can turn the file in npy fromat to tfrecords fromat  
# Train code
## Inside this folder there some program about training and testing
* noSG_fnn.py is the structure about fully connected neural network  
* noSG_fnn_train_test.py is the test and train program about fully connected neural network  
* noSG_restore_fnn.py is the program about restoring fully connected model  
* noSG_cnn.py is the structure about CNN neural network  
* noSG_cnn_train_test.py is the test and train program about CNN neural network  
* noSG_restore_cnn.py is the program about restoring cnn model  

