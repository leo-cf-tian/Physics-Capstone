import numpy as np
import cv2

# Gets coordinates of white pixels given an opencv image
def getCoords(img):
    return np.flip(np.column_stack(np.where(img == [255])), axis=1)

# Gets image and runs canny edge detection
image = cv2.imread('input/test.jpg', cv2.IMREAD_GRAYSCALE)
edges = cv2.Canny(image, 50, 150)

# Prints coordinates of white pixels
print(getCoords(edges))

# Display filtered image
cv2.imshow('image', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()


'''
Takes live camera feed and runs edge detection on it, displaying live results
'''
# cap = cv2.VideoCapture()
# cap.open(0, cv2.CAP_DSHOW)
# while(True):
#     ret, frame = cap.read()
#     edges = cv2.Canny(frame,50,150)
#     cv2.imshow('frame', edges)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()
