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

from scipy.interpolate import make_interp_spline, BSpline

#%%
wavflie = '1_如意宝轮王陀罗尼.mp3'
start_frame = 36 # 开始时间 (单位秒 sec)
end_frame = 54 # 结束时间 (单位秒 sec)
channal = 0 # 声道,(0: 1声道,1 2声道)

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
    min_silence_len = 132,
    # keep_silence=10,
    # silence_thresh = -16
)

print('Frequency:',Frequency)
print('data size:',signalData.size)
print ("channel's'count", audio.channels) #2
print ("Complete Samplings N:", N)
print('len(chunks):',len(chunks))

fig = plt.figure(figsize=(5,len(chunks)))
spec = gridspec.GridSpec(ncols=1, nrows=len(chunks))
# # 每个音节
for i, chunk in enumerate(chunks):
    ax = fig.add_subplot(spec[i])
    # ax.plot(range(5), range(5, 10)
    
    data = np.array(chunks[i].get_array_of_samples())
    f, t, Sxx = signal.spectrogram(data)
    dBS = 10 * np.log10(Sxx) 
    rms = np.sqrt(sum(Sxx**2) / N)
    ax.plot(rms)# plot.pcolormesh(t, f, dBS),




# plot.specgram(samples,Fs=Frequency,NFFT =2048,cmap=cm.gray ) 
# f, t, Sxx = signal.spectrogram(samples)
# # samples = chunks[0].get_array_of_samples()
# # samples = np.array(samples)
# # print(samples)
# # plot.plot(samples)
# %%
