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
start_frame = 89 # 开始时间 (单位秒 sec)
end_frame = 95 # 结束时间 (单位秒 sec)
channal = 0 # 声道,(0: 1声道,1 2声道)

assets = 'assets/wav/'
name = wavflie.split('.')[0]

Frequency, signalData = wavfile.read(assets+wavflie)
total_time = int(np.floor(len(signalData)/Frequency))
# sample_range = np.arange(31,200,1)
# total_samples = len(sample_range)
print('Frequency:',Frequency)
print('total_time(sec):',total_time)
print('data size:',signalData.size)
print('data len:',len(signalData))
data = signalData[:,channal][start_frame*Frequency:end_frame*Frequency]
# show Image
plot.subplot(311)
plot.title('Spectrogram of a wav file with '+name,fontproperties = ChineseFont)
plot.xlabel('Sample')
plot.ylabel('Amplitude')
plot.plot(data)

plot.subplot(312)
plot.xlabel('Time')
plot.ylabel('Frequency')
plot.specgram(data,Fs=Frequency,NFFT =2048,cmap=cm.gray ) # plot.specgram(signalData[:,0],Fs=Frequency)




plot.subplot(313)
CHUNK = int(Frequency/20)
f, t, Sxx = signal.spectrogram(data)
print('len Sxx:',len(Sxx))
print('size Sxx:',Sxx.size)
# # filter frequencies
# fmin = 30# Hz
# fmax = 40 # Hz
# freq_slice = np.where((f >= fmin) & (f <= fmax))
# data  = data[freq_slice]# keep only frequencies of interest
# Sxx = Sxx[freq_slice,:][0] 
# dBS = 10 * np.log10(Sxx)
plot.plot(Sxx) # plot.pcolormesh(t, f, dBS)
print('len Sxx:',len(Sxx))
print('size Sxx:',Sxx.size)
print(Sxx)
plot.show()

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

# %%
# ##save Image
# CM = 1/2.54  # cm in inches
# plot.figure(figsize=(7*CM,9*CM))
# plot.specgram(signalData,Fs=samplingFrequency,cmap=cm.gray)
# plot.axis('off')
# plot.savefig(name+'.png',bbox_inches='tight', pad_inches = 0,dpi=(100))





# %%
