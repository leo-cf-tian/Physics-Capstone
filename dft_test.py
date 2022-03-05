"""
separation of real component and imaginary component for x and y values

"""

import math
import numpy as np
from scipy.io import wavfile

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

test_points = [[0, 100], [0, 50], [0, 0], [100, 100], [100, 50], [100, 0], [50, 100], [50, 0]] #should be a square idk
test_points_x = [x[0] for x in test_points]
test_points_y = [x[1] for x in test_points]

print(DFT(test_points_x))

#samples per second
sps = 44100

#frequency scaling factor
freq_base = 440.0 # i think this is A

duration = 5.0 # this is in seconds

sample_number = np.arrange(duration * sps)

waveform = np.sin(2 * np.pi * sample_number * freq_base / sps)

waveform_quiet = waveform * 0.3

waveform_integers = np.int16(waveform_quiet * 32767)

wavfile.write("soundlmao.wav", sps, waveform_integers)

