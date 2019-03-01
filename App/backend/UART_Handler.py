import serial
import time
import cv2
import numpy as np

class UART_Handler():
    def __init__(self, portname, baudrate):
        self.ser = serial.Serial(port=portname, baudrate=baudrate, timeout=5, write_timeout=5)

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
            
            print(data)
            
            if data == "":
                timeout = True

            if data == "pairdone":
                paired = True

            # time.sleep(0.001)

        if paired == True:
            return True

        return False

    def get_point(self):
        invalid = False
        data_x = int(self.getData(4))
        data_y = int(self.getData(4))

        if data_x == 1023 and data_y == 1023:
            invalid = True

        if invalid == False:
            return [data_x, data_y]

    def calibration(self, dest_geometry):
        self.calib_pts_src = np.array([])

        # obtain calibration points
        for i in range(0, 4):
            np.append(self.calib_pts_src, self.get_point())

        self.calib_pts_dest = np.array([[dest_geometry.left(), dest_geometry.top()],
                                        [dest_geometry.right(), dest_geometry.top()],
                                        [dest_geometry.right(), dest_geometry.bottom()],
                                        [dest_geometry.left(), dest_geometry.bottom()]])

        self.H = self.find_homography(self.calib_pts_src, self.calib_pts_dest)

    def find_homography(self, calib_pts_src, calib_pts_dest):
        self.H = cv2.getPerspectiveTransform(calib_pts_src, calib_pts_dest)

    def transform_coordinates(self, pts_src):
        pts_dest = np.matmul(pts_src, self.H)
        return pts_dest

            
if __name__ == "__main__":
    uart_handler = UART_Handler("/dev/ttyS0", 9600)
    # status = uart_handler.pairing()

    points = []

    while True:
        point = uart_handler.test_get_coordinates()