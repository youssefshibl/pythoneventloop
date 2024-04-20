import select



class EventLoop:
    def __init__(self) -> None:
        self._running = False
        self._io = []
        self._timeouts = []
        self._queuecallback = []

    def AddIo(self, io):
        io.eventloop = self
        self._io.append(io)

    def RunForever(self):
        self._running = True
        while self._running:
            # print("running")    
            try:
                readables, writables, _ = select.select(
                    [elem for io in self._io if io.CanRead() for elem in io.objs()],
                    [elem for io in self._io if io.CanWrite() for elem in io.objs()],
                    [],
                    0,
                )
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                self._running = False
                continue
            if readables:
                print(readables)
                for io in self._io:
                    io.Readable(readables)
            while self._queuecallback:
                callback ,argu = self._queuecallback.pop()
                callback(*argu)
