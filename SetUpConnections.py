import zmq
from MasterId import HiyaMsg, DataMsg, InBuf, MasterId
import secrets  # for creating a test id

class ClientSetup:
    def __init__(self, context):
        self.context = context
        self.socket = None

    def createClientSocket(self):
        self.socket = self.context.socket(zmq.DEALER)
        print("ClientSetup::createClientSocket() creating socket")
        return self.socket

    def clientConnect(self, addr, port, socket=None):
        serverAddr = "tcp://{}:{}".format(addr,port)
        print ('ClientSetup::connectToServer() serverAddr=', serverAddr)
        if socket == None:
            print("ClientSetup::clientConnect() socket parm is None")
            if self.socket == None: # if self.socket does not exist
                print("ClientSetup::clientConnect() self.socket is None ")
                print(" creating  self.socket")
                self.createClientSocket() # create a self.socket
            else:
                print ("ClientSetup::clientConnect() using self.socket")
                socket = self.socket # set socket parm to self.socket
        else:
            print ("ClientSetup::clientConnect() using socket parm")
            self.socket = socket # else set self.socket to socket parm
        assert self.socket != None
        self.socket.connect(serverAddr) # connect

    def setIdentity(self, id):
        print ("ClientSetup::setIdentity id=", id)
        self.socket.identity = id

    def getSocket(self):
        return self.socket

class ServerSetup:
    def __init__(self, context):
        self.context = context
        self.socket = None

    def createServerSocket(self):
        self.socket = self.context.socket(zmq.ROUTER)
        print("ServerSetup::createServerSocket() creating socket")
        return self.socket

    def serverBind(self, port, socket=None):
        serverAddr = "tcp://*:{}".format(port)
        print ('ServerSetup::serverBind() serverAddr=', serverAddr)
        if socket == None:
            print("ServerSetup::serverBind() socket parm is None")
            if self.socket == None:
                print("ServerSetup::serverBind() self.socket is None ")
                print(" creating  self.socket")
                self.createServerSocket()
            else:
                print ("ServerSetup::serverBind() using self.socket")
                socket = self.socket
        else:
            print ("ServerSetup::serverBind() using socket parm")
            self.socket = socket
        assert self.socket != None
        self.socket.bind(serverAddr)

    def setIdentity(self, id):
        print ("ConnectToServer::setIdentity id=", id)
        self.socket.identity = id.encode()

    def getSocket(self):
        return self.socket
