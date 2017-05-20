import pigpio
import time

pi = pigpio.pi()

e = 27
i1 = 17
i2 = 22

pi.set_mode(e, pigpio.OUTPUT)
pi.set_mode(i1, pigpio.OUTPUT)
pi.set_mode(i2, pigpio.OUTPUT)

pi.set_PWM_range(e, 100)

pi.write(i1, 1)
pi.write(i2, 0)

import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 9001              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    i = int(data.split('*')[1])
    if i < 0:
        i *= -1
        pi.write(i1, 0)
        pi.write(i2, 1)
    else:
        pi.write(i1, 1)
        pi.write(i2, 0)
    pi.set_PWM_dutycycle(e, i)
    
    if not data: break
    print i

conn.close()
