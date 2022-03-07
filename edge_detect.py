import numpy as np
import cv2
import pyvirtualcam

# Gets coordinates of white pixels given an opencv image
def getCoords(img):
    return np.flip(np.column_stack(np.where(img == [255])), axis=1)

# Gets image and runs canny edge detection
image = cv2.imread('input/test.jpg', cv2.IMREAD_GRAYSCALE)
edges = cv2.Canny(image, 250, 300)

# Prints coordinates of white pixels
coord = getCoords(edges)
print(coord)

with open("drawing.js", 'a') as file:
    file.write("let drawing = [\n")
    for c in coord:    
        file.write("{" + "x: " + str(c[0] - 113.5) +", y: " + str(c[1] - 85) + "},\n")
    file.write("];")

# Display filtered image
cv2.imshow('image', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()