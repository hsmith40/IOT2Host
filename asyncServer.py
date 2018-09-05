import asyncio
import zmq
from zmq.asyncio import Context
from zmq.eventloop.ioloop import IOLoop, PeriodicCallback


class Receive:
    def __init__(self):
        self.stop = False
        self.conx = Context.instance()
        self.socket = self.conx.socket(zmq.ROUTER)
        self.socket.bind('tcp://*:5555')
        self.periodic = PeriodicCallback(self.timer, 4000)
        self.periodic.start()

    def prt(self,message):
        print('id=', message[0])
        print('data=', message[1])
        if (message[1] == b'exit'):
            self.stop = True

    async def recv(self):
        while (self.stop == False):
            msg = await self.socket.recv_multipart()
            self.prt(msg)
        self.socket.close()

    async def timer(self):
        print('OMG asynchronicity!')

loop = asyncio.get_event_loop()
recve = Receive()

loop.run_until_complete(recve.recv())
#loop.run_until_complete(recve.timer())



loop.close()
