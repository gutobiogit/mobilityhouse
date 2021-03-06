from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import csv
import collections
import threading
import pika
import numpy as np
from datetime import datetime

class DynamicPlotter():
    '''
    class DynamicPlotter
    
    Methods:
    
    pika_start() --> Connect to the broker,set all data for connection and link the 
    callback method named "callback()"
    
    parse_magic(::datetimestamp) --> Receive datetimestamp::datetimestamp format and transform to a hh:mm:ss::string
     format then set the closest time in the magic table(15min)
    
    callback(ch, method, properties, body)) --> ch,method,properties, using only one 
    channel in this project theres no need for this parameters, in body::binary is our data transmitted from broker.
    
    getdata() -->  Load data transmitted, set time now::datetimenow(for the x axis in the graphic) and get parse_magic result::string 
    
    updateplot() --> First add data from getdata() to plot x(time),y(data) from both curves and add to file "Data_recorded.csv" 
    (::timestamp , meter power value,::int(from 0 to 9000), PV power value::float(magic table value), and sum of both)
    
    run() --> Singleton, starts execution
    
    '''
    def __init__(self, sampleinterval=0.1, timewindow=10., size=(600,350)):
        #Set lists 
        self._interval = int(sampleinterval*1000)
        #Buffer size is how much data it can store. The graph will show only this much of data
        self._bufsize = int(timewindow/sampleinterval)*10000
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        #set first point in the graph, if set to 0 data will begin at 1/1/1970(0 unixtime)
        self.databuffer2 = collections.deque([datetime.now().timestamp()]*self._bufsize, self._bufsize)
        self.databuffer3 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=np.float)
        self.y_PV = np.zeros(self._bufsize, dtype=np.float)
        self.x = np.zeros(self._bufsize, dtype=np.float)
        #Magic table load to memory as dict
        self.PV_control={}
        with open('magic_table.csv', mode='r') as magic_table:
            data_var = csv.reader(magic_table)
            for data_read in data_var:
                self.PV_control[data_read[0][11:19]]=float(data_read[2])
        #Start pika as thread, non-blocking
        pika_start_thread = threading.Thread(target=self.pika_start)
        pika_start_thread.start()
        # PyQtGraph start, setup, set positions, labels and create 2 plot draws, pause for self._interval::integer
        self.app = QtGui.QApplication([])
        self.plt = pg.plot(title='PV Simulator Challenger')
        axis = pg.DateAxisItem()
        self.plt.setAxisItems({'bottom':axis})
        self.plt.plotItem.setMouseEnabled(y=False)
        self.plt.setBackground((255,255,255))
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', 'Power(kW)', '')
        self.plt.setLabel('bottom')
        self.curve = self.plt.plot(self.x, self.y, pen=(0,0,255),fillLevel=0, brush=(0,0,255,130))
        self.curve2 = self.plt.plot(self.x, self.y_PV, pen=(0,255,0),fillLevel=0, brush=(0,255,0,130))
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)
        self.received_data=0

    def pika_start(self):
        #pika connection set up and start up
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='meter_data')
        channel.basic_consume(queue='meter_data', on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()

    def parse_magic(self,input_data)->datetime:
        #parse time now to format hh:mm:ss and search dict
        if (int(input_data[3:5])%15) ==0:
            treat_data=input_data[:-2]+"00"
            if treat_data in self.PV_control:
                return (self.PV_control[treat_data])
            else:
                return 0
        else:
            x=int(input_data[3:5]) % 15 
            search=int(input_data[3:5])-x
            treat_data=f"{input_data[:2]}:{str(search).zfill(2)}:00"
            if treat_data in self.PV_control:
                return self.PV_control[str(treat_data)]
            else:
                return 0

    def callback(self,ch, method, properties, body)->str:
        #Just callback method 
        self.received_data=int(body)

    def getdata(self):
        #Get data to graph plot
        new=[]
        time_now=datetime.now()
        new.append(self.received_data)
        new.append(time_now)
        new.append(self.parse_magic(str(time_now.time())[:8]))
        return new

    def updateplot(self):
        #Plot graphis and save a csv data with timestamp,meter,PV, meter+PV
        get_data=self.getdata()
        self.databuffer.append( get_data[0] )
        self.y[:] = self.databuffer
        self.databuffer2.append(get_data[1].timestamp())
        self.x[:] = self.databuffer2
        self.databuffer3.append(get_data[2])
        self.y_PV[:] = self.databuffer3
        with open('Data_recorded.csv', mode='a') as data_recorder:
            data_var = csv.writer(data_recorder, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_var.writerow([datetime.now(), get_data[0] ,get_data[2], get_data[0]  + get_data[2]])
        self.curve.setData(self.x, self.y)
        self.curve2.setData(self.x, self.y_PV)
        self.received_data=0
        self.app.processEvents()

    def run(self):
        self.app.exec_()


if __name__ == '__main__':
    m = DynamicPlotter(sampleinterval=5, timewindow=10.)
    m.run()
