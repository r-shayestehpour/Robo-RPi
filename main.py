import pigpio
import time
import socket

pi = pigpio.pi()

################################# const

right_motor_en = 27
left_motor_en = 17

################################# init rpi gpio

pi.set_mode(right_motor_en, pigpio.OUTPUT)
pi.set_mode(left_motor_en, pigpio.OUTPUT)

pi.set_PWM_range(right_motor_en, 100)
pi.set_PWM_range(left_motor_en, 100)

################################# init server socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 9001              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr

################################# main program loop

STRAIGHT_OFFSET = 10
MAX_PWM_DUTYCYCLE = 100

while 1:
    data = conn.recv(1024)
    gyro_y = int(data.split('*')[1])
    if gyro_y < STRAIGHT_OFFSET and gyro_y > (STRAIGHT_OFFSET * -1):
        #robot should go straing, both motors same speed
        pi.set_PWM_dutycycle(right_motor_en, MAX_PWM_DUTYCYCLE)
        pi.set_PWM_dutycycle(left_motor_en, MAX_PWM_DUTYCYCLE)

    elif gyro_y < (STRAIGHT_OFFSET * -1):
        #robot should turn right, slow down right motor
        pi.set_PWM_dutycycle(left_motor_en, MAX_PWM_DUTYCYCLE)
        pi.set_PWM_dutycycle(right_motor_en, MAX_PWM_DUTYCYCLE + gyro_y)
    
    elif gyro_y > STRAIGHT_OFFSET:
        #robot should turn left, slow down left motor
        pi.set_PWM_dutycycle(right_motor_en, MAX_PWM_DUTYCYCLE)
        pi.set_PWM_dutycycle(left_motor_en, MAX_PWM_DUTYCYCLE - gyro_y)
    
    if not data: break
    print gyro_y

conn.close()
