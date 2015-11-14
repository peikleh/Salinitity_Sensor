from time import sleep
import serial
import time

import numpy as np
import pylab as plt
import time

class TestGraph(object):
    def __init__(self):
        ser = serial.Serial('/dev/ttyACM1', 9600) # Establish the connection on a specific port
        self.text_file = open("data.txt", "a")
        self.x=0
        self.y=0 
        self.fig=plt.figure(1)
        self.ax=self.fig.add_subplot(111)
        self.ax.set_xlim(0,5)
        self.ax.set_ylim(0,30)
        self.line,=self.ax.plot(self.x,self.y,'ko-')
        self.start = (float) time.time()
        
    def start(self, x, y):
        self.x = np.concatenate((self.line.get_xdata(),[x]))
        self.y = np.concatenate((self.line.get_ydata(),[y]))
        self.line.set_data(self.x,self.y)
        plt.pause(.01)
        

    def recieve(self):
        while True:
            input = ser.readline()
            time = time.time()-self.start
            self.text_file.write(input +', ' + time)
            self.start(time, (int) input);

    def convert(self):
        #need convert for accurate plotting
        i = o;

    def update_x:
        #to update the x axis of the graph if need be
        i=0

a = TestGraph()

