import zmq
#from zmq.eventloop.ioloop import IOLoop, PeriodicCallback
#from zmq.eventloop.zmqstream import ZMQStream
import asyncio
from Messages import HiyaMsg, DataMsg, Messages, MasterId
from SetUpConnections import ClientSetup, ServerSetup
import time

class DeviceController:
    def __init__(self):
#        hostControllerAddr = '165.227.24.226'  # I am client to HostController
        hostControllerAddr = 'localhost'  # I am client to HostController

        hostControllerPort = '5556'
        deviceControllerPort = '5555' # I server to device

        print("Device Controller Starting\n")

        self.context = zmq.Context()   # get context

        self.clientSetup = ClientSetup(self.context)  # instantiate the ClientSetup object
        self.serverSetup = ServerSetup(self.context) # instantiate the ServerSetup object


# set up separate server and client sockets
        self.serverSocket = self.serverSetup.createServerSocket() # get a server socket
        self.serverSetup.serverBind(deviceControllerPort, self.serverSocket) # bind to an address
        self.clientSocket = self.clientSetup.createClientSocket() # get a client socket

        # NOTE: setIdentity() MUST BE CALLED BEFORE clientConnect or the identity will
        # not take effect
        self.clientSetup.setIdentity(MasterId().getDevId(), self.clientSocket) # get the device id
        self.clientSetup.clientConnect(hostControllerAddr, hostControllerPort, self.clientSocket) # connect to server using clientSocket
        self.messages = Messages() # instantiate a Messages object

#        self.serverSocket = ZMQStream(self.serverSocket)
#        self.clientSocket = ZMQStream(self.clientSocket)

#        self.serverSocket.on_recv(self.onServerRecv)
#        self.clientSocket.on_recv(self.onClientRecv)

        self.inDict = {}

    # Receive from Host Controller
    async def onClientRecv(self):
        clientMsg = []
        print("1.onClientRecv")
        await asyncio.sleep(.01)
        def clientRecv():
            nonlocal clientMsg
            clientMsg = self.clientSocket.recv_multipart()
        await clientRecv()
        print("onClientRecv() msg=", clientMsg)
        print("length of msg=", len(clientMsg))
        cmdFrmHostController = clientMsg[0]
        data = clientMsg[1]
        print("Message received from host controller: cmd=", cmdFrmHostController, "data=", data)

        # Create a dictionary from the Json msg from Host Controller
        self.inDict = self.messages.bufferToDict(data) # create a list from the message
        print("Internal list, devType={}, cmd={}, data={}, returnList={}\n"
                .format(self.inDict['devType'], self.inDict['cmd'], self.inDict['data'], self.inDict['returnList']))
        # For testing purposes, send the message back to the device

        # Get the last return identity
        self.outIdent = (self.messages.popLastReturnId(self.inDict)).encode() # get the device controller id
        dataToClient = (self.messages.dictToBuffer(self.inDict)).encode()
        cmdToClient = (self.inDict['cmd']).encode()
        print("Sending to device with cmd={}, data={} \n".format(cmdToClient, dataToClient))
        self.serverSocket.send_multipart([self.outIdent, cmdToClient, dataToClient])


    # Receive from Device

    async def onServerRecv(self):
        print("1.onServerRecv")
#        await asyncio.sleep(.01)

#        serverMsg = self.serverSocket.recv_multipart()
        serverMsg = []
        part = await self.serverSocket.recv()
        serverMsg.append(part)
        print("onServerRecv, part=", part)
        # have first part already, only loop while more to receive
        while self.serverSocket.getsockopt(zmq.RCVMORE):
            part = self.serverSocket.recv()
            self.serverMsg.append(part)



        print("onServerRecv msg=", serverMsg)
        print("length of msg=", len(serverMsg))
        ident = serverMsg[0]
        cmdFrmDevice = serverMsg[1]
        data = serverMsg[2]
        # Create a dictionary from the incoming msg from Device
        self.inDict = self.messages.bufferToDict(data) # create a list from the message

        print("Internal list, devType={}, cmd={}, data={}, returnList={}\n"
            .format(self.inDict['devType'], self.inDict['cmd'], self.inDict['data'], self.inDict['returnList']))

        print("Message received from device: ident=", ident,"cmd=", cmdFrmDevice, "data=", data)
        #For testing purposes only, relay the message upstream

        self.messages.appendMyIdToReturnList(self.inDict)
        print("Sending this dictionary to HostController:", self.inDict)
        self.dataToServer = self.messages.dictToBuffer(self.inDict).encode()
        print('Sending this output message:', self.dataToServer)
        self.clientSocket.send_multipart([cmdFrmDevice, self.dataToServer])
        print ("Sent to HostController, ident={}, cmd={}, data={}\n".format(ident, cmdFrmDevice,  self.dataToServer))


    async def start(self):
        while 1:
            pass

def main():
    my_server = DeviceController()
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(my_server.onServerRecv())
        asyncio.ensure_future(my_server.onClientRecv())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()

if __name__ == '__main__':
	main()
