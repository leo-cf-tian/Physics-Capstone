import gen
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
import cv2

file = input("File to encode: ")

if file.endswith((".jpg", ".png")):
    frame = cv2.imread(file)
    x, y = gen.encode(frame)

    repeat = 1000

    wavfile.write("output/sound_wave_x.wav", 44100, np.int16(x * 32767))
    wavfile.write("output/sound_wave_y.wav", 44100, np.int16(y * 32767))

    left_channel = AudioSegment.from_wav("output/sound_wave_x.wav") * repeat
    right_channel = AudioSegment.from_wav("output/sound_wave_y.wav") * repeat
    stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)
    stereo_sound.export("output/final_sound.wav", format="wav")

elif file.endswith((".mp4")):
    
    cap = cv2.VideoCapture(file)
    success,frame = cap.read()
    count = 0
    while success:
        if (count % 1 == 0):
            x, y = gen.encode(frame)
            wavfile.write("output/sound_wave_x.wav", 44100, np.int16(x * 32767))
            wavfile.write("output/sound_wave_y.wav", 44100, np.int16(y * 32767))
            left_channel = AudioSegment.from_wav("output/sound_wave_x.wav") * 2
            right_channel = AudioSegment.from_wav("output/sound_wave_y.wav") * 2
            if count == 0:
                stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)
            else:
                stereo_sound += AudioSegment.from_mono_audiosegments(left_channel, right_channel)
        success,frame = cap.read()
        count += 1
    stereo_sound.export("output/final_sound.wav", format="wav")