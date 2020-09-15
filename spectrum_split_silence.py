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
# from pydub.silence import split_on_silence
import pandas as pd
import json
from scipy.interpolate import make_interp_spline, BSpline
from scipy.ndimage.filters import gaussian_filter


#%% [markdown]
# ## 调试配置参数


#%%
# 调试一下静音参数达到最终输出音频段数 例如:108 段音频

# wavflie = '1_般若波罗蜜多咒.mp3' #38句 
# min_silence_len = 640 # interge 
# sigma = 4

# wavflie = '1、如意宝轮王陀罗尼.mp3' #10句 
# min_silence_len = 640 # interge
# sigma= 3


# wavflie = '3_大悲咒.mp3' #85句 
# min_silence_len = 640 # interge
# sigma= 3

# wavflie = '2_雨宝咒.mp3' #60句 
# min_silence_len = 640 # interge
# sigma= 4


# wavflie = '4_清心普善咒.mp3' #129句 
# min_silence_len = 640 # interge
# sigma= 3

# wavflie = '5_佛顶尊胜陀罗尼咒.mp3' #35句 
# min_silence_len = 640 # interge
# sigma= 4

# wavflie = '6_宝箧印陀罗尼咒注音.mp3' #38句 
# min_silence_len = 640 # interge
# sigma= 4.5


wavflie = '2、消灾吉祥神咒.mp3' #7段 # 一个区域太高
min_silence_len = 640 # interge
sigma= 5

# wavflie = '3、功德宝山神咒.mp3'
# min_silence_len = 79 # interge



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
print('dBFS:',audio.dBFS)
print('Frequency:',Frequency)
print('data size:',signalData.size)
print ("channel's'count", audio.channels) #2
print ("Complete Samplings N:", N)
# dBS = 10 * np.log10(Sxx) 
    # print(dBS)

 # 分割静音 
 #pydub.silence.detect_silence(
chunks =  pydub.silence.split_on_silence(
    audio, 
    # silence_thresh = audio.dBFS # float,defult-16
    # min_silence_len = min_silence_len,
    min_silence_len = 500,
    silence_thresh =-999, 
    
    # keep_silence=10,
)
len_rows = len(chunks)
chunks[0].export('split-.mp3', format='mp3',codec='mp3')
# for i, chunk in enumerate(chunks):
#     chunk.export('split-%d.mp3'%(i+1), format='mp3',codec='mp3')


print('len(chunks):',len_rows)# 调试至 108 


# 产生RMS: 每句话一行(sentence/rows)的array(首位填充0)
# ---------
RMS = []

# # 每个音节
for i, chunk in enumerate(chunks):
    data = np.array(chunks[i].get_array_of_samples())
    f, t, Sxx = signal.spectrogram(data)
    rms = np.sqrt(sum(Sxx**2) / N)
    # rms = gaussian_filter(rms, sigma=20) # 高斯模糊
    RMS.append(rms)
    
    # print(len(RMS)) 

# 将不等的多位数组,规范居中的 dataframe

def get_df_alignCenter_from_mlist(array):
    # print (type(array)) #<class 'list'>
    signalsPoints = []
    for x in array:
        signalsPoints.append(len(x)) # 一行rms信号点个数
    
    len_cols = max(signalsPoints) #df 的 cols数
    for i, row in enumerate(array):
        len_arr = len(row)
        len_fill = round((len_cols - len_arr)/2)
        zeroarr = [0] * len_fill
        row= np.append(zeroarr,row)
        row= np.append(row,zeroarr)
        array[i] = row
    return array # <class 'list'>,array[0] # <class 'numpy.ndarray'>

RMS = get_df_alignCenter_from_mlist(RMS)
# 每rows头尾插入静音数组
RMS_0 = RMS.copy()
len_cols = len(RMS_0[0])
zeros = np.zeros(len_cols) # <class 'numpy.ndarray'>

for x in range(len(RMS_0)):
    RMS_0.insert(2*x+1, zeros)
RMS_0.insert(0,zeros)


# Gaussian blur DataFrame
#------------------------------
df = pd.DataFrame(RMS_0,dtype=float)
# 非居中可使用更简单高效方式
# df = pd.DataFrame(RMS,dtype=float)
# RMS = df.fillna(method="bfill").values # 拉伸填充
# 将dataframe 内values 规范在指定范围内,
# df = (df-df.min())/(df.max()-df.min()) # 某些峰位会被截掉 [Normalization vs Standardization, which one is better](https://towardsdatascience.com/normalization-vs-standardization-which-one-is-better-f29e043a57eb)
# df.insert(0,"0",np.zeros(len(df))) #第一列填充0
df = df.fillna(value=0.0)
RMSG = df.values
RMSG = gaussian_filter(RMSG, sigma=sigma)
print('number of rows: 1 ~',len(df)-2)
print('number of cols: 1 ~',len(df.columns)-2)



# Export Json
#--------------——
df = pd.DataFrame(data=RMSG)
outTXT = r'%s%s_splitRows%d.json'%(exports,name,len_rows)
result = df.to_json(outTXT,orient="values")
print(outTXT,'is outputed')
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
