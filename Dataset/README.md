
* cullpdb_pc40_res2.0_R0.25_d190801_chains15139 was retrieved from the PISCES database (http://dunbrack.fccc.edu/Guoli/pisces_download.php), which records the non-redundant dataset with the PDB ID and chain ID. 

The dataset has sequence identity cutoff of 0.40, the structures have resolutions better than 2.0 Å, and the R-factors are lower than 0.25. There are 15,139 chains in this dataset.

## the data in detaildata are the datafiles used for training and testing   
* *test_name.txt* : the PDB ID and chian ID for testing
* *validation_name_noss.txt* : the PDB ID for validation 

* *positive_distance.npy* : the atom distance matrices of positive sample  
* *negative_distance.npy* : the atom distance matrices of negative sample  
* *positive_ssbond_map.npy* : the positive map
* *negative_nossbonds_map.npy* : the negative map

* *nor_train_shulffle.tfrecords* : the data for training in tensorflow data format
* *nor_test_shulffle.tfrecords* : the data for testing in tensorflow data format
* *validation.tfrecords* : the data for validation in tensorflow data format
  
