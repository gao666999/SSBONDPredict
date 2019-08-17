# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import time
import numpy as np
import tensorflow as tf
import argparse
import os
import exceptions
import noSG_fnn
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt
from sklearn.metrics import average_precision_score
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import roc_auc_score

FLAGS = None

# Constants used for dealing with the files, matches convert_to_records.
# TRAIN_FILE = 'train.tfrecords'
# TEST_FILE = 'test.tfrecords'



parser = noSG_fnn.parser
parser.add_argument(
	'--learning_rate',
	type=float,
	default=0.01,
	help='Initial learning rate.'
)
parser.add_argument(
	'--hidden1',
	type=int,
	default=128,
	help='Number of units in hidden layer 1.'
)
# parser.add_argument(
# 	'--hidden2',
# 	type=int,
# 	default=64,
# 	help='Number of units in hidden layer 2.'
# )
parser.add_argument(
	'--hidden2',
	type=int,
	default=32,
	help='Number of units in hidden layer 2.'
)
# parser.add_argument(
# 	'--batch_size',
# 	type=int,
# 	default=100,
# 	help='Batch size.'
# )
MODEL_SAVE_PATH='/Users/dongxq/Desktop/SSBOND_supplement/rootpath40/log/'
MODEL_NAME='model.ckpt'
parser.add_argument(
	'--log_dir',
	type=str,
	#default=os.path.join(os.getenv('TEST_TMPDIR', '/Users/dongxq/Desktop/SSBOND_supplement/'),
	#                  '/rootpath40/log/'),
	default='/Users/dongxq/Desktop/SSBOND_supplement/rootpath40/log/',
	help='Directory to put the log data.'
 )
parser.add_argument(
	'--train_dir',
	type=str,
	default='/Users/dongxq/Desktop/SSBOND_supplement/rootpath40/',
	help='Directory with the training data.'
)
# parser.add_argument(
# 	'--Validation_path',
# 	type=str,
# 	default='/Users/dongxq/Desktop/disulfide/other_set_map/7635_refine_4_full_possible_ssbond_nr.npy',
# 	help='path with the Validation data.'
# )
# parser.add_argument(
# 	'--Validation_ord_path',
# 	type=str,
# 	default='/Users/dongxq/Desktop/disulfide/other_set_map/7635_refine_4_possible_ssbond_id_nr.npy',
# 	help='path with the Validation data.'
# )

def draw_P_R_curve(images_placeholder,labels_placeholder, x_test,y_test,sess,loss,accuracy,one_hot_labels,out):
	feed_dict = noSG_fnn.fill_feed_dict(images_placeholder,labels_placeholder, x_test,y_test,sess=sess)
	test_loss,accuracy_,testlabel,out_= sess.run([loss,accuracy,one_hot_labels,out],feed_dict=feed_dict)
	print('testSet: test loss  = %.2f ,accuracy:%.2f'% (test_loss, accuracy_))
	testlabel = sess.run(tf.argmax(testlabel, 1))
	# print(out_)
	new_out_ = out_[:,1]
	# print('******************************')
	# print(new_out_)
	average_precision = average_precision_score(testlabel, new_out_)
	precision, recall, _ = precision_recall_curve(testlabel, new_out_)
	plt.step(recall, precision, color='b', alpha=0.2, where='post')
	plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')

	plt.xlabel('Recall')
	plt.ylabel('Precision')
	plt.ylim([0.0, 1.05])
	plt.xlim([0.0, 1.0])
	plt.title('2-class Precision-Recall curve: AUC={0:0.6f}'.format(average_precision))
	plt.show()

def draw_ROC_curve(images_placeholder,labels_placeholder, x_test,y_test,sess,loss,accuracy,one_hot_labels,out):
	feed_dict = noSG_fnn.fill_feed_dict(images_placeholder,labels_placeholder, x_test,y_test,sess=sess)
	test_loss,accuracy_,testlabel,out_= sess.run([loss,accuracy,one_hot_labels,out],feed_dict=feed_dict)
	print('testSet: test loss  = %.2f ,accuracy:%.2f'% (test_loss, accuracy_))
	fpr, tpr, thresholds = roc_curve(testlabel[:,1], out_[:,1])
	roc_auc = auc(fpr, tpr)
	print(thresholds)
	print(len(thresholds))
	print(roc_auc_score(testlabel[:,1], out_[:,1]))
	plt.figure()
	lw = 2
	plt.plot(fpr, tpr, color='darkorange',
	         lw=lw, label='ROC curve (area = %0.4f)' % roc_auc)
	plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
	plt.xlim([0.0, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Test set receiver operating characteristic')
	plt.legend(loc="lower right")
	plt.show()
def run_training():
	now = time.time()
	with tf.Graph().as_default():
	    # Generate placeholders for the images and labels.
		x,y = noSG_fnn.inputs(train=True, batch_size=100,
			num_epochs=10)
		x_test,y_test = noSG_fnn.inputs(train=False, batch_size=100,
			num_epochs=FLAGS.num_epochs)
		images_placeholder = tf.placeholder(tf.float32, [None,100],name='image')
		labels_placeholder = tf.placeholder(tf.int64, [None],name='labels')
		print (images_placeholder,labels_placeholder)

		logits = noSG_fnn.inference(images_placeholder, 128, 32)
		print('here')

		out=tf.nn.softmax(logits=logits)

		loss = noSG_fnn.loss(logits, labels_placeholder)
		# Add to the Graph operations that train the model.
		train_op = noSG_fnn.training(loss, FLAGS.learning_rate)

		# The op for initializing the variables.
		init_op = tf.group(tf.global_variables_initializer(),
			tf.local_variables_initializer())

		# Build the summary Tensor based on the TF collection of Summaries.
		summary = tf.summary.merge_all()

		# Create a saver for writing training checkpoints.
		saver = tf.train.Saver()
		
		# Create a session for running operations in the Graph.
		sess = tf.Session()
		# Instantiate a SummaryWriter to output summaries and the Graph.
		summary_writer = tf.summary.FileWriter(FLAGS.log_dir, sess.graph)
		
		# Initialize the variables (the trained variables and the
		# epoch counter).
		sess.run(init_op)

		# Start input enqueue threads.
		coord = tf.train.Coordinator()
		threads = tf.train.start_queue_runners(sess=sess, coord=coord)

		one_hot_labels = tf.one_hot(labels_placeholder,axis=-1,depth=2)

		correct_prediction = tf.equal(tf.argmax(out, 1), tf.argmax(one_hot_labels, 1))

		correct_prediction = tf.cast(correct_prediction, tf.float32)
		print(correct_prediction)
		accuracy = tf.reduce_mean(correct_prediction)

		try:
			step = 0
			while not coord.should_stop():
				start_time = time.time()
				#print('start_time:',start_time,'tttttttttttttt')
				
				feed_dict=noSG_fnn.fill_feed_dict(images_placeholder,
					labels_placeholder,x,y,sess=sess)
				loss_value, _ = sess.run([loss,train_op],feed_dict=feed_dict)
				# print('step',loss_value)
				duration = time.time() - start_time
				# Print an overview fairly often.
				summary_str = sess.run(summary, feed_dict=feed_dict)
				summary_writer.add_summary(summary_str, step)
				summary_writer.flush()
				if step % 100 == 0 :
					print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
					checkpoint_file = os.path.join(FLAGS.log_dir, 'model.ckpt')
					saver.save(sess, checkpoint_file, global_step=step)
					'''
					testi = step
				 	feed_dict = noSG_fnn.fill_feed_dict(images_placeholder,labels_placeholder,
				 		x_test,y_test,sess=sess)
				 	test_loss,accuracy_,abcd_,out_= sess.run([loss,accuracy,one_hot_labels,out],
				 		feed_dict=feed_dict)
				 	print('testyyyyyyyy')
				 	print('Step %d: test loss  = %.2f (%3f sec),accuracy:%.2f'% (testi, test_loss,
				 		duration,accuracy_))
					'''
				 	
				step += 1				
		except tf.errors.OutOfRangeError:
			print('Done training for %d epochs, %d steps.' % (FLAGS.num_epochs, step))
			end = time.time()
			print (end-now)
		finally:
			#draw_P_R_curve(images_placeholder,labels_placeholder, x_test,y_test,sess,loss,accuracy,one_hot_labels,out)
			draw_ROC_curve(images_placeholder,labels_placeholder, x_test,y_test,sess,loss,accuracy,one_hot_labels,out)

			# When done, ask the threads to stop.
			#checkpoint_file = os.path.join(FLAGS.log_dir, 'model.ckpt')
			#saver.save(sess, checkpoint_file, global_step=step)
			coord.request_stop()
			
		# Wait for threads to finish.
		coord.join(threads)
		sess.close()


def main(_):
#	now = time.time
	print(FLAGS.log_dir)
	if tf.gfile.Exists(FLAGS.log_dir):
		tf.gfile.DeleteRecursively(FLAGS.log_dir)
	tf.gfile.MakeDirs(FLAGS.log_dir)
	run_training()
#	end = time.time()
#	print (end-now)

if __name__ == '__main__':
	FLAGS= parser.parse_args()
	tf.app.run()
