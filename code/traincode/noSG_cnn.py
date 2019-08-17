# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import math
import tensorflow as tf
import re
import numpy as np


TOWER_NAME = 'tower'
NUM_CLASSES = 2

# The ssbond_distance_map are always 12x12 pixels.
IMAGE_SIZE = 10
IMAGE_PIXELS = IMAGE_SIZE * IMAGE_SIZE

TRAIN_FILE = 'nor_train_shulffle.tfrecords'
TEST_FILE = 'test_shulffle.tfrecords'

parser = argparse.ArgumentParser()

# Basic model parameters.
parser.add_argument(
	'--batch_size', 
	type=int, 
	default=100,
	help='Number of images to process in a batch.'
	)

parser.add_argument(
	'--data_dir', 
	type=str, 
	default='/Users/dongxq/Desktop/SSBOND_supplement/rootpath40/',
	help='Path to the training data directory.'
	)
parser.add_argument(
    '--num_epochs',
    type=int,
    default=10,
    help='Number of epochs to run trainer.'
	)
FLAGS = parser.parse_args()

def fill_feed_dict(images_pl, labels_pl,x,y,sess=None ):

    if sess!= None:
        images_feed,labels_feed = sess.run([x,y])
        # print(labels_feed.reshape(len(labels_feed)))
        images_feed= np.reshape(images_feed,(len(images_feed),10,10,1))
        # print('images_feed',images_feed.shape)
        feed_dict = {
            images_pl: images_feed,
            labels_pl: labels_feed.reshape((len(labels_feed))),
        }
    else:
    	x = np.reshape(x,(len(x),10,10,1))
    	print('x',x.shape)

        feed_dict = {
            images_pl: x,
            labels_pl: y.reshape((len(labels_feed))),
        }
    # images_feed, labels_feed = data_set.next_batch(FLAGS.batch_size,FLAGS.fake_data)
    # print(images_feed.shape,labels_feed.shape)
    
    return feed_dict


def _variable_with_weight_decay(name, shape, stddev, wd):

  dtype = tf.float32
  var = _variable_on_cpu(
      name,
      shape,
      tf.truncated_normal_initializer(stddev=stddev, dtype=dtype))
  if wd is not None:
    weight_decay = tf.multiply(tf.nn.l2_loss(var), wd, name='weight_loss')
    tf.add_to_collection('losses', weight_decay)
  return var

def _activation_summary(x):
    """Helper to create summaries for activations.
    Creates a summary that provides a histogram of activations.
    Creates a summary that measures the sparsity of activations.
    Args:
        x: Tensor
    Returns:
        nothing
    """
    # Remove 'tower_[0-9]/' from the name in case this is a multi-GPU training
    # session. This helps the clarity of presentation on tensorboard.
    tensor_name = re.sub('%s_[0-9]*/' % TOWER_NAME, '', x.op.name)
    tf.summary.histogram(tensor_name + '/activations', x)
    tf.summary.scalar(tensor_name + '/sparsity', tf.nn.zero_fraction(x))

def _variable_on_cpu(name, shape, initializer):
    """Helper to create a Variable stored on CPU memory.
    Args:
        name: name of the variable
        shape: list of ints
        initializer: initializer for Variable
    Returns:
        Variable Tensor
    """
    with tf.device('/cpu:0'):
      dtype = tf.float32
      var = tf.get_variable(name, shape, initializer=initializer, dtype=dtype)
    return var

def read_and_decode(filename_queue):
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(
        serialized_example,
        # Defaults are not specified since both keys are required.
        features={
            'image_raw': tf.FixedLenFeature([IMAGE_PIXELS], tf.float32),
            'label': tf.FixedLenFeature([1], tf.int64),
      })

    image = features['image_raw']
    # image = tf.reshape(image, [12,12,1])

    label = tf.cast(features['label'], tf.int64)
    

    return image, label

def inputs(train, batch_size, num_epochs):
    """Reads input data num_epochs times.
    Args:
    train: Selects between the training (True) and validation (False) data.
    batch_size: Number of examples per returned batch.
    num_epochs: Number of times to read the input data, or 0/None to
       train forever.
    Returns:
    A tuple (images, labels), where:
    * images is a float tensor with shape [batch_size, mnist.IMAGE_PIXELS]
      in the range [-0.5, 0.5].
    * labels is an int32 tensor with shape [batch_size] with the true label,
      a number in the range [0, mnist.NUM_CLASSES).
    Note that an tf.train.QueueRunner is added to the graph, which
    must be run using e.g. tf.train.start_queue_runners().
    """
    if not num_epochs: num_epochs = None
    filename = os.path.join(FLAGS.data_dir,TRAIN_FILE if train else TEST_FILE)
    print(filename)
    with tf.name_scope('input'):
        filename_queue = tf.train.string_input_producer([filename],num_epochs=num_epochs)

        # Even when reading in multiple threads, share the filename
        # queue.
        image, label = read_and_decode(filename_queue)
        # Shuffle the examples and collect them into batch_size batches.
        # (Internally uses a RandomShuffleQueue.)
        # We run this in two threads to avoid being a bottleneck.
        images, sparse_labels = tf.train.shuffle_batch(
            [image, label], batch_size=batch_size, num_threads=2,
            capacity=1000 + 3 * batch_size,
            # Ensures a minimum amount of shuffling of examples.
            min_after_dequeue=1000)
        # print images, sparse_labels

    return images, sparse_labels

def inference(images):
	"""Build the cnn model.
	Args:
	images: Images returned from distorted_inputs() or inputs().
	Returns:
	Logits.
	"""
	# We instantiate all variables using tf.get_variable() instead of
	# tf.Variable() in order to share variables across multiple GPU training runs.
	# If we only ran this model on a single GPU, we could simplify this function
	# by replacing all instances of tf.get_variable() with tf.Variable().
	#
	# conv1
	print('image',images)
	with tf.variable_scope('conv1') as scope:
		kernel = _variable_with_weight_decay('weights',
		                                     shape=[5, 5, 1, 64],
		                                     stddev=5e-2,
		                                     wd=0.0)
		conv = tf.nn.conv2d(images, kernel, [1, 1, 1, 1], padding='SAME')
		print('conv',conv)
		biases = _variable_on_cpu('biases', [64], tf.constant_initializer(0.0))
		pre_activation = tf.nn.bias_add(conv, biases)
		conv1 = tf.nn.relu(pre_activation, name=scope.name)
		_activation_summary(conv1)

		# # pool1
		pool1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool1')
		# # norm1
		norm1 = tf.nn.lrn(pool1, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75,name='norm1')
		

		# conv2
	with tf.variable_scope('conv2') as scope:
		kernel = _variable_with_weight_decay('weights',
		                                     shape=[5, 5, 64, 64],
		                                     stddev=5e-2,
		                                     wd=0.0)
		conv = tf.nn.conv2d(norm1, kernel, [1, 1, 1, 1], padding='SAME')
		biases = _variable_on_cpu('biases', [64], tf.constant_initializer(0.1))
		pre_activation = tf.nn.bias_add(conv, biases)
		conv2 = tf.nn.relu(pre_activation, name=scope.name)
		_activation_summary(conv2)

		# norm2
		norm2 = tf.nn.lrn(conv2, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75, name='norm2')
		# # pool2
		pool2 = tf.nn.max_pool(norm2, ksize=[1, 2, 2, 1],strides=[1, 2, 2, 1], padding='SAME', name='pool2')
		print('reshape',pool2)
		# local3
	with tf.variable_scope('local3') as scope:
		# Move everything into depth so we can perform a single matrix multiply.
		reshape = tf.reshape(pool2, [-1, 576])
		# dim = reshape.get_shape()[1].value
		# print('dim',dim)
		weights = _variable_with_weight_decay('weights', shape=[576, 384],
		                                      stddev=0.04, wd=0.004)
		biases = _variable_on_cpu('biases', [384], tf.constant_initializer(0.1))
		local3 = tf.nn.relu(tf.matmul(reshape, weights) + biases, name=scope.name)
		_activation_summary(local3)

		# local4
	with tf.variable_scope('local4') as scope:
		weights = _variable_with_weight_decay('weights', shape=[384, 192],
		                                      stddev=0.04, wd=0.004)
		biases = _variable_on_cpu('biases', [192], tf.constant_initializer(0.1))
		local4 = tf.nn.relu(tf.matmul(local3, weights) + biases, name=scope.name)
		_activation_summary(local4)

		# linear layer(WX + b),
		# We don't apply softmax here because
		# tf.nn.sparse_softmax_cross_entropy_with_logits accepts the unscaled logits
		# and performs the softmax internally for efficiency.
	with tf.variable_scope('softmax_linear') as scope:
		weights = _variable_with_weight_decay('weights', [192, NUM_CLASSES],
		                                      stddev=1/192.0, wd=0.0)
		biases = _variable_on_cpu('biases', [NUM_CLASSES],
		                          tf.constant_initializer(0.0))
		softmax_linear = tf.add(tf.matmul(local4, weights), biases, name=scope.name)
		print(softmax_linear)
		_activation_summary(softmax_linear)

	return softmax_linear

def loss(logits, labels):
    """Calculates the loss from the logits and the labels.
    Args:
      logits: Logits tensor, float - [batch_size, NUM_CLASSES].
      labels: Labels tensor, int32 - [batch_size].
    Returns:
      loss: Loss tensor of type float.
    """
    # print('loss')
    labels = tf.to_int64(labels)
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
        labels=labels, logits=logits, name='xentropy')
    return tf.reduce_mean(cross_entropy, name='xentropy_mean')

def training(loss, learning_rate):
    """Sets up the training Ops.
    Creates a summarizer to track the loss over time in TensorBoard.
    Creates an optimizer and applies the gradients to all trainable variables.
    The Op returned by this function is what must be passed to the
    `sess.run()` call to cause the model to train.
    Args:
      loss: Loss tensor, from loss().
      learning_rate: The learning rate to use for gradient descent.

    Returns:
      train_op: The Op for training.
    """
    # Add a scalar summary for the snapshot loss.
    # print('train')
    tf.summary.scalar('loss', loss)
    # Create the gradient descent optimizer with the given learning rate.
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    # Create a variable to track the global step.
    global_step = tf.Variable(0, name='global_step', trainable=False)
    # Use the optimizer to apply the gradients that minimize the loss
    # (and also increment the global step counter) as a single training step.
    train_op = optimizer.minimize(loss, global_step=global_step)
    # print('train done')
    return train_op
