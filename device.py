import zmq
from Messages import HiyaMsg, DataMsg, MasterId, Messages
from SetUpConnections import ClientSetup, ServerSetup

#deviceControllerAddr = '192.168.1.7'
deviceControllerAddr = 'localhost'

deviceControllerPort = '5555'
clientPort = ''

print("Device Starting\n")

context = zmq.Context()   # get context
clientSetup = ClientSetup(context)  # instantiate the ClientSetup object
#serverSetup = ServerSetup(context) # instantiate the ServerSetup object

# set up separate server and client sockets

clientSocket = clientSetup.createClientSocket() # get a client socket

# NOTE: setIdentity() MUST BE CALLED BEFORE clientConnect or the identity will
# not take effect
clientSetup.setIdentity(MasterId().getDevId(), clientSocket) # get the device id

clientSetup.clientConnect(deviceControllerAddr, deviceControllerPort, clientSocket) # connect to server using clientSocket


clientDevId = MasterId().getDevId()
print("Device's id=", clientDevId)

poller = zmq.Poller()
#poller.register(serverSocket, zmq.POLLIN)
poller.register(clientSocket, zmq.POLLIN)

print("beginning poll")
messages = Messages() # instantiate a Messages object

# send a test message.  This message will be passed on to the HostController and then sent back down.
#  That's the test
cmdToServer = "01".encode()
outDict = messages.createMessageDict('00', '01', 'Hello HostServer', [])
print("initial state, sending this dictionary:", outDict)
dataToServer = messages.dictToBuffer(outDict).encode()
print('sending this output message:\n', dataToServer)
clientSocket.send_multipart([cmdToServer, dataToServer])

clientCount = 0
while 1:
    socks = dict(poller.poll(1000))
    if clientSocket in socks and socks[clientSocket] == zmq.POLLIN:
        cmdFrmServer, data = clientSocket.recv_multipart()

        print("Received from DeviceController: cmd=", cmdFrmServer, "data=", data)

        dataList = messages.bufferToDict(data) # create a list

        print("internal list, devType={}, cmd={}, data={}, returnList={}"
            .format(dataList['devType'], dataList['cmd'], dataList['data'], dataList['returnList']))

#        dataToServer = ("Hello Server count={}".format(clientCount)).encode()
#        clientCount += 1
#        cmdToServer = "02".encode()
#        clientSocket.send_multipart([cmdToServer, dataToServer])
#        print("sent to server, cmd={}, data={}".format(cmdToServer, dataToServer))
