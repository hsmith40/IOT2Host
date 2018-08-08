import zmq
from Messages import HiyaMsg, DataMsg, MasterId, Messages
from SetUpConnections import ClientSetup, ServerSetup
import time


#procControllerAddr = '165.227.24.226'  # I am client to HostController
#procControllerPort = '5557'
hostControllerPort = '5556' # I server to device

print("Host Controller Starting\n")

context = zmq.Context()   # get context
#clientSetup = ClientSetup(context)  # instantiate the ClientSetup object
serverSetup = ServerSetup(context) # instantiate the ServerSetup object


# set up separate server and client sockets
serverSocket = serverSetup.createServerSocket() # get a server socket
serverSetup.serverBind(hostControllerPort, serverSocket) # bind to an address

#clientSocket = clientSetup.createClientSocket() # get a client socket

# NOTE: setIdentity() MUST BE CALLED BEFORE clientConnect or the identity will
# not take effect
#clientSetup.setIdentity(MasterId().getDevId()) # get the device id
#clientSetup.clientConnect(hostControllerAddr, hostControllerPort, clientSocket) # connect to server using clientSocket


poller = zmq.Poller()
poller.register(serverSocket, zmq.POLLIN)
#poller.register(clientSocket, zmq.POLLIN)

serverCount = 0
messages = Messages()
print("Host Controller beginning poll")
while 1:
    socks = dict(poller.poll(1000))
    if serverSocket in socks and socks[serverSocket] == zmq.POLLIN:
        ident, cmdFrmClient, data = serverSocket.recv_multipart()
        print("Rcvd from DeviceController: ident=", ident, "cmd=", cmdFrmClient, "data=", data)

        inDict = messages.bufferToDict(data) # create a list from the message

        print("Internal list, devType={}, cmd={}, data={}, returnList={}\n"
            .format(inDict['devType'], inDict['cmd'], inDict['data'], inDict['returnList']))

        # For testing purposes, now send the message back down the line

        outIdent = messages.popLastReturnId(inDict).encode() # get the device controller id
        print("Ident poped from returnId", outIdent)
        dataToClient = messages.dictToBuffer(inDict).encode() # create a buffer
        print("Data to Device Controller=", dataToClient)
        cmdToClient = inDict['cmd'].encode()
        print("Cmd to Device Controller=", cmdToClient)
        print("Sending to outIdent =", outIdent)
        serverSocket.send_multipart([outIdent, cmdToClient, dataToClient])
