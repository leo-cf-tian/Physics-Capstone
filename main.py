import gen
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
import cv2
import imutils
import math

file = input("File to encode: ")
blur = input("Blur? (Y/N): ").capitalize()
while not (blur == "Y" or blur == "N"):
    blur = input("Blur? (Y/N): ").capitalize()
blur = blur == "Y"

detect = input("Crop Background? (Y/N): ").capitalize()
while not (detect == "Y" or detect == "N"):
    detect = input("Crop Background? (Y/N): ").capitalize()
detect = detect == "Y"

if file.endswith((".jpg", ".png")):
    frame = cv2.imread(file)
    x, y = gen.encode(frame, blur, detect)

    repeat = 1000

    wavfile.write("output/sound_wave_x.wav", 44100, np.int16(x * 32767))
    wavfile.write("output/sound_wave_y.wav", 44100, np.int16(y * 32767))

    left_channel = AudioSegment.from_wav("output/sound_wave_x.wav") * repeat
    right_channel = AudioSegment.from_wav("output/sound_wave_y.wav") * repeat
    stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)
    stereo_sound.export("output/final_sound.wav", format="wav")

elif file.endswith((".mp4", ".avi")):
    
    cap = cv2.VideoCapture(file)
    
    num = gen.count_frames(cap)
    
    cap = cv2.VideoCapture(file)
    
    success,frame = cap.read()
    count = 0
    while success:
        if (count % 1 == 0):
    
            x, y = gen.encode(frame, blur, detect)
            
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
        
        progress = math.ceil(count / num * 20)
        print("Progress: |" + "█" * progress + " " * (20 - progress) + "| " + str(round(count / num * 100)) + "% (" + str(count) + "/" + str(num) + ")", end='\r')
        
    print("\nFinished Rendering!")
    stereo_sound.export("output/final_sound.wav", format="wav")