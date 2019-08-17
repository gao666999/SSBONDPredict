# -*- coding:utf-8-*-
# from __future__ import unicode_literals
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import sys
import time
import numpy as np
import tensorflow as tf
import argparse
import os
import math
import exceptions
from . import noSG_fnn
from django.conf import settings  # added by xxli

checkpoint_dir = os.path.join(settings.BASE_DIR, 'static/newmodel')

def predict(args,sess,images,labels,logits,out):
    data = args[0]
    id_ord = args[1]
    name = args[2]
    out_ = sess.run(out,feed_dict={images:data.reshape((len(data),100))})
    count = 0
    result_dict = {}
    new_list=[]
    new_list_score = []
    #with open('/Users/dongxq/Desktop/disulfide/predict/%s.txt'%name, 'w') as wf:
    for outi in range(len(out_)):
        # calculating entropy
        if(out_[outi][1] > out_[outi][0]):
            count += 1
            number1 = id_ord[outi][0][4:]
            number2 = id_ord[outi][1][4:]
            distance = abs( int(number1) - int(number2) )
            if distance != 0:
                t = math.log(distance, )
                s = -2.1 - 1.5*8.314*t
                #s = float('%.3f'% ss)
                s = '%.4f'% s
            else:
                s = -2.1
                s = '%.3f'% s
            result_dict[id_ord[outi][0]+'-'+id_ord[outi][1]] = str('%.3f'% out_[outi][1]) + ' ' + str(s)
    print 'finish predict.'
    return result_dict



def main(args):
    sess=tf.Session()
    ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
    ckpt_path = os.path.join(checkpoint_dir, 'model.ckpt-800')  # modified by xxli
    #print(ckpt_path)
    saver = tf.train.import_meta_graph(ckpt_path + '.meta')
    saver.restore(sess,ckpt_path)
    graph = tf.get_default_graph()

    images = graph.get_tensor_by_name('image:0')
    labels=graph.get_tensor_by_name('labels:0')

    logits = graph.get_tensor_by_name('softmax_linear/add:0')
    # logits = new_fnn.inference(images, 128, 32)
    out=tf.nn.softmax(logits=logits)
    result_dict = predict(args,sess,images,labels,logits,out)
    return result_dict
if __name__ == '__main__':
    settings.configure()
    tf.app.run()
