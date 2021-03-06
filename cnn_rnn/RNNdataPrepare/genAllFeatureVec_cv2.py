import numpy as np
import random as rd

import sys
import os
import os.path as path
from os.path import join as pj
import tensorflow as tf
import cv2 as cv

cwd = r'/home/hzx/tensorflow_intro_practice'
cwd = r'E:\github_repo\tensorflow_intro_practice'
sys.path.append(pj(cwd, 'cnn_rnn'))
import cnn

# a = '011'
# b = int(a)
# print(b)

# dir = r'D:\Lab408\cnn_rnn'

# os.chdir(dir)

# for i in range(80, 101):
#   with open('%06d.txt' % i, 'w') as f:
#     f.write(str(i))
# l = os.listdir(os.getcwd())
# print(l)

t_logits = 0
model = 0

def main():
  global t_logits
  global model
  srcDir = r'/home/all_data'
  dstDir = r'/home/all_data/77featureVectorNpy'

  # srcDir = r'D:\Lab408\cnn_rnn\src_dir'
  # dstDir = r'D:\Lab408\cnn_rnn\dst_dir'
  videoIdList = range(1, 78)
  videoIdList = range(1, 5)
  # videoIdList = range(11, 12)
  if not path.exists(dstDir):
    os.mkdir(dstDir)

  inputx = tf.placeholder(tf.uint8, shape=[None, 250, 250, 3])
  
  # model = cnn.CNN(data_format = 'NHWC')
  model = cnn.CNN(data_format = 'NCHW')
  t_logits = model(inputx)
  # print(logits.shape.dims)
  # print(model.feature2rnn.shape.dims)
  # return 
  
  saver = tf.train.Saver()
  ckptDir = r'D:\Lab408\monitored_sess_log_all_two_4.17\monitored_sess_log\ckpts'
  ckptDir = r'D:\Lab408\monitored_sess_log_all_two_4.17\ckpt'
  ckptDir = r'/home/tensorflow_intro_practice/cnn_rnn/cnn_fire_ckpt'
  # state = tf.train.get_checkpoint_state(ckptDir)
  # print(type(state))
  # if ckpt and ckpt.model_checkpoint_path:

  latestCkpt = tf.train.latest_checkpoint(ckptDir)
  # print(latestCkpt)
  # return

  sess_conf = tf.ConfigProto()
  sess_conf.gpu_options.allow_growth = True
  sess_conf.gpu_options.per_process_gpu_memory_fraction = 0.9
  
  with tf.Session(config= sess_conf) as sess:
    # sess.run(tf.global_variables_initializer())
    saver.restore(sess, latestCkpt)
    for videoId in videoIdList:
      handelVideoFrames(sess, inputx, srcDir, dstDir, videoId)

  return

def handelVideoFrames(sess, inputx, srcDir, dstDir, videoId):
  video_dir = '%03d' % videoId
  perFramesDir = pj(srcDir, video_dir)
  dstNpyDir = pj(dstDir, video_dir)
  if not path.exists(dstNpyDir):
    os.mkdir(dstNpyDir)
  
  # fire_begin_frame = 66
  # fire_biggest_frame = 95
  # fire_over_frame = 183
  
  jpglist = os.listdir(perFramesDir)
  jpglist = [f for f in jpglist if path.splitext(f)[1]=='.jpg']
  # jpglist = jpglist[54:55]
  # jpglist = jpglist[54:62]
  # print(len(jpglist))
  # print(jpglist[0])
  # print(path.splitext(jpglist[0])[0])
  # print(path.splitext(jpglist[0])[1])

  os.chdir(perFramesDir)
  for jpg in jpglist:
    # img_raw = tf.read_file(jpg)
    # decoded = tf.image.decode_jpeg(img_raw)
    # resized = tf.image.resize_images(decoded, [250, 250])
    # reshaped = tf.reshape(resized, [-1, 250, 250, 3])
    # print('reshaped shape: ')
    # print(reshaped.shape.dims)
    img = cv.imread(jpg)
    resized = cv.resize(img, (250, 250)) # w, h
    # print(type(resized[0, 0, 0]))
    # logits = sess.run(t_logits, feed_dict= 
    #     {inputx: [resized], model.is_training: False})
    # print(logits[0])
    feature2rnn = sess.run(model.feature2rnn, feed_dict= 
        {inputx: [resized], model.is_training: False})
    # print(feature2rnn[0])
    # print(jpg)
    basename = path.splitext(jpg)[0] # 000011 etc
    # print('basename: ' + basename)
    np.save(pj(dstNpyDir, basename), feature2rnn[0]) # ext .npy
    print(pj(dstNpyDir, basename)+'.pny')
  return

def tst():
  batch_vec = np.zeros((16,128), np.float)
  f = r'D:\Lab408\cnn_rnn\src_dir\011\000000.jpg'
  img = cv.imread(f)
  resized = cv.resize(img, (320, 240))
  print(resized.dtype)
  print(img.shape)

  f = r'D:\Lab408\cnn_rnn\dst_dir\011\000054.npy'
  nda = np.load(f)
  print(nda)
  print(nda.shape) # (128,)

  return

if __name__ == '__main__':
  tst()
  # main()