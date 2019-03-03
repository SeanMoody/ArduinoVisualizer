import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import struct
import pyaudio
from scipy.fftpack import fft

import sys
import time

import serial

import atexit


class AudioStream(object):
    def __init__(self):

        # pyqtgraph stuff
        pg.setConfigOptions(antialias=True)
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title='Spectrum Analyzer')
        self.win.setWindowTitle('Spectrum Analyzer')
        self.win.setGeometry(5, 115, 1910, 1070)

        wf_xlabels = [(0, '0'), (2048, '2048'), (4096, '4096')]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        wf_ylabels = [(0, '0'), (127, '128'), (255, '255')]
        wf_yaxis = pg.AxisItem(orientation='left')
        wf_yaxis.setTicks([wf_ylabels])

        sp_xlabels = [
            (np.log10(10), '10'), (np.log10(100), '100'),
            (np.log10(1000), '1000'), (np.log10(22050), '22050')
        ]
        sp_xaxis = pg.AxisItem(orientation='bottom')
        sp_xaxis.setTicks([sp_xlabels])

        self.waveform = self.win.addPlot(
            title='WAVEFORM', row=1, col=1, axisItems={'bottom': wf_xaxis, 'left': wf_yaxis},
        )
        self.spectrum = self.win.addPlot(
            title='SPECTRUM', row=2, col=1, axisItems={'bottom': sp_xaxis},
        )

        # pyaudio stuff
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2

        #logging stuff
        self.zero_one = 0
        self.one_two = 0
        self.two_three = 0
        self.three_four = 0
        self.four_five = 0
        self.five_six = 0
        self.six_seven = 0
        self.seven_eight = 0
        self.eight_nine = 0
        self.nine_ten = 0
        self.ten_eleven = 0
        self.eleven_twelve = 0
        self.twelve_thirteen = 0
        self.thirteen_fourteen = 0
        self.fourteen_fifteen = 0
        self.fifteen_sixteen = 0
        self.sixteen_seventeen = 0
        self.seventeen_eighteen = 0
        self.eighteen_nineteen = 0
        self.nineteen_twenty = 0
        self.twenty_twentyone = 0
        self.greater_than_twentyone = 0
        self.log_path = '/Users/seanmoody/Desktop/ArduinoLights/log.txt'
        

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
            #input_device_index = 
        )
        # waveform and spectrum x points
        self.x = np.arange(0, 2 * self.CHUNK, 2)
        self.f = np.linspace(0, self.RATE / 2, self.CHUNK / 2)

        #init serial    
        self.ser = serial.Serial('/dev/cu.usbmodem14401', 9600)

        

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setYRange(0, 255, padding=0)
                self.waveform.setXRange(0, 2 * self.CHUNK, padding=0.005)
            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen='m', width=3)
                self.spectrum.setLogMode(x=True, y=True)
                self.spectrum.setYRange(-4, 0, padding=0)
                self.spectrum.setXRange(
                    np.log10(20), np.log10(self.RATE / 2), padding=0.005)

    def update(self):
        wf_data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)
        wf_data = np.array(wf_data, dtype='b')[::2] + 128
        self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data,)

        sp_data = fft(np.array(wf_data, dtype='int8') - 128)
        sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]
                         ) * 2 / (128 * self.CHUNK)
        self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)

        #analyze frequency
        for q in range(0,5):
            sp_data[q] = 0
        
        maxFreq = int(round(np.argmax(sp_data) * (22050 / 1024)))
        print(maxFreq)

        if(maxFreq < 1000):
            self.ser.write(b'0')
            self.zero_one = self.zero_one + 1
        elif(maxFreq >= 1000 and maxFreq <= 2000):
            self.ser.write(b'1')
            self.one_two = self.one_two + 1
        elif(maxFreq >= 2000 and maxFreq <= 3000):
            self.ser.write(b'2')
            self.two_three = self.two_three + 1
        elif(maxFreq >= 3000 and maxFreq <= 4000):
            self.ser.write(b'3')
            self.three_four = self.three_four + 1
        elif(maxFreq >= 4000 and maxFreq <= 5000):
            self.ser.write(b'4')
            self.four_five = self.four_five + 1
        elif(maxFreq >= 5000 and maxFreq <= 6000):
            self.ser.write(b'5')
            self.five_six = self.five_six + 1
        elif(maxFreq >= 6000 and maxFreq <= 7000):
            self.ser.write(b'6')
            self.six_seven = self.six_seven + 1
        elif(maxFreq >= 7000 and maxFreq <= 8000):
            self.ser.write(b'7')
            self.seven_eight = self.seven_eight + 1
        elif(maxFreq >= 8000 and maxFreq <= 9000):
            self.ser.write(b'8')
            self.eight_nine = self.eight_nine + 1
        elif(maxFreq >= 9000 and maxFreq <= 10000):
            self.ser.write(b'9')
            self.nine_ten = self.nine_ten + 1
        elif(maxFreq >= 10000 and maxFreq <= 13000):
            self.ser.write(b':')
        elif(maxFreq >= 10000 and maxFreq <= 11000):
            self.ten_eleven = self.ten_eleven + 1
        elif(maxFreq >= 11000 and maxFreq <= 12000):
            self.eleven_twelve = self.eleven_twelve + 1
        elif(maxFreq >= 12000 and maxFreq <= 13000):
            self.twelve_thirteen = self.twelve_thirteen + 1
        elif(maxFreq >= 13000 and maxFreq <= 14000):
            self.thirteen_fourteen = self.thirteen_fourteen + 1
        elif(maxFreq >= 14000 and maxFreq <= 15000):
            self.fourteen_fifteen = self.fourteen_fifteen + 1
        elif(maxFreq >= 15000 and maxFreq <= 16000):
            self.fifteen_sixteen = self.fifteen_sixteen + 1
        elif(maxFreq >= 16000 and maxFreq <= 17000):
            self.sixteen_seventeen = self.sixteen_seventeen + 1
        elif(maxFreq >= 17000 and maxFreq <= 18000):
            self.seventeen_eighteen = self.seventeen_eighteen + 1
        elif(maxFreq >= 18000 and maxFreq <= 19000):
            self.eighteen_nineteen = self.eighteen_nineteen + 1
        elif(maxFreq >= 19000 and maxFreq <= 20000):
            self.nineteen_twenty = self.nineteen_twenty + 1
        elif(maxFreq >= 20000 and maxFreq <= 21000):
            self.twenty_twentyone = self.twenty_twentyone + 1
        elif(maxFreq > 21000):
            self.greater_than_twentyone = self.greater_than_twentyone + 1
        if(maxFreq > 13000):
            self.ser.write(b';')    

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()
    
    def fileout(self):
        self.outfile =  open(self.log_path, 'w+')
        self.outfile.write("%d \n" % self.zero_one)
        self.outfile.write("%d \n" % self.one_two)
        self.outfile.write("%d \n" % self.two_three)
        self.outfile.write("%d \n" % self.three_four)
        self.outfile.write("%d \n" % self.four_five)
        self.outfile.write("%d \n" % self.five_six)
        self.outfile.write("%d \n" % self.six_seven)
        self.outfile.write("%d \n" % self.seven_eight)
        self.outfile.write("%d \n" % self.eight_nine)
        self.outfile.write("%d \n" % self.nine_ten)
        self.outfile.write("%d \n" % self.ten_eleven)
        self.outfile.write("%d \n" % self.eleven_twelve)
        self.outfile.write("%d \n" % self.twelve_thirteen)
        self.outfile.write("%d \n" % self.thirteen_fourteen)
        self.outfile.write("%d \n" % self.fourteen_fifteen)
        self.outfile.write("%d \n" % self.fifteen_sixteen)
        self.outfile.write("%d \n" % self.sixteen_seventeen)
        self.outfile.write("%d \n" % self.seventeen_eighteen)
        self.outfile.write("%d \n" % self.eighteen_nineteen)
        self.outfile.write("%d \n" % self.nineteen_twenty)
        self.outfile.write("%d \n" % self.twenty_twentyone)
        self.outfile.write("%d \n" % self.greater_than_twentyone)

if __name__ == '__main__':

    audio_app = AudioStream()
    audio_app.animation()
    atexit.register(audio_app.fileout)