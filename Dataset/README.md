
* cullpdb_pc40_res2.0_R0.25_d190801_chains15139 records all the PDB ID and chain ID used during the train and test  
## the data in detaildata are some recording about data used for training and testing actually  
* test_name.txt records the PDB ID and chian ID for testing
* validation_name_noss.txt records the PDB ID for validation 
* positive_distance.npy records the atoms' distance matrix of positive sample  
* negative_distance.npy records the atoms' distance matrix of negative sample  
* positive_ssbond_map.npy records the positive map
* negative_nossbonds_map.npy records the negative map
* nor_train_shulffle.tfrecords is the data for training  
* nor_test_shulffle.tfrecords is the data for testing  
* validation.tfrecords is the data for validation  
  
