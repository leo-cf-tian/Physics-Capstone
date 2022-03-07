# import necessary packages
import os
import cv2
import numpy as np
import mediapipe as mp

# initialize mediapipe
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(
    model_selection=1)

frame = cv2.imread('input/test.jpg')
bg_image = cv2.imread('input/white.jpg')
height, width, channel = frame.shape

RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# get the result
results = selfie_segmentation.process(RGB)
# extract segmented mask
mask = results.segmentation_mask

# it returns true or false where the condition applies in the mask
# it returns true or false where the condition applies in the mask
condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5
# resize the background image to the same size of the original frame
bg_image = cv2.resize(bg_image, (width, height))

# combine frame and background image using the condition
output_image = np.where(condition, frame, bg_image)

edges = cv2.Canny(output_image, 125, 175)

# Prints coordinates of white pixels
coord = np.flip(np.column_stack(np.where(edges == [255])), axis=1)

with open("gen.csv", 'a') as file:
    for c in coord:    
        file.write(str(c[0] - 113.5) +", " + str(c[1] - 85) + "\n")

cv2.imshow("Frame", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
