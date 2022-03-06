"""
separation of real component and imaginary component for x and y values

"""

import math
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
import matplotlib.pyplot as plt

#implementation of the DFT algorithm from wikipedia
def DFT(x):
    N = len(x)
    X_final = [] # this is the final result, it gives the set of imaginary numbers
    for k in range (0,N):
        re = 0
        im = 0
        for n in range(0,N):
            phi = (2*math.pi*k*n) / N
            re += x[n] * math.cos(phi)
            im -= x[n] * math.sin(phi)
        re = re / N
        im = im / N

        freq = k; #k according to formula idk why
        amplitude = math.sqrt(re * re + im * im); #modulus of the imaginary number
        phase = math.atan2(im, re); #angle of the imaginary number with the positive real axis

        X_final.append({"re":re, "im":im, "freq":freq, "amplitude":amplitude, "phase":phase}) 
    return X_final

def map_amplitude(x):
    previ = -1
    for i in x:
        if i["amplitude"] > previ:
            previ = i["amplitude"]
    for i in x:
        i["amplitude"] = i["amplitude"]/previ
    return x


test_points = [[0, 100], [0, 0], [100, 100],  [100, 0], [0,50], [50,0], [100,50], [50,100]] #should be a square idk
test_points.sort()
test_points_x = [x[0] for x in test_points]
test_points_y = [x[1] for x in test_points]

"""
triangle_points_x = [i for i in range(0,100)]
triangle_points_y = [1 for i in range(0,100)]
trianglex = DFT(triangle_points_x)
trianglex = map_amplitude(trianglex)
triangley = DFT(triangle_points_y)
triangley = map_amplitude(triangley)
"""

wave_info_x = DFT(test_points_x)
wave_info_x.sort(key=lambda x:x["amplitude"])
wave_info_x = map_amplitude(wave_info_x)

wave_info_y = DFT(test_points_y)
wave_info_y.sort(key=lambda x:x["amplitude"])
wave_info_y = map_amplitude(wave_info_y)



sps = 44100

def generate_mono_sound(x, isx = True):
    #samples per second
    T = 1/ sps
    #frequency scaling factor
    freq_base = 440 # i think this is A
    duration = 5.0 # this is in seconds
    N = sps * duration #sample size
    waveform_quiet = np.empty(int(N))
    for wave in x:
        sample_number = np.arange(N)*T
        omega = 2 * np.pi * freq_base * wave["freq"]
        phase = wave["phase"]
        if (isx):
            waveform = np.sin(omega * sample_number + phase )
        else:
            waveform = np.cos(omega * sample_number + phase )
        waveform_quiet += waveform * wave["amplitude"]

    #waveform_integers = np.int16(waveform_quiet * 32767)
    plt.scatter(np.arange(N)*T, waveform_quiet)
    plt.show()
    return waveform_quiet


#generate_mono_sound([{"freq":1.0,"phase":0,"amplitude":1},{"freq":2.0,"phase":0,"amplitude":1}])
#wavfile.write("test.wav", sps, generate_mono_sound([{"freq":1.0,"phase":0,"amplitude":1}]))
x = generate_mono_sound(wave_info_x)
y = generate_mono_sound(wave_info_y, False)
#x = generate_mono_sound(triangley)
#y = generate_mono_sound(trianglex, False)

wavfile.write("sound_x.wav", sps, x)
wavfile.write("sound_y.wav", sps, y)
#wavfile.write("triangle.wav", sps, generate_mono_sound(triangle))

plt.scatter(x, y)
plt.show()

left_channel = AudioSegment.from_wav("sound_x.wav")
right_channel = AudioSegment.from_wav("sound_y.wav")
stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)
stereo_sound.export("final.wav", format="wav")
