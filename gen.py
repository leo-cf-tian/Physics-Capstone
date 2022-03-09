import cv2
import numpy as np
import mediapipe as mp
from sklearn.neighbors import NearestNeighbors
import networkx as nx


"""
Function returning list of pixel positions of the edge of an image
This list is ordered to form a path
"""


def get_edges(frame):
    # initialize mediapipe
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(
        model_selection=1)
    
    height, width, channel = frame.shape
    frame = cv2.resize(frame, [200, int(200/width*height)])
    height, width, channel = frame.shape

    # bg_image = cv2.imread('input/white.jpg')

    # RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # # get the result
    # results = selfie_segmentation.process(RGB)
    # # extract segmented mask
    # mask = results.segmentation_mask

    # # it returns true or false where the condition applies in the mask
    # # it returns true or false where the condition applies in the mask
    # condition = np.stack((mask,) * 3, axis=-1) > 0.5
    # # resize the background image to the same size of the original frame
    # bg_image = cv2.resize(bg_image, (width, height))

    # # combine frame and background image using the condition
    # output_image = np.where(condition, frame, bg_image)

    # edges = cv2.Canny(cv2.GaussianBlur(frame, [0, 0], 1, 1), 100, 150)
    edges = cv2.Canny(frame, 100, 150)

    # Prints coordinates of white pixels
    y, x = np.where(edges == [255])

    points = np.c_[x, y]

    if len(points) > 16:
        clf = NearestNeighbors(n_neighbors=15).fit(points)
        G = clf.kneighbors_graph()

        T = nx.from_scipy_sparse_array(G)

        order = list(nx.dfs_preorder_nodes(T, 0))

        xx = x[order] - width / 2
        yy = height / 2 - y[order]

        coord = np.column_stack([xx, yy])

        return coord

    return []

"""
Inverse Fourier Transform
"""


def ifft(data_list):
    if len(data_list) > 0:
        data_list = [list(map(float, lst)) for lst in data_list]

        # print(data_list)

        data_list_x = [x[0] for x in data_list]
        data_list_y = [x[1] for x in data_list]

        duration = 0.016777
        data_length = len(data_list_x)
        if int(44100 * duration) > data_length:
            N = int(44100 * duration)
        else:
            N = data_length
        
        NN2 = int(data_length/2)

        fft_x = np.fft.fft(data_list_x) / data_length
        fft_y = np.fft.fft(data_list_y) / data_length

        X0 = np.append(fft_x[range(NN2)], np.zeros([N-data_length], dtype=complex))
        X = np.append(X0, fft_x[range(NN2, data_length)])

        Y0 = np.append(fft_y[range(NN2)], np.zeros([N-data_length], dtype=complex))
        Y = np.append(Y0, fft_y[range(NN2, data_length)])

        x = np.real(N*np.fft.ifft(X))  # real values taken for plotting
        y = np.real(N*np.fft.ifft(Y))

        x = map_amplitude(x)
        y = map_amplitude(y)

        return x, y
    return [0], [0]

"""
Amplitude Mapper
"""


def map_amplitude(x):
    previ = 0
    for i in x:
        if np.abs(i) > np.abs(previ):
            previ = i
    x = x/np.abs(previ)
    return x

def encode(frame):
    return ifft(get_edges(frame))