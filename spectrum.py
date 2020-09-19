# Terminal 启动  /Applications/Blender.app/Contents/MacOS/Blender
# 
# 科普 - 振幅/响度/音量/增益 大乱斗 https://zhuanlan.zhihu.com/p/38439252
# Read the wav file (mono)conda install -c conda-forge librosa
# 截取 https://stackoverflow.com/questions/53797199/perform-fft-for-every-second-on-wav-file-with-python
# [参考Audio spectrum extraction from audio file by python] (https://stackoverflow.com/questions/24382832/audio-spectrum-extraction-from-audio-file-by-python)
# [Python audio spectrum analyzer] (https://medium.com/quick-code/python-audio-spectrum-analyser-6a3c54ad950)
# youtube-dl -f bestaudio --extract-audio --audio-format wav --audio-quality 0 https://www.youtube.com/watch?v=LJUaXNaQwrE

#import the pyplot and wavfile modules
#%%
import matplotlib.pyplot as plot
from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.cm as cm
from matplotlib import gridspec
import struct
from math import sqrt
import IPython
from pydub import AudioSegment
from pydub.silence import split_on_silence
# 中文字体
from matplotlib.font_manager import FontProperties
ChineseFont = FontProperties(fname = '/Users/yamlam/Documents/GitHub/spectrum/assets/fonts/NotoSansSC-Regular.otf')






#%%
# CONFIG
# wavflie = '01佛说阿弥陀经.10.wav'
# wavflie = '白財神咒.wav'
# wavflie = '普巴金剛心咒 喇嘛 唱誦.wav'
# wavflie = '十小咒念誦【中文字幕】-QEyJfpJMYIE.wav'
# wavflie = '《十小咒》 萬佛聖城唱誦 高清-vM-2EY_up18.wav'
# wavflie = '十小咒-DWVFn8xxrH8.wav'
# wavflie = '十小咒 ~ 妙喜居士  持誦-ozEinsl8oww.wav'
# wavflie = '十小咒【如意寶輪王陀羅尼】印良法師-TrGhWl0dDxo.wav'
# wavflie = '般若心経 (cho ver.) at 京都・天龍寺【MV】  _ 薬師寺寛邦 キッサコ-wyUaRYLTbr0.wav'
# wavflie = 'Chö Lineage Prayer-dDuJs7Cmdw8.wav'
# wavflie = '大吉祥天女咒_吉祥天女咒_善女天咒_《早晚课诵集》十小咒之一_功德利益_梵文_梵音_教念_念诵_念法_佛教_歌曲_ 梵呗_梵唱_陀罗尼-5utLR2L7BK8.wav'
# wavflie = '法鼓山早課 [大悲咒十小咒早課] (法鼓山僧團) [有字幕]-A80SNDxLXvg.wav'
wavflie = '白財神咒（每天觀看常念咒語），可祛除貧病窮困之苦，消除罪業障礙，增上順緣，獲得受用無慮，屬無財信士起修之妙法（廣傳得福）-M2Aykg4hmJM.wav'
start_frame = 36 # 开始时间 (单位秒 sec)
end_frame = 54 # 结束时间 (单位秒 sec)
channal = 0 # 声道,(0: 1声道,1 2声道)

assets = 'assets/wav/'
name = wavflie.split('.')[0]

Frequency, signalData = wavfile.read(assets+wavflie)

channel_count = len(signalData.shape)
if channel_count == 2:
    signalData = signalData.sum(axis=1) / 2 # 相当于 signalData[:,channal],通道1:channal=0,通道2:channal=1
N = signalData.shape[0] #相当与 len(signalData)
secs = N / float(Frequency) #Frequency:fs_rate
total_time = int(np.floor(len(signalData)/Frequency))

print('Frequency:',Frequency)
print('data size:',signalData.size)
print ("channel's'count", channel_count) #2
print ("Complete Samplings N:", N)
print('total_time(sec):',total_time)
print ("secs",secs)

data = signalData[start_frame*Frequency:end_frame*Frequency]

# show Image
plot.subplot(411)
plot.title('Spectrogram of a wav file with '+name,fontproperties = ChineseFont)
plot.xlabel('Sample')
plot.ylabel('Amplitude')
plot.plot(data)

plot.subplot(412)
plot.xlabel('Time')
plot.ylabel('Frequency')
plot.specgram(data,Fs=Frequency,NFFT =2048,cmap=cm.gray ) # plot.specgram(signalData[:,0],Fs=Frequency)

plot.subplot(413)
CHUNK = int(Frequency/20)
f, t, Sxx = signal.spectrogram(data)
dBS = 10 * np.log10(Sxx) # 分贝（decibels/dB）
rms = np.sqrt(sum(Sxx**2) / N) # rms voltage/power ,方均根（Root Mean Square，縮寫為 RMS(符合正态分布才有效)
# print('rms data',rms)
plot.plot(rms) # plot.pcolormesh(t, f, dBS),


plot.subplot(414)
# print('len(Sxx)[0]:',len(Sxx[0]))
Sxx = Sxx.transpose()
print('len(Sxx):',len(Sxx))
print('len(rms):',len(rms))
scaleFactor = np.interp(rms, (rms.min(), rms.max()), (1.0, 100.0))
for idx, x in enumerate(Sxx):
    arr = np.interp(x, (x.min(), x.max()), (-100.0, +100.0))
    arr*= scaleFactor[idx]
    Sxx[idx] = arr
Sxx = Sxx.transpose()
plot.contourf(Sxx,cmap=cm.gray)
plot.show()

# %%
##save Image
CM = 1/2.54  # cm in inches
plot.figure(figsize=(70*CM,90*CM))
plot.specgram(data,Fs=Frequency,NFFT =2048,cmap=cm.gray ) 
plot.axis('off')
plot.savefig(name+'.png',bbox_inches='tight', pad_inches = 0,dpi=(100))



# %%
# IPython.display.Audio(data, rate=Frequency) # load a NumPy array

# %%
# specgram 参数
# sides ='twosided'
# cmap=cm.twilight
# plot.specgram(signalData,Fs=Frequency,cmap=cm.gray)
# plot.specgram(signalData,Fs=Frequency,cmap=cm.bone)
# plot.specgram(signalData[:,0][32*Frequency:200*Frequency],Fs=Frequency,NFFT =4096 )
# plot.specgram(signalData[:,0][75*Frequency:90*Frequency],Fs=Frequency,NFFT =2048,cmap=cm.terrain )

# struct, unpack the data into a numpy array.

# [f,t,Sxx] = spectrogram(_)
# f:ndarray -- Array of sample frequencies.
# t:ndarray -- Array of segment times.
# Sxx:ndarray -- Spectrogram of x. By default, the last axis of Sxx corresponds to the segment times.




# # filter frequencies
# fmin = 30# Hz
# fmax = 40 # Hz
# freq_slice = np.where((f >= fmin) & (f <= fmax))
# data  = data[freq_slice]# keep only frequencies of interest
# Sxx = Sxx[freq_slice,:][0] 