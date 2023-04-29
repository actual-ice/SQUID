# march 16 - this works

import bluetooth

bd_addr = "24:D7:EB:0F:05:B2"
# bd_addr = "DC:A9:56:8C:5B:0E" 

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
print("connection success")

sock.send("hello!!")
a = b''
datum = b''
while True:
    datum = sock.recv(1084)
    print(datum)
    if datum == b'\n':
        break
    a = a+datum
    
print(a)


sock.close()