import zmq
from Messages import HiyaMsg, DataMsg, Messages, MasterId
from SetUpConnections import ClientSetup, ServerSetup
import time


hostControllerAddr = '165.227.24.226'  # I am client to HostController
hostControllerPort = '5556'
deviceControllerPort = '5555' # I server to device

print("Device Controller Starting\n")

context = zmq.Context()   # get context
clientSetup = ClientSetup(context)  # instantiate the ClientSetup object
serverSetup = ServerSetup(context) # instantiate the ServerSetup object


# set up separate server and client sockets
serverSocket = serverSetup.createServerSocket() # get a server socket
serverSetup.serverBind(deviceControllerPort, serverSocket) # bind to an address
clientSocket = clientSetup.createClientSocket() # get a client socket

# NOTE: setIdentity() MUST BE CALLED BEFORE clientConnect or the identity will
# not take effect
clientSetup.setIdentity(MasterId().getDevId(), clientSocket) # get the device id
clientSetup.clientConnect(hostControllerAddr, hostControllerPort, clientSocket) # connect to server using clientSocket


poller = zmq.Poller()
poller.register(serverSocket, zmq.POLLIN)
poller.register(clientSocket, zmq.POLLIN)

#print("send a message to HostController server")
#dataToServer = "Hey there HostController Server".encode()
#cmdToServer = "02".encode()
#clientSocket.send_multipart([cmdToServer, dataToServer])
#print("sent to server, cmd={}, data={}".format(cmdToServer, dataToServer))

messages = Messages() # instantiate a Messages object

print("beginning poll")
clientCount = 0
serverCount = 0
inDict = {}
while 1:
    socks = dict(poller.poll(1000))
    if serverSocket in socks and socks[serverSocket] == zmq.POLLIN:
        ident, cmdFrmClient, data = serverSocket.recv_multipart()

        print("Message received from device: ident=", ident,"cmd=", cmdFrmClient, "data=", data)

        inDict = messages.bufferToDict(data) # create a list from the message

        print("Internal list, devType={}, cmd={}, data={}, returnList={}\n"
            .format(inDict['devType'], inDict['cmd'], inDict['data'], inDict['returnList']))

       #For testing purposes only, relay the message upstream

        messages.appendMyIdToReturnList(inDict)
        print("Sending this dictionary to HostController:", inDict)
        dataToServer = messages.dictToBuffer(inDict).encode()
        print('Sending this output message:', dataToServer)
        clientSocket.send_multipart([cmdFrmClient, dataToServer])
        print ("Sent to HostController, ident={}, cmd={}, data={}\n".format(ident, cmdFrmClient, dataToServer))

    if clientSocket in socks and socks[clientSocket] == zmq.POLLIN:
        cmdFrmServer, data = clientSocket.recv_multipart()
        print("Received from HostController: cmd=", cmdFrmServer, "data=", data)
        inDict = messages.bufferToDict(data) # create a list from the message
        print("inDict=\n", inDict)

        # For testing purposes, send the message back to the device

        outIdent = (messages.popLastReturnId(inDict)).encode() # get the device controller id
        dataToClient = (messages.dictToBuffer(inDict)).encode()
        cmdToClient = (inDict['cmd']).encode()
        print("Sending to device with cmd={}, data={} \n".format(cmdToClient, dataToClient))
        serverSocket.send_multipart([outIdent, cmdToClient, dataToClient])


#    time.sleep(1)
