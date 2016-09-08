#
# functions to process smoothing

import matplotlib.pyplot as plt
import numpy as np


def smoothingWindowUM2PX(smoothingWindowUM, voxelWidth):
    #calculate smoothing window in PX from smoothing window in UM, should be odd number

    smoothingWindowPX = int(smoothingWindowUM/voxelWidth)
    if int(smoothingWindowUM/voxelWidth) % 2 == 0:
        return smoothingWindowPX+1
    else:
        return smoothingWindowPX


def smoothFunc(x,window_length):
    # experimental function testing various parameters
    # returns the same lengths as in input len(x) = len(smoothened), tested for option # 3.

    # 1.Savitsky Golay filter (requires import scipy.signal)
    # smoothened = signal.savgol_filter(x,window_length,polyorder=3)

    # 2.Moving Average
    # smoothened = movingaverage(x, window_length)

    # 3.Convolution of a scaled window with the signal
    smoothened = smooth(x,window_length,window='hanning')

    return smoothened

def plotSmoothedProfile(profile, smoothingWindowPlotUM=100, AreaLabel="", show=True):
    #plotting the 2D profile graph

    voxelWidth = profile.voxelWidth[0]

    #smoothedProfile = np.zeros(int(smoothingWindowPlotPX/voxelWidth) - 1).tolist() + movingaverage(profile.intensity,int(smoothingWindowPlotPX/voxelWidth)).tolist()
    #smoothedProfile = smooth(profile.intensity, window_len=smoothingWindowPlotPX)

    smoothingWindowPlotPX = smoothingWindowUM2PX(smoothingWindowPlotUM, voxelWidth)
    smoothedProfile = smoothFunc(profile.intensity,smoothingWindowPlotPX)


    ploplo = plt.figure(1)
    if show:
        plt.plot(profile.distance, smoothedProfile, label=str(binNumber)+AreaLabel)
    #ploplo(title="bin Intensity Profile")
    #nplt = plt.plot(profile.intensity)
    plt.legend()

    #ploplo.legend()
    ploplo.set_size_inches(22, 11)

    return smoothedProfile

def movingaverage(values, window=10):
    #use moving averages for better smoothening the profile data
    # returns the same length as initial input

    weights = np.repeat(1.0, window) / window
    sma = np.convolve(values, weights, 'valid')

    startsma = np.zeros(window-1)
    sma = startsma.tolist() + sma.tolist()

    return sma

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.

    From https://scipy-cookbook.readthedocs.io/items/SignalSmooth.html

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """
    if (window_len % 2 != 0):
            window_len = window_len+1
    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')

    # not corrected for the size output
    #return y

    #corrected for the size output
    return y[(window_len/2-1):-(window_len/2)]


