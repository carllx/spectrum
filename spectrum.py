# [参考Audio spectrum extraction from audio file by python] (https://stackoverflow.com/questions/24382832/audio-spectrum-extraction-from-audio-file-by-python)
# [Python audio spectrum analyzer] (https://medium.com/quick-code/python-audio-spectrum-analyser-6a3c54ad950)
# ffmpeg -i "d:\PROJECTS\spectrumFoJiao\assets\01佛说阿弥陀经.mp3" -ss 60 -t 10 -vn -acodec pcm_s16le -ac 1 -ar 44100 -f wav "d:\PROJECTS\spectrumFoJiao\assets\01佛说阿弥陀经.10.wav"
# youtube-dl -f bestaudio --extract-audio --audio-format wav --audio-quality 0 https://www.youtube.com/watch?v=LJUaXNaQwrE
# -ss 60 means, "start from second 60"
# -t 15 audio output length in seconds.. in this case, 15 seconds..






# # spectrum
# from scipy.fftpack import fft # fourier transform
# n = len(Audiodata)
# AudioFreq = fft(Audiodata)
# AudioFreq = AudioFreq[0:int(np.ceil((n+1)/2.0))] #Half of the spectrum
# MagFreq = np.abs(AudioFreq) # Magnitude
# MagFreq = MagFreq / float(n)
# # power spectrum
# MagFreq = MagFreq**2
# if n % 2 > 0: # ffte odd
#     MagFreq[1:len(MagFreq)] = MagFreq[1:len(MagFreq)] * 2
# else:# fft even
#     MagFreq[1:len(MagFreq) -1] = MagFreq[1:len(MagFreq) - 1] * 2


# plt.figure()
# freqAxis = np.arange(0,int(np.ceil((n+1)/2.0)), 1.0) * (fs / n);
# plt.plot(freqAxis/1000.0, 10*np.log10(MagFreq)) #Power spectrum
# #Spectrogram
# N = 512 #Number of point in the fft
# f, t, Sxx = signal.spectrogram(Audiodata, fs,window = signal.blackman(N),nfft=N)






#import the pyplot and wavfile modules
#%%
import matplotlib.pyplot as plot
from scipy.io import wavfile
import numpy as np
import matplotlib.cm as cm
from matplotlib import gridspec


# wavflie = 'assets/01佛说阿弥陀经.10.wav'
# wavflie = 'assets/白財神咒.wav'
# wavflie = 'assets/普巴金剛心咒 喇嘛 唱誦.wav'


# wavflie = 'assets/十小咒念誦【中文字幕】-QEyJfpJMYIE.wav'
# wavflie = 'assets/《十小咒》 萬佛聖城唱誦 高清-vM-2EY_up18.wav'
# wavflie = 'assets/十小咒-DWVFn8xxrH8.wav'
# wavflie = 'assets/十小咒 ~ 妙喜居士  持誦-ozEinsl8oww.wav'
# wavflie = 'assets/十小咒【如意寶輪王陀羅尼】印良法師-TrGhWl0dDxo.wav'
# wavflie = 'assets/般若心経 (cho ver.) at 京都・天龍寺【MV】  _ 薬師寺寛邦 キッサコ-wyUaRYLTbr0.wav'
# wavflie = 'assets/Chö Lineage Prayer-dDuJs7Cmdw8.wav'
wavflie = 'assets/大吉祥天女咒_吉祥天女咒_善女天咒_《早晚课诵集》十小咒之一_功德利益_梵文_梵音_教念_念诵_念法_佛教_歌曲_ 梵呗_梵唱_陀罗尼-5utLR2L7BK8.wav'
name = wavflie.split('/')[1].split('.')[0]


# Read the wav file (mono)conda install -c conda-forge librosa
# 截取 https://stackoverflow.com/questions/53797199/perform-fft-for-every-second-on-wav-file-with-python
Frequency, signalData = wavfile.read(wavflie)
total_time = int(np.floor(len(signalData)/Frequency))
print('Frequency:',Frequency)
print('total_time(sec):',total_time)
print('size:',signalData.size)
print('len:',len(signalData))
#%%
# sample_range = np.arange(31,200,1)
# total_samples = len(sample_range)


# show Image
# Plot the signal read from wav file
# plot.subplot(211)
# plot.title('Spectrogram of a wav file with piano music')
# plot.specgram(signalData,Fs=Frequency,cmap=cm.gray)
# plot.specgram(signalData,Fs=Frequency,cmap=cm.bone)


# specgram
# sides ='twosided'
# cmap=cm.twilight
# plot.specgram(signalData[:,0][32*Frequency:200*Frequency],Fs=Frequency,NFFT =4096 )
# plot.specgram(signalData[:,0][75*Frequency:90*Frequency],Fs=Frequency,NFFT =2048,cmap=cm.terrain )
plot.xlabel('Time')
plot.ylabel('Frequency')
# plot.specgram(signalData[:,1][50*Frequency:100*Frequency],Fs=Frequency,NFFT =2048,cmap=cm.gray )
plot.specgram(signalData[:,0],Fs=Frequency,NFFT =4096,cmap=cm.gray )
plot.show()


# save Image
# CM = 1/2.54  # cm in inches
# plot.figure(figsize=(7*CM,9*CM))
# plot.specgram(signalData,Fs=samplingFrequency,cmap=cm.gray)
# plot.axis('off')
# plot.savefig(name+'.png',bbox_inches='tight', pad_inches = 0,dpi=(100))




# %%