# -*-coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import sys
import tensorflow as tf 
import numpy as np
import collections
import random

# Datasets = collections.namedtuple('Datasets', ['train', 'validation', 'test'])

FLAGS = None


def _int64_feature(value):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _Float_feature(value):
  return tf.train.Feature(float_list=tf.train.FloatList(value=value))

def splitTestSet(samplelist):
	# small_list = random.sample(samplelist,num)
	small_list = samplelist[-FLAGS.split_size:]
	big_list = samplelist[:len(samplelist)-FLAGS.split_size]
	return big_list,small_list
	

def bind_p_n(positiveSample, negtiveSample):
	print('length of the positiveSample:{}, length of the negtiveSample:{}'.format(len(positiveSample),len(negtiveSample)))
	positivetrain,positivetest = splitTestSet(positiveSample)
	negativetrain,negativetest = splitTestSet(negtiveSample)
	allsampletrain = np.concatenate((positivetrain, negativetrain), axis=0)
	allsampletest = np.concatenate((positivetest, negativetest), axis=0)
	print('allsampletrain length is %d'%allsampletrain.shape[0])
	print('allsampletest length is %d'%allsampletest.shape[0])
	return allsampletrain, allsampletest

def shulffle(samplelist,labels):
	samplezip = zip(samplelist.tolist(),labels)
	random.shuffle(samplezip)
	# print(samplezip[0])
	print([x[1] for x in samplezip])
	return samplezip

def convert_to(data_set, name, labelmark):
	"""Converts a dataset to tfrecords."""
	num_examples = len(data_set)
	print(num_examples//2)
	labels = [1 for i in range(num_examples//2)]
	labels.extend([0 for j in range(num_examples//2)])
	
	if len(labels) != num_examples:
		print('length of the label is %d'%len(labels))
		sys.exit()

	filename = os.path.join(FLAGS.directory, name + '.tfrecords')
	print('Writing', filename)
	writer = tf.python_io.TFRecordWriter(filename)
	for index in range(num_examples):
		image_raws = data_set[index].reshape(100) #.tolist()
		# for row in data_set[index]:
		# print(type(image_raws[0]))

		# print([float(x) for x in data_set[index]])
		example = tf.train.Example(features=tf.train.Features(feature={
		    'label': _int64_feature(int(labels[index])),
		    'image_raw': _Float_feature(image_raws)}))
		writer.write(example.SerializeToString())
	writer.close()

def convert_to_shulffle_tfrecord(data_set, name, labelmark):
	num_examples = len(data_set)
	print(num_examples//2)
	labels = [1 for i in range(num_examples//2)]
	labels.extend([0 for j in range(num_examples//2)])
	shulfflelist = shulffle(data_set,labels)
	if len(labels) != num_examples:
		print('length of the label is %d'%len(labels))
		sys.exit()

	filename = os.path.join(FLAGS.directory, name + '_shulffle.tfrecords')
	print('Writing', filename)
	writer = tf.python_io.TFRecordWriter(filename)
	for index in range(num_examples):
		image_raws = np.array(shulfflelist[index][0]).reshape(100) #.tolist()
		# for row in data_set[index]:
		# print(type(image_raws[0]))

		# print([float(x) for x in data_set[index]])
		example = tf.train.Example(features=tf.train.Features(feature={
		    'label': _int64_feature(int(shulfflelist[index][1])),
		    'image_raw': _Float_feature(image_raws)}))
		writer.write(example.SerializeToString())
	writer.close()

def convert_image_only(filename):
	pass

def main(unused_argv):
	# Get the data.
	if FLAGS.predict == False:
		data_sets_p = np.load(FLAGS.directory+FLAGS.p_sample)
		#data_sets_p = data_sets_p
		data_sets_n = np.load(FLAGS.directory+FLAGS.n_sample)
		data_sets_n = data_sets_n[:5122][:][:]

		if len(data_sets_n) != len(data_sets_p):
			print('positve sample and negative length are not equal!')
			sys.exit()

		train_dataset, test_dataset= bind_p_n(data_sets_p, data_sets_n)
		labelmark = len(data_sets_n)-FLAGS.split_size

		# Convert to Examples and write the result to TFRecords.
		# convert_to(train_dataset, 'train', labelmark)
		# convert_to(test_dataset, 'test', labelmark)
		convert_to_shulffle_tfrecord(train_dataset, 'nor_train', labelmark)
		convert_to_shulffle_tfrecord(test_dataset, 'nor_test', labelmark)
		# convert_to(data_sets.test, 'test')
	else:
		print('Only convert images, no label.')




if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
	  '--directory',
	  type=str,
	  default='/Users/dongxq/Desktop/SSBOND_supplement/rootpath40/',
	  help='Directory to exist positive data files and write the converted result'
	)
	parser.add_argument(
	  '--p_sample',
	  type=str,
	  default='positive_distance.npy',
	  help='Directory to exist negative data files and write the converted result'
	)
	parser.add_argument(
	  '--n_sample',
	  type=str,
	  default='negative_distance.npy',
	  help='Directory to exist negative data files and write the converted result'
	)
	
	parser.add_argument(
	  '--split_size',
	  type=int,
	  default=1000,
	  help="""\
	  Number of examples to separate from the training data for the validation set.\
	  """
	)
	parser.add_argument(
	  '--predict',
	  type=bool,
	  default=False,
	  help="""\
	  Number of examples to separate from the training data for the validation set.\
	  """
	)
	# parser.add_argument(
	#   '--predict_image',
	#   type=str,
	#   default=False,
	#   help="""\
	#   Number of examples to separate from the training data for the validation set.\
	#   """
	# )

	FLAGS, unparsed = parser.parse_known_args()
	tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
	
