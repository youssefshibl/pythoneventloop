import select
class EventLoop:
    def __init__(self) -> None:
        self._running = False
        self._io = []
        self._timeouts = []
        self._queuecallback = []
        self.readables = {}
        self.writables = {}

    def AddIo(self, io):
        io.eventloop = self
        self._io.append(io)

    def RunForever(self):
        self._running = True
        while self._running:
            # print("running")
            # self.readables = self._io[0].objs()
            self.readables = {}
            for io in self._io:
                self.readables.update(io.objs())


            try:
                # block until there is something to read 
                # if there is nothing to read, it will block
                # to disable blocking, pass 0 as the last argument
                readables, writables, _ = select.select(
                    self.readables,
                    self.writables,
                    [],
                    None,
                )
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                self._running = False
                continue
            if readables:
                for readable in readables:
                    obj, callback, *args = self.readables[readable]
                    callback(obj, *args)
