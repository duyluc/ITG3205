from http import server
from i2c_itg3205 import *
import sys
import socket
import time



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

    while True:
        # Wait for a connection
        print('--> waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('--> connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(ReceiveDataBudder)
                if data:
                    (x,y,z) = _itg.getDegPerSecAxes()
                    data = str(x) + "$$" + str(y) + "$$" + str(z)
                    connection.sendall(data.encode('utf-8'))
                    time.sleep(0.05)
                else:
                    print('--> no more data from', client_address)
                    break
                
        finally:
            connection.close()
            print("Over!!!")
            break

if __name__ == "__main__":
    Main()