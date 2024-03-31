from eventloop import EventLoop
from socket import create_server

eventloop = EventLoop()
server = create_server(("", 8081))


def callback(conn,data):
    print("---------------------")
    print(data)
    print("---------------------")



eventloop.socket_server(server, callback)

eventloop.run()
