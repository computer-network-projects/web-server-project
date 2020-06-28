import socket
import os
from _thread import start_new_thread

clients = {}
addresses = {}

BUFFER_SIZE = 1024
host = 'localhost'
port = 3000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
print("Server started on port", port)
cur_status = ''


def parse_data(data_arg):
    start = data_arg.find('username') + 9
    end = start
    for char in data_arg[start:]:
        if char == '&':
            break
        end += 1

    _username = data_arg[start: end]
    _password = data_arg[end + 10:]
    return [_username, _password]


def client_thread(client_sock):
    data = client_sock.recv(1024)
    if not data:
        client_sock.close()
        return

    clients[client_sock] = len(clients)

    data = data.decode('utf-8')
    method = data[0]

    if method == 'P':
        username, password = parse_data(data)

        if username != 'admin' and password != 'admin':
            print("404")
            cur_status = '404'
        elif username == 'admin' and password == 'admin':
            print("SUCCESS")
            cur_status = 'success'

    elif method == 'G':
        cur_status = ''

    file = 'static/index.html'
    if cur_status == '404':
        file = 'static/notFound.html'
        cur_status = ''
    elif cur_status == 'success':
        file = 'static/info.html'
        cur_status = ''

    filename = os.path.join(os.path.dirname(__file__), file)
    client_sock.sendall(str.encode("HTTP/1.1 200 OK\n"))
    client_sock.sendall(str.encode('Connection: keep-alive\n'))
    client_sock.sendall(str.encode('Content-Type: text/html\n'))
    client_sock.sendall(str.encode('\r\n'))
    f = open(filename, 'r')
    client_sock.sendall(str.encode(f.read()))
    f.close()


while True:
    client, client_address = server.accept()
    addresses[client] = client_address
    print("Connection from: " + str(client_address))
    start_new_thread(client_thread, (client, ))


