from time import sleep
import re;
import serial
import time

import numpy as np
import pylab as plt
import time

class TestGraph(object):
    def __init__(self):
        self.text_file = open("data.txt", "a")
        self.ser = serial.Serial('/dev/ttyACM2', 9600) # Establish the connection on a specific port
        self.x=0
        self.y=0 
        self.fig=plt.figure(1)
        self.ax=self.fig.add_subplot(111)
        self.ax.set_xlim(0,10)
        self.ax.set_ylim(0,1024)
        self.line,=self.ax.plot(self.x,self.y,'ko-')
        self.t_start =  time.time()

        self.currentx = 10;
        
    def start(self, x, y):
        self.x = np.concatenate((self.line.get_xdata(),[x]))
        self.y = np.concatenate((self.line.get_ydata(),[y]))
        self.line.set_data(self.x,self.y)
        plt.pause(.01)
        

    def recieve(self):
        while True:
            read = self.ser.readline()
            print read;

            read = self.parse(read)
            c_time = int (time.time()-self.t_start)
            if len(read) == 3:
                print read[1]
                self.update_x(c_time)
                self.text_file.write("%d,%d,%d\n" %(read[1], read[2], c_time))
                self.start(c_time, read[1])
            

    def parse(self, x):
        if x[0] == "-" and x[1] == "1":
            readings = [int(i) for i in x.split()]
            return readings
        else:
            return [0]
    def update_x(self, x):
        if x > self.currentx:
            self.ax.set_xlim(0,x+10)

a = TestGraph()
a.recieve();

