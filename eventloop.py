import time
import select
import socket


class EventLoop:
    def __init__(self) -> None:
        self._running = False
        self._readers = []
        self._writers = []
        self._timeouts = []
        self.tempacceptcallback = None
        self.tempreadcallback = None

    def add_reader(self, fd, event, callback, *args):
        self._readers.append((fd, event, callback, *args))

    def add_writer(self, fd, event, callback, *args):
        self._writers.append((fd, event, callback, *args))

    def add_timeout(self, timeout, callback):
        current_time = time.time()
        self._timeouts.append((current_time, timeout, callback))

    def run(self):
        self._running = True
        while self._running:
            # print("checking for timeouts")
            for timer in self._timeouts:
                current_time = time.time()
                if current_time - timer[0] >= timer[1]:
                    timer[2]()
                    self._timeouts.remove(timer)
            # print("checking for IO")
            readables, writables, _ = select.select(
                [reader[0] for reader in self._readers],
                [writer[0] for writer in self._writers],
                [],
                0.05,
            )
            for reader in self._readers:
                source, event, callback, *args = reader
                if source in readables:
                    callback(source, *args)
            for writer in self._writers:
                source, event, callback, *args = writer
                if writer[0] in writables:
                    callable(source, *args)

    def socket_server(self, server, readcallback=None, acceptcallback=None):
        # add valiation to socket
        if not server:
            return
        if type(server) != socket.socket:
            return
        server.setblocking(False)
        self.tempreadcallback = readcallback
        self.tempacceptcallback = acceptcallback
        self.add_reader(server, select.POLLIN, self.on_accept)

    def on_accept(self, server):
        try:
            conn, addr = server.accept()
            print(f"accepted connection from {addr}")
            if self.tempacceptcallback:
                self.tempacceptcallback(conn, addr)
            conn.setblocking(False)
            self.add_reader(conn, select.POLLIN, self.on_read)
        except BlockingIOError:
            pass

    def on_read(self, conn):
        try:
            data = conn.recv(1024)
            if not data:
                print("closing connection")
                self._readers.remove((conn, select.POLLIN, self.on_read))
                conn.close()
            else:
                print(f"received data: {data}")
                if self.tempreadcallback:
                    self.tempreadcallback(conn, data)
        except BlockingIOError:
            pass
