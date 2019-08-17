from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import math
import tensorflow as tf
import re


TOWER_NAME = 'tower'
NUM_CLASSES = 2

# The ssbond_distance_map are always 12x12 pixels.
IMAGE_SIZE = 10
IMAGE_PIXELS = IMAGE_SIZE * IMAGE_SIZE

TRAIN_FILE = 'nor_train_shulffle.tfrecords'

TEST_FILE = 'test_shulffle.tfrecords'
# TRAIN_FILE = 'nor_train_shulffle.tfrecords'
# TEST_FILE = 'nor_test_shulffle.tfrecords'

parser = argparse.ArgumentParser()

# Basic model parameters.
parser.add_argument('--batch_size', type=int, default=100,
                    help='Number of images to process in a batch.')

parser.add_argument('--data_dir', type=str, default='/Users/dongxq/Desktop/SSBOND_supplement/rootpath40/',
                    help='Path to the CIFAR-10 data directory.')
parser.add_argument(
    '--num_epochs',
    type=int,
    default=30,
    help='Number of epochs to run trainer.'
)
FLAGS = parser.parse_args()

def fill_feed_dict(images_pl, labels_pl,x,y,sess=None ):
    """Fills the feed_dict for training the given step.
    A feed_dict takes the form of:
    feed_dict = {
      <placeholder>: <tensor of values to be passed for placeholder>,
    }
    Args:
    data_set: The set of images and labels, from input_data.read_data_sets()
    images_pl: The images placeholder, from placeholder_inputs().
    labels_pl: The labels placeholder, from placeholder_inputs().
    Returns:
    feed_dict: The feed dictionary mapping from placeholders to values.
    """
    # Create the feed_dict for the placeholders filled with the next
    # `batch size` examples.

    if sess!= None:
        images_feed,labels_feed = sess.run([x,y])
        # print(labels_feed.reshape(len(labels_feed)))
        feed_dict = {
            images_pl: images_feed,
            labels_pl: labels_feed.reshape((len(labels_feed))),
        }
    else:
        feed_dict = {
            images_pl: x,
            labels_pl: y.reshape((len(labels_feed))),
        }
    # images_feed, labels_feed = data_set.next_batch(FLAGS.batch_size,FLAGS.fake_data)
    # print(images_feed.shape,labels_feed.shape)
    
    return feed_dict

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
    # image.set_shape([12,12])

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
    if train == False:
        with tf.name_scope('input_test'):
            filename_queue = tf.train.string_input_producer([filename],num_epochs=1, shuffle=False)

            # Even when reading in multiple threads, share the filename
            # queue.
            image, label = read_and_decode(filename_queue)
            # Shuffle the examples and collect them into batch_size batches.
            # (Internally uses a RandomShuffleQueue.)
            # We run this in two threads to avoid being a bottleneck.
            images, sparse_labels = tf.train.shuffle_batch(
                [image, label], batch_size=2000, num_threads=2,capacity=1000 + 3 * batch_size,min_after_dequeue=1000)
            # print(image)
        return images, sparse_labels
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

def inference(images, hidden1_units, hidden2_units):
    """Build the MNIST model up to where it may be used for inference.
    Args:
      images: Images placeholder, from inputs().
      hidden1_units: Size of the first hidden layer.
      hidden2_units: Size of the second hidden layer.
    Returns:
      softmax_linear: Output tensor with the computed logits.
    """
    # Hidden 1
    with tf.variable_scope('hidden1'):
        weights = _variable_on_cpu('weights',[IMAGE_PIXELS, hidden1_units],
            tf.truncated_normal_initializer(stddev=1.0 / math.sqrt(float(IMAGE_PIXELS))))
        print(weights)
        biases = _variable_on_cpu('biases',[hidden1_units],tf.constant_initializer(0.0))
        hidden1 = tf.nn.relu(tf.matmul(images, weights) + biases)
        _activation_summary(hidden1)
    # Hidden 2
    with tf.variable_scope('hidden2'):
        weights = _variable_on_cpu('weights',[hidden1_units, hidden2_units],
            tf.truncated_normal_initializer(stddev=1.0 / math.sqrt(float(IMAGE_PIXELS)),))
        biases = _variable_on_cpu( 'biases',[hidden2_units],tf.constant_initializer(0.0))
        hidden2 = tf.nn.relu(tf.matmul(hidden1, weights) + biases)
        _activation_summary(hidden2)
    # Linear
    with tf.variable_scope('softmax_linear'):
        weights = _variable_on_cpu( 'weights',[hidden2_units, NUM_CLASSES],
            tf.truncated_normal_initializer(stddev=1.0 / math.sqrt(float(IMAGE_PIXELS))))
        biases = _variable_on_cpu('biases',[NUM_CLASSES],tf.constant_initializer(0.0)  )
        logits = tf.matmul(hidden2, weights) + biases
        print('logits',logits)
        _activation_summary(logits)
    return logits

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
