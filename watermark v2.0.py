import scipy.io.wavfile  # for sound file
import pydub  # for sound file
import numpy as np
import pywt
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

watermark = np.array([10,0,0,0,0,0,10,0,10,10,10,10,0,0,0,0,10,0,0,0,0,10,10,0,0,0,0,10,0,0,0,10,10,0])
def dwt_function():
    global channel1, watermark
    for i in range(0, len(peaks_massive)):
        # dwt with mass0
        cA1, cD1 = pywt.dwt(dic_mass["mass" + str(i)], 'db2')
        cA2, cD2 = pywt.dwt(cA1, 'db2')
        cA3, cD3 = pywt.dwt(cA2, 'db2')
        cA4, cD4 = pywt.dwt(cA3, 'db2')
        cA5, cD5 = pywt.dwt(cA4, 'db2')
        # add watermark and cD7
        cD5 = cD5 + watermark
        # decompozition
        cA4 = pywt.idwt(cA5, cD5, 'db2')
        cA3 = pywt.idwt(cA4, cD4, 'db2')
        cA2 = pywt.idwt(cA3, cD3, 'db2')
        cA1 = pywt.idwt(cA2, cD2, 'db2')
        mass_decompoz = pywt.idwt(cA1[:-1], cD1, 'db2')
        # channel1 with mass_decompoz
        channel1 = np.hstack((channel1[:peaks_massive[i]],mass_decompoz,channel1[peaks_massive[i]+len(mass_decompoz):]))


    return channel1

# music folder
temp_folder = "D:\\PythonProjects\\"
# test mp3 file
mp3_file = "Hardkiss20.mp3"

# read mp3 file
mp3 = pydub.AudioSegment.from_mp3(temp_folder + mp3_file)
# convert to wav
mp3.export(temp_folder + "testfile.wav", format="wav")
# read wav file
rate, audData = scipy.io.wavfile.read(temp_folder + "testfile.wav")

print("The sampling rate - " + str(rate))
print("The total number of data - " + str(audData.shape[0]))
print("The number of channels (i.e. is it mono or stereo) is - " + str(audData.shape[1]))
print("The wav length is " + str(audData.shape[0] / rate) + " seconds")

# wav number of channels

channel1 = audData[:, 0]  # left
channel2 = audData[:, 1]  # right
audData[:, 1] = audData[:, 0]

# find peaks with distance
peaks = find_peaks(channel1, distance=100000)
peaks_massive = peaks[0]
print("Number of peaks in file with distance - " + str(len(peaks_massive)))
print("Massive of peaks - " + str(peaks_massive))

# len array dwt
len_array = 1024

# create dict for name mass
dic_mass = {}

# cycle for mass
for i in range(0, len(peaks_massive)):
    dic_mass["mass" + str(i)] = channel1[peaks_massive[i]:peaks_massive[i] + len_array]

for i in range(0, len(peaks_massive)):
    dic_mass["mas2s" + str(i)] = channel2[peaks_massive[i]:peaks_massive[i] + len_array]

dwt_function()

# return audiodata
audData[:, 0] = channel1

# save new data as watermark_audio.wav
scipy.io.wavfile.write("D:\\PythonProjects\\watermark_audio1123.wav", rate, audData)

print(dic_mass["mass0"]-dic_mass["mas2s0"])
print(dic_mass["mass0"])
print(dic_mass["mas2s0"])


#plot
plt.figure(1)
plt.plot(watermark*0.1, linewidth=0.5, alpha=1, color='#ff7f00')
plt.xlabel('Значення')
plt.ylabel('Двійкова система')
plt.show()
