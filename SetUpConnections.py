import zmq
from Messages import HiyaMsg, DataMsg, MasterId
import secrets  # for creating a test id

class ClientSetup:
    def __init__(self, context):
        self.context = context   # Save the context to be used later

    def createClientSocket(self):
        socket = self.context.socket(zmq.DEALER)
        print("ClientSetup::createClientSocket() creating socket")
        return socket

    def clientConnect(self, addr, port, socket):
        serverAddr = "tcp://{}:{}".format(addr,port)
        socket.connect(serverAddr) # connect

    def setIdentity(self, id, socket):
        print ("ClientSetup::setIdentity identity=", id)
        socket.set(zmq.IDENTITY, id.encode())


class ServerSetup:
    def __init__(self, context):
        self.context = context

    def createServerSocket(self):
        socket = self.context.socket(zmq.ROUTER)
        print("ServerSetup::createServerSocket() creating socket")
        return socket

    def serverBind(self, port, socket):
        serverAddr = "tcp://*:{}".format(port)
        socket.bind(serverAddr)

    def setIdentity(self, id, socket):
        print ("ConnectToServer::setIdentity identity=", id)
        socket.set(zmq.IDENTITY, id.encode())

#        socket.identity = id.encode()
