# from eventloop import EventLoop
from socket import create_server

# eventloop = EventLoop()
# server = create_server(("", 8081))


# def callback(conn, data):
#     print("-----------( 1 )----------")
#     print(data)
#     conn.sendall(data)
#     print("---------------------")


# eventloop.socket_server(server, callback)

# server2 = create_server(("", 8082))

# def callback2(conn, data):
#     print("-----------2----------")
#     print(data)
#     conn.sendall(data)
#     print("---------------------")

# eventloop.socket_server(server2, callback2)

# eventloop.run()


from EventLoop1 import EventLoop
from IO import IO


server = create_server(("", 8081))
server2 = create_server(("", 8082))
def callback1(conn, data):
    print("-----------2----------")
    print(data)
    conn.sendall(data)
    print("---------------------")

def callback2(conn, data):
    print("-----------1----------")
    print(data)
    conn.sendall(data)
    print("---------------------")
io = IO()
io.add_socket(server, callback1)
io.add_socket(server2, callback2)
eventloop = EventLoop()
eventloop.AddIo(io)


eventloop.RunForever()
