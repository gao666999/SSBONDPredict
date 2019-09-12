## datafiles used for training,testing and validation

* **positive_atom_position.npy** : recorded array about atoms position of positive sample
* **negative_atom_position.npy** : recorded array about atoms position of negative sample
* **negative_distance_map.npy** : the atoms distance map of positive sample
* **negative_distance_map.npy** : the atoms distance map of negative sample
* **cullpdb_train.tfrecords** : the data retrieved from cullpdb_pc40_res2.0_R0.25_d190801_chains15139 for training in tensorflow data format
* **cullpdb_test.tfrecords** : the data retrieved from cullpdb_pc40_res2.0_R0.25_d190801_chains15139 for testing in tensorflow data format
* **validation.tfrecords** : the data for validation in tensorflow data format
* the files in **CNNlog** are the models trained used CNN network based on cullpdb_pc40_res2.0_R0.25_d190801_chains15139
* the files in **fullyconnectedlog** are the models trained used fully connected network based on data cullpdb_pc40_res2.0_R0.25_d190801_chains15139
