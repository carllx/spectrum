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
import json
from scipy.interpolate import make_interp_spline, BSpline

#%% [markdown]
# ## 调试配置参数


#%%
# 调试一下静音参数达到最终输出音频段数 例如:108 段音频
# wavflie = '1_般若波罗蜜多咒.mp3'
# channal = 0 # 声道,(0: 1声道,1 2声道)
# min_silence_len = 16 # interge
# silence_thresh = -15.6 # float,defult-16

# wavflie = '1_般若波罗蜜多咒.mp3'
# channal = 0 # 声道,(0: 1声道,1 2声道)
# min_silence_len = 98 # interge
# silence_thresh = -16 # float,defult-16

# wavflie = '1、如意宝轮王陀罗尼.mp3'
# channal = 0 # 声道,(0: 1声道,1 2声道)
# min_silence_len = 110 # interge
# silence_thresh = -16 # float,defult-16

# wavflie = '2、消灾吉祥神咒.mp3'
# channal = 0 # 声道,(0: 1声道,1 2声道)
# min_silence_len = 97 # interge
# silence_thresh = -16 # float,defult-16

wavflie = '3、功德宝山神咒.mp3'
channal = 0 # 声道,(0: 1声道,1 2声道)
min_silence_len = 79 # interge
silence_thresh = -16 # float,defult-16



# 预设参数
name = wavflie.split('.')[0]
assets = 'assets/wav/'
exports = 'exports/'

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
len_rows = len(chunks)

print('Frequency:',Frequency)
print('data size:',signalData.size)
print ("channel's'count", audio.channels) #2
print ("Complete Samplings N:", N)
print('len(chunks):',len_rows)# 调试至 108 


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

# 将不等的多位数组,规范居中的 dataframe

def get_df_alignCenter_from_mlist(array):
    # print (type(array)) #<class 'list'>
    signalsPointss = []
    for x in array:
        signalsPointss.append(len(x)) # 一行rms信号点个数
    
    len_array = max(signalsPointss) # 将会产生df 的 cols数
    for i, arr in enumerate(array):
        len_arr = len(arr)
        len_fill = round((len_array - len_arr)/2)
        zeroarr = [0] * len_fill
        arr= np.append(zeroarr,arr)
        arr= np.append(arr,zeroarr)
        
        array[i] = arr
    # 头尾静音数组
    zeros = np.zeros(len_array) 
    # print (type(zeros)) # <class 'numpy.ndarray'>
    # print (type(array)) # <class 'list'>
    # print (type(array[0])) # <class 'numpy.ndarray'>
    array.insert(0,zeros)
    array.insert(len(array),zeros)
    return array
RMS = get_df_alignCenter_from_mlist(RMS)
df = pd.DataFrame(RMS,dtype=float)

# 非居中可使用更简单高效方式
# df = pd.DataFrame(RMS,dtype=float)
# RMS = df.fillna(method="bfill").values # 拉伸填充

df = (df-df.min())/(df.max()-df.min()) # 将dataframe 内values 规范在指定范围内,[Normalization vs Standardization, which one is better](https://towardsdatascience.com/normalization-vs-standardization-which-one-is-better-f29e043a57eb)
df.insert(0,"0",np.zeros(len(df))) #第一列填充0
df = df.fillna(value=0.0)
RMS = df.values
print('number of rows: 1 ~',len(df)-2)
print('number of cols: 1 ~',len(df.columns)-2)



#%%
# Export Json
#--------------
outTXT = r'%s%s_splitRows%d.json'%(exports,name,len_rows)
result = df.to_json(outTXT,orient="values")
# parsed = json.loads(result)

#%%
# Show图形 108张截面 plot
# ---------
fig = plt.figure(figsize=(5,len(RMS)))
spec = gridspec.GridSpec(ncols=1, nrows=len(RMS))
for i, chunk in enumerate(RMS):
    ax = fig.add_subplot(spec[i])
    ax.plot(chunk) # plot.pcolormesh(t, f, dBS),


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
