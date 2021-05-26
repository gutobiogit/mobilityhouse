from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import csv
import collections
import threading
import pika
import numpy as np
from datetime import datetime

class DynamicPlotter():

    def __init__(self, sampleinterval=0.1, timewindow=10., size=(600,350)):
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)*10000
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer2 = collections.deque([datetime.now().timestamp()]*self._bufsize, self._bufsize)
        self.databuffer3 = collections.deque([0.0]*self._bufsize, self._bufsize)
        #self.databuffer2.append()
        #self.databuffer4=[*self.databuffer2]
        #self.databuffer4.append(datetime.now().timestamp())

        self.y = np.zeros(self._bufsize, dtype=np.float)
        self.y_PV = np.zeros(self._bufsize, dtype=np.float)
        self.x = np.zeros(self._bufsize, dtype=np.float)
        #self.x[0]=datetime.now()
        #Magic table 
        self.PV_control={}
        with open('magic_table.csv', mode='r') as magic_table:
            data_var = csv.reader(magic_table)
            for data_read in data_var:
                self.PV_control[data_read[0][11:19]]=float(data_read[2])
    



        #self.pika_start()
        pika_start_thread = threading.Thread(target=self.pika_start)
        pika_start_thread.start()

        # PyQtGraph stuff
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
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='meter_data')
        channel.basic_consume(queue='meter_data', on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()

    def parse_magic(self,input_data):
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

    def callback(self,ch, method, properties, body):
        self.received_data=int(body)


    def getdata(self):
        new=[]
        time_now=datetime.now()
        new.append(self.received_data)
        new.append(time_now)
        new.append(self.parse_magic(str(time_now.time())[:8]))
        return new

    def updateplot(self):
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