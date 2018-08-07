# update - 8/7/2018 13:27 MST
import zmq
from MasterId import HiyaMsg, DataMsg, InBuf, MasterId
from SetUpConnections import ClientSetup, ServerSetup
import secrets  # for creating a test id

severAddr = '192.168.1.7'
serverPort = '5555'
clientPort = '5556'

print("Test Setup Connections Started\n")

context = zmq.Context()   # get context
clientSetup = ClientSetup(context)  # instantiate the ClientSetup object
serverSetup = ServerSetup(context) # instantiate the ServerSetup object

# set up for one socket
"""
socket = serverSetup.createServerSocket() # get a server socket (using one socket)
serverSetup.serverBind(serverPort, socket) # bind to an address (using one socket)
clientSetup.clientConnect(serverAddr, serverPort, socket) # connect to server using one socket
"""

# set up for using server and client self.socket
"""
serverSetup.serverBind(serverPort) # bind to an address using seld.socket
clientSetup.clientConnect(serverAddr, serverPort) # connect to server using self.socket
"""

# set up separate server and client sockets
serverSocket = serverSetup.createServerSocket() # get a server socket
serverSetup.serverBind(serverPort, serverSocket) # bind to an address
clientSocket = clientSetup.createClientSocket() # get a client socket
clientSetup.clientConnect(severAddr, serverPort, clientSocket) # connect to server using clientSocket

clientSetup.setIdentity(MasterId().getDevId()) # get the device id
