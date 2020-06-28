import socket
import os

# Standard socket stuff:
host = 'localhost'
port = 3000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)

print("Server started on port", port)

filename = os.path.join(os.path.dirname(__file__), 'static/index.html')

while True:
    client_sock, client_address = sock.accept()
    print("Connection from: " + str(client_address))
    req = client_sock.recv(1024)  # get the request, 1kB max
    if not req:
        break

    f = open(filename, 'r')
    client_sock.sendall(str.encode("HTTP/1.0 200 OK\n"))
    client_sock.sendall(str.encode('Content-Type: text/html\n'))
    client_sock.send(str.encode('\r\n'))
    # send data per line
    for line in f.readlines():
        print('Sent ', repr(line))
        client_sock.sendall(str.encode(""+line+""))
        line = f.read(1024)
    f.close()
    client_sock.close()
