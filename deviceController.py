import zmq
from MasterId import HiyaMsg, DataMsg, InBuf, MasterId
from SetUpConnections import ClientSetup, ServerSetup
import secrets  # for creating a test id
import time


hostControllerAddr = '165.227.24.226'  # I am client to HostController
hostControllerPort = '5556'
deviceControllerPort = '5555' # I server to device

print("Device Controller Starting\n")

context = zmq.Context()   # get context
clientSetup = ClientSetup(context)  # instantiate the ClientSetup object
serverSetup = ServerSetup(context) # instantiate the ServerSetup object

# set up for one socket
"""
socket = serverSetup.createServerSocket() # get a server socket (using one socket)
serverSetup.serverBind('deviceControllerPort', socket) # bind to an address (using one socket)
clientSetup.clientConnect(deviceControllerAddr, deviceControllerPort, socket) # connect to server using one socket
"""

# set up for using server and client self.socket
"""
serverSetup.serverBind(deviceControllerPort) # bind to an address using seld.socket
clientSetup.clientConnect(deviceControllerAddr, deviceControllerPort) # connect to server using self.socket
"""

# set up separate server and client sockets
serverSocket = serverSetup.createServerSocket() # get a server socket
serverSetup.serverBind(deviceControllerPort, serverSocket) # bind to an address
clientSocket = clientSetup.createClientSocket() # get a client socket
clientSetup.clientConnect(hostControllerAddr, hostControllerPort, clientSocket) # connect to server using clientSocket

clientSetup.setIdentity(MasterId().getDevId()) # get the device id

poller = zmq.Poller()
poller.register(serverSocket, zmq.POLLIN)
poller.register(clientSocket, zmq.POLLIN)

print("send a message to HostController server")
dataToServer = "Hey there HostController Server".encode()
cmdToServer = "02".encode()
clientSocket.send_multipart([cmdToServer, dataToServer])
print("sent to server, cmd={}, data={}".format(cmdToServer, dataToServer))

print("beginning poll")
clientCount = 0
serverCount = 0
while 1:
    socks = dict(poller.poll(1000))
    if serverSocket in socks and socks[serverSocket] == zmq.POLLIN:
        ident, cmdFrmClient, data = serverSocket.recv_multipart()
        print("rcvd from client: ident=", ident, "cmd=", cmdFrmClient, "data=", data)
        dataToClient = ("Hello Client count={}".format(clientCount)).encode()
        clientCount += 1
        cmdToClient = "01".encode()
        print("type of ident=",type(ident))

        serverSocket.send_multipart([ident, cmdToClient, dataToClient])
        print ("sent to client, ident={}, cmd={}, data={}".format(ident, cmdToClient, dataToClient))

    if clientSocket in socks and socks[clientSocket] == zmq.POLLIN:
        cmdFrmServer, data = clientSocket.recv_multipart()
        print("rcvd from server: cmd=", cmdFrmServer, "data=", data)
        dataToServer = ("Hello Server count={}".format(serverCount)).encode()
        serverCount += 1
        cmdToServer = "02".encode()
        clientSocket.send_multipart([cmdToServer, dataToServer])
        print("sent to server, cmd={}, data={}".format(cmdToServer, dataToServer))

    time.sleep(1)
