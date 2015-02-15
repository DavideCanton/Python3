from socket import create_connection

with create_connection(("www.google.it", 80)) as s:
    s.send("GET / HTTP/1.0\n\n".encode())
    while True:
        data = s.recv(1024)
        if not data:
            break
        string = data.decode()
        print(string)
