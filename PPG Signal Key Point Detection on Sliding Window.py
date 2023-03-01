
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd
from scipy.misc import electrocardiogram

#get ready to use ECG signal
rawsignals=pd.read_csv(r'C:\Users\umuts\Desktop\mimic_perform_non_af_csv\mimic_perform_non_af_csv\mimic_perform_non_af_001_data.csv')

ecg = rawsignals["PPG"].to_numpy()[0:14000]

#sampling frequency 360Hz
fs = 125
# generating time axis values
time = np.arange(ecg.size) / fs

winsize=fs*5
winhop=fs
i=0


def heartRate(firstPeak):
    elemanSayisi=len(firstPeak)
    i=0
    sum=0
    while i<elemanSayisi-1:
        sum=sum+((125/(firstPeak[i+1]-firstPeak[i]))*60)
        i=i+1
    print("Heart Rate:",str(sum/elemanSayisi-1))
    

def pwa(firstPeak,peaks2):
    i=0
    toplam=0
    control=len(ecg[firstPeak])
    while i<control:
        toplam=toplam+ecg[firstPeak][i]-ecg[peaks2][i]
        i=i+1
    print("PWA:",str(toplam/control))
    
    
def dp(firstPeak,peaks2):
    control=len(ecg[firstPeak])
    i=0
    toplam=0
    count=0
    while i<control-1:
        if (peaks2[i+1]-firstPeak[i]) <0:
            i=i+1
            count=count+1
        else:
            toplam=toplam+(peaks2[i+1]-firstPeak[i])
            i=i+1
    print("DP:", str(toplam/control-1))


def pwd(peaks2):
    elemanSayisi=len(peaks2)
    i=0
    sum=0
    while i<elemanSayisi-1:
        sum=sum+(peaks2[i+1]-peaks2[i])
        i=i+1
    print("PWD:",str(sum/elemanSayisi-1))
    

def on_press(event):
    global i
    sys.stdout.flush()
    
    lower=i
    upper=i+winsize
    
    winhighlight=np.ones(len(ecg))*-3
    winhighlight[lower:upper]=4
    ax1.cla()
    ax1.plot(time, ecg, 'g')
    ax1.plot(time, winhighlight, 'r')
    ax1.plot(time[lower:upper], ecg[lower:upper], 'r')
    ax1.grid()
    ax1.set_title('Raw Signal')
    
    x = ecg[lower:upper]
    peaks, properties = find_peaks(x, prominence=[0.7])     
     
    ax2.cla()
    ax2.plot( x, 'r')
    ax2.plot(peaks, x[peaks], 'bx')
    ax2.grid()
    ax2.set_title('Sliding Window')
    
    peaks2, _ = find_peaks(-ecg, distance=55, height=-0.4)
    
    plt.plot(ecg)
    plt.plot(peaks2,ecg[peaks2],"o" , color="blue")
    plt.show()

    peaks3, _ = find_peaks(-ecg, distance=18, height=[-0.8,-0.6])
    plt.plot(ecg)
    plt.plot(peaks3,ecg[peaks3],"o" , color="orange")
    plt.show()

    peaks, _ = find_peaks(ecg, distance=10, height=0.556789)
    
    i=0
    arrayeAtama=0
    peakControl=[]
    sayi=len(peaks)
    while arrayeAtama<sayi:
        peakControl.append(peaks[arrayeAtama])
        arrayeAtama=arrayeAtama+1
    
    while i<sayi-2:
        if (peaks[i+2]-peaks[i]) <35:
            peakControl.remove(peaks[i+2])
        i=i+1 
    peaks = np.array(peakControl)
        
    numOfPeaks=len(peaks)
    i=0
    firstPeak=[]
    secondPeak=[]
    while i<numOfPeaks:
        if i % 2 == 0:
            firstPeak.append(peaks[i])
            i=i+1
            
        else :
            secondPeak.append(peaks[i])
            i=i+1

    
    plt.plot(ecg)
    plt.plot(firstPeak, ecg[firstPeak], "o", color = "purple")
    plt.show()
    
    plt.plot(ecg)
    plt.plot(secondPeak, ecg[secondPeak], "o", color = "green")
    plt.show()
    
    heartRate(firstPeak)
 
    pwd(peaks2)
    
    dp(firstPeak,peaks2)

    pwa(firstPeak,peaks2)


    if event.key == 'right':
        i=i+winhop
        fig.canvas.draw()
    elif event.key == 'left':
        i=i-winhop
        fig.canvas.draw()


fig=plt.figure()

ax1 = fig.add_subplot(211)
ax1.plot(time, ecg, 'g')
ax1.grid()
ax1.set_title('Raw Signal')

ax2 = fig.add_subplot(212)
ax2.grid()

fig.canvas.mpl_connect('key_press_event', on_press)




