# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from django.conf import settings
import os
import sys
import numpy as np
import tensorflow as tf


#load graph

with tf.gfile.FastGFile(os.path.join(settings.BASE_DIR,"classify/tf_files/retrained_graph.pb"),'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def,name='')

#init session
sess = tf.Session()
softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

#load labels
labels = [line.rstrip() for line in tf.gfile.GFile(os.path.join(settings.BASE_DIR,'classify/tf_files/retrained_labels.txt'))]

def get_class(file_name):

    image_data = tf.gfile.FastGFile(os.path.join(settings.BASE_DIR,'classify/newdata/%s'%file_name), 'rb').read()
   
    predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0':image_data})
    top_k = predictions.argsort()[-5:]
    return labels[top_k[0][::-1][0]]

