import socket
from EventLoop1 import EventLoop


class IO:
    def __init__(self) -> None:
        self.eventloop : EventLoop  = None
        self.objects = []

    def add_socket(
        self,
        sock,
        callback,
    ):
        iotype = None
        # check if sock is a socket
        if isinstance(sock, socket.socket):
            iotype = "socket"
            sock.setblocking(False)
            
        self.objects.append((sock, callback,iotype, False))

    def objs(self):
        return [obj[0] for obj in self.objects]

    def CanRead(self):
        return True

    def CanWrite(self):
        return True

    def Readable(self, readables):
        for obj, callback, iotype, status in self.objects:
            if obj in readables:
                if iotype == "socket":
                    self.HandleSocket(obj,callback,iotype,status)
    def HandleSocket(self, obj, callback, iotype, status):
        if not status:
            conn, addr = obj.accept()
            conn.setblocking(False)
            self.objects.append((conn, callback, iotype, True))
        else:
            data = obj.recv(1024)
            if not data:
                self.objects.remove((obj, callback, iotype, status))
            else:
                # callback(obj, data) 
                self.eventloop._queuecallback.append((callback,[obj,data]))
        
