import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
import pandas

df = pandas.read_csv('pi.csv') # data from Olli Niemitalo

xx = np.array(df['x'],dtype='int')
yy = np.array(df['y'],dtype='int')

xx = np.append(xx,xx[0]) # to complete figure
yy = np.append(yy,yy[0]) # to complete figure

NN = len(xx)
NN2 = int(NN/2)
N = 300 # must be greater than NN

XX = fft(xx)/NN
YY = fft(yy)/NN

X0 = np.append(XX[range(NN2)], np.zeros([N-NN],dtype=np.complex))
X  = np.append(X0, XX[range(NN2,NN)])

Y0 = np.append(YY[range(NN2)], np.zeros([N-NN],dtype=np.complex))
Y  = np.append(Y0, YY[range(NN2,NN)])

x = np.real(N*ifft(X)) # real values taken for plotting
y = np.real(N*ifft(Y))

fig1 = plt.figure(figsize=(16,6))
ax1 = fig1.add_subplot(131)
ax1.plot(xx, yy, 'mx')
ax1.plot(x, y, 'b')
ax1.set_title(f"FFT fit of $\pi$ figure - zero-padding: N ={N:3}")

xnn = np.linspace(0,NN,NN)
xn  = np.linspace(0,NN,N)

#
ax2 = fig1.add_subplot(132)
ax2.plot(xnn,xx, 'mx')
ax2.plot(xn, x, 'b')
ax2.set_title("FFT fit of x-coordinates")

#
ax3 = fig1.add_subplot(133)
ax3.plot(xnn,yy, 'mx')
ax3.plot(xn, y, 'b')
ax3.set_title("FFT fit of y-coordinates")