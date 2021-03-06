import numpy as np
import random as rd

import os
import os.path as path
from os.path import join as pj
import json

def main():
  tst()
  return

  with open('.json') as f:
    dat = json.load(f)
  dat = dat['fire_clips']

  srcDir = r''
  dstDir = r''
  labelList = {
      'raging':'raging',
      'invariant':'invariant', 
      'weaking':'weaking'}

  for it in dat:
    vedio_dir = it['vedio_dir']
    fire_begin_frame = it['fire_begin_frame']
    fire_biggest_frame = it['fire_biggest_frame']
    fire_over_frame = it['fire_over_frame']
    over_frame = it['over_frame']
    formatted = '%03d' % int(vedio_dir)
    srcFramesDir = pj(srcDir, formatted)

    perClassDir = pj(dstDir, labelList['raging'])
    dstFramesDir = pj(perClassDir, formatted)
    # dstDir/raging/077
    genStepedSeq(srcFramesDir, dstFramesDir,
          fire_begin_frame, fire_biggest_frame, 16)
    
    perClassDir = pj(dstDir, labelList['weaking'])
    dstFramesDir = pj(perClassDir, formatted)
    genStepedSeq(srcFramesDir, dstFramesDir,
          fire_biggest_frame, fire_over_frame, 16)

    # handleOne(it, srcDir, dstDir)
  return

# def handleOne(dict_item, srcDir, dstDir):
#   vedio_dir = dict_item['vedio_dir']
#   begin_frame = dict_item['begin_frame']
#   fire_begin_frame = dict_item['fire_begin_frame']
#   fire_biggest_frame = dict_item['fire_biggest_frame']
#   fire_over_frame = dict_item['fire_over_frame']
#   over_frame = dict_item['over_frame']
  
#   vedio_dir = '%03d' % int(vedio_dir)
#   genStepedSeq(pj(srcDir, vedio_dir), pj(dstDir, vedio_dir),
#       fire_begin_frame, fire_biggest_frame, 16, 128)
#   return
  

  # {"vedio_dir": "11","begin_frame":"0","fire_begin_frame":"0",
  #       "fire_biggest_frame":"17","fire_over_frame":"50","over_frame":"50"},
  #       {"vedio_dir": "11","begin_frame":"66","fire_begin_frame":"66",
  #       "fire_biggest_frame":"95","fire_over_frame":"183","over_frame":"183"}

# fv: feature vecotr
# shape=(帧数, fc_out)
def genStepedSeq(mVideoFV, dstSeqDir, startFrame, endFrame, seqLen, step=1):
  # flist = os.listdir(srcFramesDir)
  # flist = [f for f in flist if path.splitext[f][1]=='.npy']

  seqList = []
  border = endFrame + 1
  for i in range(startFrame, border, step):
    end = i+seqLen
    if end > border: # 分片越界
      break
    aSeq = mVideoFV[np.newaxis, i:end, :]
    seqList.append(aSeq)
    # fname = '%06d-%06d.npy' % (i, end-1)
    # f = pj(dstSeqDir, fname)
    # np.save(f, mVideoFV[i:end, :])
  buckSlice = np.concatenate(seqList) # (-1, seqLen, vecSize)

  fname = 'frameInterval-%d'
  
  return
  seq = np.zeros((seqLen, vecSize), np.float32)
  print(seq.shape)

def tst():
  i = 300
  seqLen = 16
  vecSize = 128
  s = '%06d-%06d.npy' %(i-seqLen+1, i)
  print(s)
  seq = np.zeros((seqLen, vecSize), np.float32)
  aa = seq[0:1, :]
  aa[0, 0] = 3.3
  print(seq[0, 0]) # 3.3

  aa = np.reshape(seq, (-1, seqLen, vecSize))
  # print(seq.shape) # (16, 128)
  # print(aa.shape) # (1, 16, 128)
  bb = seq[np.newaxis, 4:8, :]
  print(seq.shape) # (16, 128)
  # bb = np.expand_dims()
  print(bb.shape) # (1, 4, 128)
  l = [aa]*4
  b = np.concatenate(l)
  print(b.shape) # (4, 16, 128)
  return

  print(seq.shape)
  vedio_dir = '11'
  vedio_dir = '%03d' % int(vedio_dir)
  print(vedio_dir)
  npyDir = r'D:\Lab408\cnn_rnn\77featureVectorNpy'
  videoIdList = range(1, 78)
  for videoId in videoIdList:
    vId = '%03d.npy' % videoId
    f = pj(npyDir, vId)
    nda = np.load(f)
    print('%s shape[0]: %d' % (f, nda.shape[0]))
  

  # for i in range(0, 20):
  #   fname = '%06d' % i
  #   print(fname)
    
  # getOne('', '', '', 16, 128, 'ff.npy')

if __name__ == '__main__':
  tst()
  # main()