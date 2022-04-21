from http import server
from i2c_itg3205 import *
import sys
import socket
import time
from i2c_adxl345 import *
from timeit import default_timer as timer



#Methods

def Main():
    #Property
    ReceiveDataBudder = 2
    #init IP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind the socket to the port
    server_address = ("192.168.0.95",9999)
    print('--> starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    _itg = i2c_itg3205(1)
    #_adx = i2c_adxl345(1)
    starttimer = 0
    try:
        while True:
            x = 0
            y = 0
            z = 0
            xA = 0
            yA = 0
            zA = 0
            # Wait for a connection
            print('--> waiting for a connection')
            connection, client_address = sock.accept()
            print('--> connection from', client_address)
            # Receive the data in small chunks and retransmit it
            try:
                #cal error
                xE = 0
                yE = 0
                zE = 0

                for i in range(0,20):
                    (_x,_y,_z) = _itg.getDegPerSecAxes()
                    if i == 0:
                        xE = _x
                        yE = _y
                        zE = _z
                    else:
                        xE = (xE + _x)/2
                        yE = (yE + _y)/2
                        zE = (zE + _z)/2
                    time.sleep(0.1)


                prtime = timer()
                starttimer = timer()
                while True:
                    data = connection.recv(ReceiveDataBudder)
                    if data:
                        (x,y,z) = _itg.getDegPerSecAxes()
                        #(x,y,yaw) = _adx.RollPitch()
                        now = timer()
                        deltime = timer() - prtime
                        prtime = now
                        # xA += (x - xE)*deltime
                        # yA += (y - yE)*deltime
                        xA = x
                        yA = y
                        zA += (z - zE)*deltime
                        if(timer() - starttimer < 0.05):
                            xA = 0
                            yA = 0
                            zA = 0                           
                        #data = str(x) + "$$" + str(y) + "$$" + str(z)
                        data = str(xA) + "$$" + str(yA) + "$$" + str(zA)
                        connection.sendall(data.encode('utf-8'))
                    else:
                        print('--> no more data from', client_address)
                        connection.close()
                        break
            except Exception as e:
                connection.close()
                break
                    
    finally:
        print("Over!!!")

if __name__ == "__main__":
    Main()