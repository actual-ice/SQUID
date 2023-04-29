#!/usr/bin/env python3
import serial



if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.reset_input_buffer()
    
    byte = b""
    biting = b""
    
    f = open("picture", "wb")
    number = 0

    while True:
        if ser.in_waiting > 0:
#            try:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if line == "start":
                while True:
                    biting = ser.readline()
                    byte = byte + biting 
                    print(biting)
                    if biting == b'boom':
                        break
                    number = number + 1
                    print(number)
                break
    f.write(byte) 
    f.close()
'''
            except:
            
                biting = ser.readline()
                byte = byte + biting 
                print(biting)
                if biting == b'boom':
                    break
                number = number + 1
                print(number)
                '''              

        
            
            