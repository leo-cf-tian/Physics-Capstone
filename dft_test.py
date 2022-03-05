"""
separation of real component and imaginary component for x and y values

"""

import math
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment

#implementation of the DFT algorithm from wikipedia
def DFT(x):
    N = len(x)
    X_final = [] # this is the final result, it gives the set of imaginary numbers

    for k in range (0,N):
        re = 0
        im = 0
        for n in range(0,N):
            phi = (math.pi*k*n) / N
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


test_points = [[0, 100], [0, 50], [0, 0], [100, 100], [100, 50], [100, 0], [50, 100], [50, 0]] #should be a square idk
test_points_x = [x[0] for x in test_points]
test_points_y = [x[1] for x in test_points]

wave_info_x = DFT(test_points_x)
wave_info_x = map_amplitude(wave_info_x)

wave_info_y = DFT(test_points_y)
wave_info_y = map_amplitude(wave_info_y)

sps = 44100

def generate_mono_sound(x):
    #samples per second
    
    T = 1/ sps
    #frequency scaling factor
    freq_base = 440.0 # i think this is A
    duration = 5.0 # this is in seconds
    N = sps * duration #sample size
    waveform_quiet = np.arange(N)*T
    for wave in x:
        sample_number = np.arange(N)*T
        omega = 2 * np.pi * freq_base * wave["freq"]
        phase = wave["phase"]
        waveform = np.sin(omega * sample_number + phase)
        waveform_quiet += waveform * wave["amplitude"]

    waveform_integers = np.int16(waveform_quiet * 32767)

    return waveform_integers



wavfile.write("sound_x.wav", sps, generate_mono_sound(wave_info_x))
wavfile.write("sound_y.wav", sps, generate_mono_sound(wave_info_y))

left_channel = AudioSegment.from_wav("sound_x.wav")
right_channel = AudioSegment.from_wav("sound_y.wav")

stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)

stereo_sound.export("final.wav", format="wav")