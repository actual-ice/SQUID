# from sim800l import SIM800L
# 
# 
# sim800l=SIM800L('/dev/serial0')
# # 
# sms="Hello there"
# #sim800l.send_sms(dest.no,sms)
# sim800l.send_sms('+639273235505',sms)

# def print_delete():
#      #assuming the sim has no sms initially
#     print(sim800l.get_msgid())
#     sms=sim800l.read_sms(sim800l.get_msgid())
#     print(sms)
#     sim800l.delete_sms(sim800l.get_msgid())
#   
# sim800l.callback_msg(print_delete)
#  
# while True:
#     sim800l.check_incoming()



# sim800l.send_sms('+639273235505',sms)

import serial
import time

ser = serial.Serial('/dev/serial0')

def SIM800(command):
    AT_command = command + "\r\n"
    ser.write(str(AT_command).encode('ascii'))
    time.sleep(1)
    if ser.inWaiting() > 0:
        echo = ser.readline() #waste the echo
        response_byte = ser.readline()
        response_str = response_byte.decode('ascii')
        return (response_str)
    else:
        return ("ERROR")
    
ser.write('AT+CMGS="+33612345678"\r\n'.encode('ascii'))
print(SIM800("testingg\x1A\r\n"))
