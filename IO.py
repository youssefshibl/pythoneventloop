import socket
from EventLoop1 import EventLoop


class IO:
    def __init__(self) -> None:
        self.eventloop: EventLoop = None
        self.objects = {}

    def add_socket(
        self,
        sock,
        callback,
    ):
        # check if sock is a socket
        if isinstance(sock, socket.socket):
            sock.setblocking(False)
            key = sock.fileno()
            self.objects[key] = (sock, self.HandleSocketConnection, callback)

    def objs(self):
        # return list(self.objects.values())
        return self.objects

    def HandleSocketConnection(self, obj, callback):
        conn, addr = obj.accept()
        conn.setblocking(False)
        key = conn.fileno()
        self.objects[key] = (conn, self.HandleSocketData, callback)

    def HandleSocketData(self, obj, callback):
        data = obj.recv(1024)
        if data:
            callback(obj, data)

    def Add_file(self, file, callback):
        key = file.fileno()
        self.objects[key] = (file, self.HandleFile, callback)

    def HandleFile(self, obj, callback):
        data = obj.read(1024)
        if data:
            callback(obj, data)
        else:
            del self.objects[obj.fileno()]
            obj.close()
