#%%
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.cm as cm
from matplotlib import gridspec
import struct
from math import sqrt
import IPython
import pydub 
from pydub.silence import split_on_silence
import pandas as pd

from scipy.interpolate import make_interp_spline, BSpline

#%%
# 调试一下静音参数达到最终输出 108 段音频
wavflie = '1_般若波罗蜜多咒.mp3'
channal = 0 # 声道,(0: 1声道,1 2声道)
min_silence_len = 16 # interge
silence_thresh = -15.6 # float,defult-16


assets = 'assets/wav/'
name = wavflie.split('.')[0]
# Load your audio.
# pyhub 转换scipy可用的数组  https://github.com/jiaaro/pydub/issues/424
audio = pydub.AudioSegment.from_mp3(assets+wavflie)
signalData = np.array(audio.get_array_of_samples())
if audio.channels == 2:
    signalData = signalData.reshape((-1, 2))  #if normalized:#return a.frame_rate, np.float32(y) / 2**15
Frequency =  audio.frame_rate
N = signalData.shape[0] #相当与 len(signalData)

chunks = split_on_silence (
    audio, 
    min_silence_len = min_silence_len,
    silence_thresh = silence_thresh
    # keep_silence=10,
)

print('Frequency:',Frequency)
print('data size:',signalData.size)
print ("channel's'count", audio.channels) #2
print ("Complete Samplings N:", N)
print('len(chunks):',len(chunks))# 调试至 108 

#%%
# 产生RMS:首位填充0 的相当len 的 array
# ---------
RMS = []
# # 每个音节
for i, chunk in enumerate(chunks):
    
    data = np.array(chunks[i].get_array_of_samples())
    f, t, Sxx = signal.spectrogram(data)
    dBS = 10 * np.log10(Sxx) 
    rms = np.sqrt(sum(Sxx**2) / N)
    RMS.append(rms)
    # print(len(RMS)) 

df = pd.DataFrame(RMS,dtype=float)
# RMS = df.fillna(method="bfill").values # 拉伸填充
df.insert(0,"0",np.zeros(108)) #第一列填充0
RMS = df.fillna(value=0.0).values
print('每row 的个数:1-',len(RMS[0]))


#%%
# 输出图形 108张截面 plot
# ---------
fig = plt.figure(figsize=(5,len(RMS)))
spec = gridspec.GridSpec(ncols=1, nrows=len(RMS))
for i, chunk in enumerate(RMS):
    ax = fig.add_subplot(spec[i])
    ax.plot(chunk)# plot.pcolormesh(t, f, dBS),



#%%
# specgram
# ---------
# plot.specgram(samples,Fs=Frequency,NFFT =2048,cmap=cm.gray ) 
# f, t, Sxx = signal.spectrogram(samples)
# # samples = chunks[0].get_array_of_samples()
# # samples = np.array(samples)
# # print(samples)
# # plot.plot(samples)
# %%
