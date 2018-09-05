import zmq
from zmq.eventloop.ioloop import IOLoop, PeriodicCallback
from zmq.eventloop.zmqstream import ZMQStream
from Messages import HiyaMsg, DataMsg, MasterId, Messages
from SetUpConnections import ClientSetup, ServerSetup
import time


class HostController:
    def __init__(self):
        #procControllerAddr = '165.227.24.226'  # I am client to HostController
        #procControllerPort = '5557'
        hostControllerPort = '5556' # I server to device

        print("Host Controller Starting\n")

        self.context = zmq.Context()   # get context
        self.loop = IOLoop.instance()

#       self.clientSetup = ClientSetup(context)  # instantiate the ClientSetup object
        self.serverSetup = ServerSetup(self.context) # instantiate the ServerSetup object


        # set up separate server and client sockets
        self.serverSocket = self.serverSetup.createServerSocket() # get a server socket
        self.serverSetup.serverBind(hostControllerPort, self.serverSocket) # bind to an address

#       self.clientSocket = self.clientSetup.createClientSocket() # get a client socket

# NOTE: setIdentity() MUST BE CALLED BEFORE clientConnect or the identity will
# not take effect
#       self.clientSetup.setIdentity(MasterId().getDevId()) # get the device id
#       self.clientSetup.clientConnect(hostControllerAddr, hostControllerPort, self.clientSocket) # connect to server using clientSocket
        self.serverSocket = ZMQStream(self.serverSocket)
        self.serverSocket.on_recv(self.onServerRecv)
        self.messages = Messages() # instantiate a Messages object

        self.inDict = {}
        self.outDict = {}

    def onServerRecv(self,msg):
        print("msg=", msg)
        print("length of msg=", len(msg))
        ident = msg[0]
        cmdFrmClient = msg[1]
        data = msg[2]
        # is it a message from a client?
        if (len(msg) == 3):
            print("Message received from device controller: ident=", ident,"cmd=", cmdFrmClient, "data=", data)
            self.inDict = self.messages.bufferToDict(data) # create a list from the message
            print("Internal list, devType={}, cmd={}, data={}, returnList={}\n"
                    .format(self.inDict['devType'], self.inDict['cmd'], self.inDict['data'], self.inDict['returnList']))

            # For testing purposes, now send the message back down the line
            self.inDict['data'] += ' host controller got it'
            self.outIdent = self.messages.popLastReturnId(self.inDict).encode() # get the device controller id
            print("Ident poped from returnId", self.outIdent)
            dataToClient = self.messages.dictToBuffer(self.inDict).encode() # create a buffer
            print("Data to Device Controller=", dataToClient)
            cmdToClient = self.inDict['cmd'].encode()
            print("Cmd to Device Controller=", cmdToClient)
            print("Sending to outIdent =", self.outIdent)
            self.serverSocket.send_multipart([self.outIdent, cmdToClient, dataToClient])

        else:
            print("Message received from host proc: cmd=", cmdFrmClient, "data=", data)


    def start(self):
    #        self.periodic.start()
        try:
            self.loop.start()

        except KeyboardInterrupt:
            pass


def main():
	my_server = HostController()
	my_server.start()

if __name__ == '__main__':
	main()
