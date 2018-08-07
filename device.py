import zmq
from MasterId import HiyaMsg, DataMsg, InBuf, MasterId
from SetUpConnections import ClientSetup, ServerSetup
import secrets  # for creating a test id

deviceControllerAddr = '192.168.1.7'
deviceControllerPort = '5555'
clientPort = ''

print("Device Starting\n")

context = zmq.Context()   # get context
clientSetup = ClientSetup(context)  # instantiate the ClientSetup object
#serverSetup = ServerSetup(context) # instantiate the ServerSetup object

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
#serverSocket = serverSetup.createServerSocket() # get a server socket
#serverSetup.serverBind(deviceControllerPort, serverSocket) # bind to an address
clientSocket = clientSetup.createClientSocket() # get a client socket
clientSetup.clientConnect(deviceControllerAddr, deviceControllerPort, clientSocket) # connect to server using clientSocket

clientSetup.setIdentity(MasterId().getDevId()) # get the device id

poller = zmq.Poller()
#poller.register(serverSocket, zmq.POLLIN)
poller.register(clientSocket, zmq.POLLIN)

print("beginning poll")
dataToServer = "Hello Server".encode()
cmdToServer = "02".encode()
clientSocket.send_multipart([cmdToServer, dataToServer])

clientCount = 0
while 1:
    socks = dict(poller.poll(1000))
    if clientSocket in socks and socks[clientSocket] == zmq.POLLIN:
        cmdFrmServer, data = clientSocket.recv_multipart()
        print("rcvd from server: cmd=", cmdFrmServer, "data=", data)
        dataToServer = ("Hello Server count={}".format(clientCount)).encode()
        clientCount += 1
        cmdToServer = "02".encode()
        clientSocket.send_multipart([cmdToServer, dataToServer])
        print("sent to server, cmd={}, data={}".format(cmdToServer, dataToServer))
