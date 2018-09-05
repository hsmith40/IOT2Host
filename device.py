import zmq
from zmq.eventloop.ioloop import IOLoop, PeriodicCallback
from zmq.eventloop.zmqstream import ZMQStream
from Messages import HiyaMsg, DataMsg, MasterId, Messages
from SetUpConnections import ClientSetup, ServerSetup

class Device:
    def __init__(self):
        deviceControllerAddr = 'localhost'

        deviceControllerPort = '5555'
        clientPort = ''

        print("Device Starting\n")

        self.context = zmq.Context()   # get context

        self.loop = IOLoop.instance()

        self.clientSetup = ClientSetup(self.context)  # instantiate the ClientSetup object
#serverSetup = ServerSetup(context) # instantiate the ServerSetup object

# set up separate server and client sockets

        self.clientSocket = self.clientSetup.createClientSocket() # get a client socket



        # NOTE: setIdentity() MUST BE CALLED BEFORE clientConnect or the identity will
        # not take effect
        self.clientSetup.setIdentity(MasterId().getDevId(), self.clientSocket) # get the device id

        self.clientSetup.clientConnect(deviceControllerAddr, deviceControllerPort, self.clientSocket) # connect to server using clientSocket

        self.clientSocket = ZMQStream(self.clientSocket)
        self.clientSocket.on_recv(self.onClientRecv)
        self.messages = Messages() # instantiate a Messages object

    def onClientRecv(self,msg):
        print("on_recv, msg=", msg)
        self.cmdFrmServer = msg[0]
        self.data = msg[1]
        print("Received from DeviceController: cmd=", self.cmdFrmServer, "data=", self.data)

        self.dataList = self.messages.bufferToDict(self.data) # create a list

        print("internal list, devType={}, cmd={}, data={}, returnList={}"
        .format(self.dataList['devType'], self.dataList['cmd'], self.dataList['data'], self.dataList['returnList']))


        self.clientDevId = MasterId().getDevId()
        print("Device's id=", self.clientDevId)

    def start(self):
    #        self.periodic.start()
        cmdToServer = "001".encode()
        outDict = self.messages.createMessageDict('00', '001', 'Hello HostServer', [])
        print("initial state, sending this dictionary:", outDict)
        dataToServer = self.messages.dictToBuffer(outDict).encode()
        print('sending this output message:\n', dataToServer)
        self.clientSocket.send_multipart([cmdToServer, dataToServer])
        try:
            self.loop.start()

        except KeyboardInterrupt:
            pass




def main():
	my_device= Device()
	my_device.start()

if __name__ == '__main__':
	main()
