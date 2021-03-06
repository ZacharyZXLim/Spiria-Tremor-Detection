import serial
import queue

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import re

class UART_Handler(QObject):
    point_ready = pyqtSignal()
    
    class PutQueueThread(QThread):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            
        def run(self):
            while self.parent.stop != True:
                self.parent.queue.put(self.parent.get_point())
            self.parent.stop = False
            
    class GetQueueThread(QThread):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            
        def run(self):
            while self.parent.stop != True:
                self.parent.curr_point = self.parent.queue.get()
                self.parent.point_ready.emit()
            self.parent.stop = False
    
    def __init__(self, portname, baudrate):
        super().__init__()
        self.ser = serial.Serial(port=portname, baudrate=baudrate, timeout=1, write_timeout=1)
        self.queue = queue.Queue()
        
        self.curr_point = None
        self.stop = False
        
        self.put_queue_thread = self.PutQueueThread(self)
        self.get_queue_thread = self.GetQueueThread(self)

    def enable(self):
        self.ser.open()

    def disable(self):
        self.ser.close()

    def getData(self, num_bytes):
        data = self.ser.read(num_bytes)
        data = data.decode("utf-8")
        return data

    def sendData(self, data):
        data = bytes(data.encode("utf-8"))
        self.ser.write(data)

    def pairing(self):
        paired = False
        timeout = False
        
        while paired == False and timeout == False:
            self.sendData("spairing")
            
            data = None
            try:
                data = self.getData(8)
            except:
                pass
            
            if data == "":
                timeout = True

            if data == "pairdone":
                paired = True

        if paired == True:
            return True

        return False

    def get_point(self):
        data = self.getData(9)
        
        match = re.match(r"(\d{4}),(\d{4})", data)
        
        if match == None:
            match = re.match(r"(\d{0,4}),(\d{4})", data)
            
            try:
                data += self.getData(9 - (4 - len(match.group(1))) )
                match = re.search(r"(\d{4}),(\d{4})", data)
            except:
                return (-1, -1)

        data_x = int(match.group(1))
        data_y = int(match.group(2))
            
        return (data_x, data_y)
    
    def run_threads(self):
        print("threads running")
        self.put_queue_thread.start()
        self.get_queue_thread.start()
        
    def kill_threads(self):
        print("threads killed")
        self.stop = True