import socket
import sys
import os


def parse_data(data_arg):
    start = data_arg.find('username') + 9
    end = start
    for char in data_arg[start:]:
        if char == '&':
            break
        end += 1
    _username = data_arg[start: end]
    _password = data_arg[end + 10:]
    return _username, _password


def create_response(status, body):
    if status == 200:
        status_line = 'HTTP/1.1 200 OK\r\n'
    elif status == 404:
        status_line = 'HTTP/1.1 404 NOT FOUND\r\n'

    headers = 'Content-Type: text/html\r\n'
    headers += 'Accept: */*\r\n'
    headers += 'Connection: close\r\n\r\n'

    res_header = status_line + headers
    return res_header, body


def get_filename(req):
    filename = req.split(' ')[1]
    filename = filename.split('?')[0]
    filename = filename[1:]
    if filename == '':
        filename = 'index.html'

    return os.path.join(os.path.dirname(__file__), filename)


def read_file(filename):
    try:
        file_obj = open(filename, 'rb')
        data = file_obj.read()
        file_obj.close()
        response_code = 200

    except FileNotFoundError:
        print('File Not Found')
        response_code = 404
        data = ""

    return response_code, data


def main():
    port = 4000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen(5)

    cur_path = os.path.dirname(__file__)
    print('Server started on PORT', port)

    while True:
        try:
            client, address = server.accept()
            print('Client connected:', client)
            data = client.recv(1024)
            if not data:
                print('No data received')
                break
            print(data)
            req = data.decode()
            req_method = req.split(' ')[0]
            res_file = os.path.join(cur_path, 'index.html')
            res_status, data = read_file(res_file)

            if req_method == 'GET' or req_method == 'POST':
                if req_method == 'POST':
                    username, password = parse_data(req)
                    if username == 'admin' and password == 'admin':
                        res_file = os.path.join(cur_path, 'info.html')
                    else:
                        res_status = 404
                        res_file = os.path.join(cur_path, '404.html')

                elif req_method == 'GET':
                    file_name = get_filename(req)
                    if file_name.find('.html') == -1:
                        res_file = os.path.join(cur_path, file_name)

                file_obj = open(res_file, 'rb')
                data = file_obj.read()

                res_header, res_body = create_response(res_status, data)
                client.send(res_header.encode())
                client.send(res_body)
                client.close()

        except KeyboardInterrupt:
            server.close()
            sys.exit(0)


main()
