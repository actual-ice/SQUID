import bluetooth

bd_addr = "24:D7:EB:0F:05:B2"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
# print("running")
sock.connect((bd_addr, port))

# print("done")
''' 
while True:
    sock.send(input())
'''
datum = b''
data = b''
sock.send(input("what is your input: "))
'''while True:
    datum = sock.recv(2048)
    print(datum)
    if datum == b'\n':
        break
    data = data + datum
    
print(data)'''



sock.close()