# -*- coding:utf-8-*-

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
import operator
from collections import OrderedDict
import json
from sklearn.metrics import average_precision_score
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import roc_auc_score

parser = noSG_fnn.parser

parser.add_argument('--test_path', type=str, default='/Users/dongxq/Desktop/disulfide/validation_ssbond/val_neg_noSG_distance_ssbond_.npy',
                    help='Directory where to write event logs.')
parser.add_argument('--checkpoint_dir', type=str, default='/Users/dongxq/Desktop/SSBOND_supplement/rootpath40/log/',
                    help='Directory where to read model checkpoints.')

parser.add_argument(
	'--predict_path',
	type=str,
	# default='/Users/dongxq/Desktop/disulfide/other_set_map/bril272cys_select_ca_full_possible_ssbond_nr.npy',
	default='/Users/dongxq/Desktop/disulfide/noSG_predict_test/brilM_ca_full_noSG_ssbond_nr.npy',
	help='path with the Validation data.'
)
parser.add_argument(
	'--predict_ord_path',
	type=str,
	# default='/Users/dongxq/Desktop/disulfide/other_set_map/bril272cys_select_ca_possible_ssbond_id_nr.npy',
	default='/Users/dongxq/Desktop/disulfide/noSG_predict_test/brilM_ca_noSG_ssbond_id_nr.npy',
	help='path with the Validation data id.'
)
parser.add_argument(
	'--mutate_pos_path',
	type=str,
	# default=os.path.join('/Users/dongxq/Desktop/disulfide/other_set_map','7211_possible_ssbond_id_nr.npy'),
	
	default='/Users/dongxq/Desktop/disulfide/other_test_set/mutational_structrue_bril_flavodoxin/bril_ssbond.npy',#bril_ssbond.npy,GLP1R_ssbond.npy,flavodoxin_ssbond.npy,
	help='the mutate pos.'
)
parser.add_argument(
	'--test_label',
	type=bool,
	# default=False,
	help='path with the Validation data.'
)
FLAGS = parser.parse_args()

def draw_ROC_curve(y_label,y_score):

	fpr, tpr, thresholds = roc_curve(y_label, y_score)
	roc_auc = auc(fpr, tpr)
	print(thresholds)
	print(len(thresholds))
	print(roc_auc_score(y_label, y_score))
	plt.figure()
	lw = 2
	plt.plot(fpr, tpr, color='darkorange',
	         lw=lw, label='ROC curve (area = %0.4f)' % roc_auc)
	plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
	plt.xlim([0.0, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Bril receiver operating characteristic')
	plt.legend(loc="lower right")
	plt.show()

def record_mutate_pos(dict_result):
	# ssbonds_detect = np.load('/Users/dongxq/Desktop/disulfide/other_test_set/mutational_structrue_bril_flavodoxin/bril_dict.npy')#flavodoxin_ssbond.npy
	with open("/Users/dongxq/Desktop/disulfide/other_test_set/mutational_structrue_bril_flavodoxin/bril_dict_new.json",'r') as load_f:
	   ssbonds_detect = json.load(load_f)
	print(ssbonds_detect)
	print(sys.getdefaultencoding())
	
	print(ssbonds_detect['16-29'])
	k = 1
	rank_dict = {}
	label_socre = []
	# print ssbonds_detect
	for item in dict_result:
		k += 1;
		# print(item)
		temp = item.split('-')

		temp_list = (str(filter(str.isdigit,temp[0]))+'-'+str(filter(str.isdigit,temp[1]))).decode('utf8')
		print(temp_list,'jjjjjjjjjjjjjjj')
		if temp_list in ssbonds_detect.keys():
			#print(repr(temp_list))
			# rank_dict[item] = str(float('%.3f'% (k/float(len(dict_result))))*100) + '%'
			rank_dict[temp_list] = dict_result[item]
			label_socre.append([ssbonds_detect[temp_list],dict_result[item]])
			print(label_socre)

	# draw_ROC_curve()
	new_label_socre = np.array(label_socre)
	# print(label_socre)
	print(new_label_socre[:,1])
	draw_ROC_curve(new_label_socre[:,0],new_label_socre[:,1])
	# print(rank_dict)
	# print(ssbonds_detect)

def test(sess,images,labels,logits,out):
	data = np.load(FLAGS.test_path).reshape((-1,100))
	one_hot_labels=tf.one_hot(labels,axis=-1,depth=2)

	correct_prediction = tf.equal(tf.argmax(out, 1), tf.argmax(one_hot_labels, 1))
	correct_prediction = tf.cast(correct_prediction, tf.float32)
	accuracy = tf.reduce_mean(correct_prediction)

	if FLAGS.test_label:
		make_labels = np.ones(len(data))
	else:
		make_labels=np.zeros(len(data))
	accuracy_,abcd_,out_= sess.run([accuracy,one_hot_labels,out],feed_dict={images:data,labels:make_labels})
	print('accuracy is :%.2f'% accuracy_)

def predict(sess,images,labels,logits,out):

	data = np.load(FLAGS.predict_path)
	name = FLAGS.predict_path.split('/')[-1].split('_')[0]
	ssbonds_detect = np.load(FLAGS.mutate_pos_path)
	out_ = sess.run(out,feed_dict={images:data.reshape((len(data),100))})
	id_ord = np.load(FLAGS.predict_ord_path)
	count = 0
	result_dict = {}
	# result_dict1 = {}

	with open('/Users/dongxq/Desktop/disulfide/predict/%s.txt'%name, 'w') as wf:
		for outi in range(len(out_)):
			# print(id_ord[outi],out_[outi])
			if(out_[outi][1] > out_[outi][0]):
				count += 1
				print(id_ord[outi],out_[outi])
				result_dict[id_ord[outi][0]+'-'+id_ord[outi][1]] = out_[outi][1]
				# result_dict1.setdefault(key，[]).append(value)
			# wf.write(id_ord[outi])
			# wf.write(':')
			# wf.write(str(out_[outi]))
			# wf.write('\n')

	print(len(id_ord),count)
	print('****** The probability of the mutate pos ********')
	mutate_pos_ord = [None for i in range(len(id_ord))]
	# print(mutate_pos_ord)
	with open('/Users/dongxq/Desktop/disulfide/predict/%s.txt'%name, 'a') as wf:
		for i in range(len(id_ord)):
			# if filter(str.isdigit,id_ord[i][0]) == '193' and filter(str.isdigit,id_ord[i][1]) == '233':
			# 	print (filter(str.isdigit,id_ord[i][0]),filter(str.isdigit,id_ord[i][1]))
			# 	break
			mutate_pos_ord[i] = [filter(str.isdigit,id_ord[i][0]),filter(str.isdigit,id_ord[i][1])]
			# wf.write(filter(str.isdigit,id_ord[i][0]) + ',')
			# wf.write(filter(str.isdigit,id_ord[i][1]))
			# wf.write('\n')
			wf.write(id_ord[i][0] + ',')
			wf.write(id_ord[i][1])
			wf.write('\n')
		for ssbonds in ssbonds_detect:
			# try:
			if ssbonds.tolist() in mutate_pos_ord:
				wf.write(ssbonds)
				wf.write(':' + str(out_[mutate_pos_ord.index(ssbonds.tolist())]))
				wf.write('\n')
				print(ssbonds,out_[mutate_pos_ord.index(ssbonds.tolist())])
			else:
				continue
		# 	# rmchr_id_ord.index(ssbonds.tolist())
		# 	# if ssbonds == ['193','233']
			
				# print('probability of the pos (%s,%s) is %0.3f%%'%(ssbonds[0],ssbonds[1],out_[mutate_pos_ord.index(ssbonds.tolist())][1]*100))
			# except ValueError:
			# 	continue
	print('finish predict.')

	sorted_result_dict = sorted(result_dict.iteritems(), key=operator.itemgetter(1), reverse=True)  
	final_dict = OrderedDict()

	for item in sorted_result_dict:
		# print item[0],item[1]
		final_dict[item[0]] = item[1]

	# print(result_dict)
	# print(final_dict)
	record_mutate_pos(final_dict)
	return result_dict

def predict_one_map(sess,images,file,out):
	data = np.load(file).reshape((-1,100))
	out_ = sess.run(out,feed_dict={images:data.reshape((len(data),100))})
	print(out_)
	# print(tf.argmax(out, 1))
	

def main(argv=None): 
	# print(FLAGS)
	sess=tf.Session() 
	
	ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
	print(ckpt)
	ckpt_path = ckpt.all_model_checkpoint_paths[-1]
	saver = tf.train.import_meta_graph(ckpt_path + '.meta')
	saver.restore(sess,ckpt_path)
	# saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path + '.meta')
	# saver.restore(sess, ckpt.model_checkpoint_path + '-100')

	graph = tf.get_default_graph()

	images = graph.get_tensor_by_name('image:0')
	labels=graph.get_tensor_by_name('labels:0')

	logits = graph.get_tensor_by_name('softmax_linear/add:0')
	# logits = new_fnn.inference(images, 128, 32)
	out=tf.nn.softmax(logits=logits)
	test(sess,images,labels,logits,out)

	result_dict = predict(sess,images,labels,logits,out)
	# return result_dict
	# test(sess,images,labels,logits,out)

	# predict_one_map(sess,images,'/Users/dongxq/Desktop/disulfide/predict_analysis/27_79change5_610.npy',out)

if __name__ == '__main__':
	
	tf.app.run()
