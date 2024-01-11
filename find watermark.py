import scipy.io.wavfile  # for sound file
import matplotlib.pyplot as plt
import numpy as np
import pywt
from scipy.signal import find_peaks

watermark = np.array([10,0,0,0,0,0,10,0,10,10,10,10,0,0,0,0,10,0,0,0,0,10,10,0,0,0,0,10,0,0,0,10,10,0])
def dwt_find_function():
    global channel1
    for i in range(0, len(peaks_massive_channel1)):
        # dwt with mass0
        cA1, cD1 = pywt.dwt(dic_mass_channel1["mass_chan10"], 'db2')
        cA2, cD2 = pywt.dwt(cA1, 'db2')
        cA3, cD3 = pywt.dwt(cA2, 'db2')
        cA4, cD4 = pywt.dwt(cA3, 'db2')
        cA5, cD5_dwt = pywt.dwt(cA4, 'db2')
    return cD5_dwt

def dwt_input_function():
    global channel2
    for i in range(0, len(peaks_massive_channel2)):
        # dwt with mass0
        cA1, cD1 = pywt.dwt(dic_mass_channel2["mass_chan20"], 'db2')
        cA2, cD2 = pywt.dwt(cA1, 'db2')
        cA3, cD3 = pywt.dwt(cA2, 'db2')
        cA4, cD4 = pywt.dwt(cA3, 'db2')
        cA5, cD5_clean = pywt.dwt(cA4, 'db2')
    return cD5_clean

# music folder
temp_folder = "D:\\PythonProjects\\"


# read wav file
rate, audData = scipy.io.wavfile.read(temp_folder + "watermark_audio1123.wav")

print("The sampling rate - " + str(rate))
print("The total number of data - " + str(audData.shape[0]))
print("The number of channels (i.e. is it mono or stereo) is - " + str(audData.shape[1]))
print("The wav length is " + str(audData.shape[0] / rate) + " seconds")

# wav number of channels

channel1 = audData[:, 0]  # left
channel2 = audData[:, 1]  # right

# find peaks with distance channel1
peaks_channel1 = find_peaks(channel1, distance=100000)
peaks_massive_channel1 = peaks_channel1[0]
print("Number of peaks in file with distance channel1 - " + str(len(peaks_massive_channel1)))
print("Massive of peaks channel1 - " + str(peaks_massive_channel1))

# find peaks with distance channel2
peaks_channel2 = find_peaks(channel1, distance=100000)
peaks_massive_channel2 = peaks_channel2[0]
print("Number of peaks in file with distance channel2 - " + str(len(peaks_massive_channel2)))
print("Massive of peaks channel2 - " + str(peaks_massive_channel2))

# len array dwt
len_array = 1024

# create dict for name mass
dic_mass_channel1 = {}
dic_mass_channel2 = {}

# cycle for mass
for i in range(0, len(peaks_massive_channel1)):
    dic_mass_channel1["mass_chan1" + str(i)] = channel1[peaks_massive_channel1[i]:peaks_massive_channel1[i] + len_array]

for i in range(0, len(peaks_massive_channel2)):
    dic_mass_channel2["mass_chan2" + str(i)] = channel2[peaks_massive_channel2[i]:peaks_massive_channel2[i] + len_array]

cD7_dwt = dwt_find_function()
cD7_clean = dwt_input_function()

delta = cD7_dwt - cD7_clean

#plot
plt.figure(1)
plt.subplot(211)
plt.title("Вхідне повідомлення")
plt.plot(watermark*0.1, linewidth=0.5, alpha=1, color='#ff7f00')
plt.xlabel('Значення')
plt.ylabel('Двійкова система')
plt.subplot(212)
plt.title("Дешифроване повідомлення")
plt.plot(delta*0.1, linewidth=0.5, alpha=1, color='#ff7f00')
plt.xlabel('Значення')
plt.ylabel('Двійкова система')
plt.show()
