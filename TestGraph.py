from time import sleep
import re
import serial
import time
import numpy as np
import pylab as plt
import time

class TestGraph(object):
    def __init__(self):
       
        self.ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port
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
            try:
                while True:
                    read = self.ser.readline()
                    print read;
                    read = self.parse(read)
                    c_time = int (time.time()-self.t_start)

                    if len(read) == 3:
                        self.update_x(c_time)
                        with open("data.csv", "a") as f:
                            f.write('%d,%f,%f\n' %(read[1], time.time(), read[2]))
                        self.start(c_time, read[1])
                    elif len(read) == 2:
                        self.update_x(c_time)
                        with open("data.csv", "a") as f:
                            f.write('%d,%f\n' %(read[1], time.time()))
                        self.start(c_time, read[1])

            except KeyboardInterrupt:
                self.user_input()

    def parse(self, x):
        pattern = re.compile('[a-z]')
        if x[0] == "-" and x[1] == "1" and not pattern.search(x):
            readings = [float(i) for i in x.split()]
            if readings[2] == -1000.0 or readings[2] == 85.00:
                readings = [readings[0], readings[1]]

            return readings
        else:
            return [0]
            
    def update_x(self, x):
        if x > self.currentx:
            self.ax.set_xlim(0,x+10)

    def user_input(self):
        choice = input("Press 0 to use pump or 1 to toggle agitator")
        if choice == 0:
            self.ser.write("p")
            liters = input("How many liters would you like to pump?")
            
            self.ser.write(liters)
        elif choice == 1:
            self.ser.write("a")
        

a = TestGraph()
a.recieve();

