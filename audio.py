"""
main file for recording audio input, data parsing
via an FFT, and rellocating peak values
"""

import numpy as np
from matplotlib import pyplot as plt 
import pyaudio
import serial
import time

# pyaudio constants
FORMAT = pyaudio.paInt16
CHUNK = 1024    # number of samples taken
DEVICE_NAME = 'VB-Cable'

# Arduino Port Constants
PORT = '/dev/cu.usbmodem14101'
BAUD_RATE = 19200

# audio visualizer constants
BIN_COUNT = 8

def main():
    # instantiate pyaudio module
    p = pyaudio.PyAudio()

    # instantiate serial connection to arduino
    #connection = serial.Serial(PORT, BAUD_RATE)
    #print('\nport used:', connection, '\n')

    # select relevant params matching specified DEVICE_NAME
    device_index = None
    max_channels = None
    default_rate = None
    for index in range(p.get_device_count()):
        device = p.get_device_info_by_index(index)
        if device.get('name') == DEVICE_NAME:
            device_index = device.get('index')
            max_channels = device.get('maxInputChannels')
            default_rate = int(device.get('defaultSampleRate'))

    # if device found matching DEVICE_NAME
    if device_index is not None:
        # instantiate audio stream
        stream = p.open(
            format = FORMAT,
            channels = max_channels,
            rate = default_rate,
            input = True,
            input_device_index = device_index
        )

        # start stream
        stream.start_stream()

        stop = False
        while(not stop):
            try:
                # convert audio bytes into 16 bit int values
                raw_data = stream.read(CHUNK, exception_on_overflow = False)
                audio_data = np.frombuffer(buffer = raw_data, dtype = np.int16)
                transform_data = np.absolute(np.fft.fft(audio_data))
                
                # convert frequency peaks to audio bins 
                # use only first half of data to ignore negative values
                # and ignoring first bin full of DC gain
                bins = [0] * BIN_COUNT   # reset bins
                for i in range(1,(int(CHUNK/2))): 
                    if (i <= 2):
                        bins[0] += transform_data[i]
                    elif (i>2 and i<=4):
                        bins[1] += transform_data[i]
                    elif (i>4 and i<=8):
                        bins[2] += transform_data[i]
                    elif (i>8 and i<=17):
                        bins[3] += transform_data[i]
                    elif (i>17 and i<=33):
                        bins[4] += transform_data[i]
                    elif (i>33 and i<=66):
                        bins[5] += transform_data[i]
                    elif (i>66 and i<=132):
                        bins[6] += transform_data[i]
                    elif (i > 132):
                        bins[7] += transform_data[i]
                
                # send bin values to arduino
                #for pos in range(BIN_COUNT):
                #    connection.write(bytes([int(bins[pos]/100000)]))

                #display bins in numpy
                x_axis = np.arange(0,len(bins))
                plt.bar(x_axis,bins)
                x1,x2,_,_ = plt.axis()  
                plt.axis((x1,x2,0,10_000_000))
                plt.pause(.01)
                plt.close()

                time.sleep(.01)

            except KeyboardInterrupt:
                stop = True
        

        # end pyudio stream & connection
        stream.stop_stream()
        stream.close()
        p.terminate()

        # end serial connection
        #connection.close()


if __name__ == '__main__':
    main()
