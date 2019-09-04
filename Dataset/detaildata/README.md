##datafiles used for training and testing##

* *test_name.txt* : the PDB ID and chian ID for testing
* *validation_name_noss.txt* : the PDB ID for validation 

* *positive_distance.npy* : the atom distance matrices of positive sample  
* *negative_distance.npy* : the atom distance matrices of negative sample  
* *positive_ssbond_map.npy* : the positive map
* *negative_nossbonds_map.npy* : the negative map

* *nor_train_shulffle.tfrecords* : the data for training in tensorflow data format
* *nor_test_shulffle.tfrecords* : the data for testing in tensorflow data format
* *validation.tfrecords* : the data for validation in tensorflow data format
