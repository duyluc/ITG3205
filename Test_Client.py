import socket
import sys
import serial
import struct

#from numpy import roll

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ("192.168.0.95", 9999)
print('>> connecting to %s port %s' % server_address)
sock.connect(server_address)
Respondmes = "."

ser = serial.Serial()

try:
    xF = None
    yF = None
    zF = None
    ser.port = "COM1"
    ser.baudrate = 9600
    ser.timeout = 1
    if ser.is_open:
        print("COM1 IS BUSY!")
        sock.close()
        sys.exit()
    ser.open()
    while True:
        sock.sendall(Respondmes.encode('utf-8'))
        # Look for the response
        data = sock.recv(1024)
        print('>> received "%s"' % data.decode("utf-8"))
        receivedatasplit = data.decode('utf-8').split('$$')
        x = float(receivedatasplit[0])
        y = float(receivedatasplit[1])
        z = float(receivedatasplit[2])
        if(xF == None):
            xF = x
            yF = y
            zF = z
        else:
            # xF = 0.94 * xF + 0.06 * x
            # yF = 0.94 * yF + 0.06 * y
            #zF = 0.94 * zF + 0.06 * z
            #xF = x
            # yF = y
            zF = z

            xF = 0.94 * xF + 0.06 * x
            yF = 0.94 * yF + 0.06 * y

        senddata = str(xF) + "/" + str(yF) + "/" + str(zF) + "\n"
        ser.write(senddata.encode("ASCII"))
except Exception as e:
    print(str(e))

finally:
    print(sys.stderr, '>> closing socket')
    if ser.is_open:
        ser.close()
    sock.close()