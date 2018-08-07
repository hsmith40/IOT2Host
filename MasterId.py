import secrets

import json


DevId = ""
DevType = "01"

class MasterId:
    def __init__(self):
        pass

    def getDevId(self):
        global DevId
        if (DevId == ""):
            DevId = secrets.token_hex(6)
        devId = DevId.encode()
        print("type of devId=", type(devId))
        return devId



        def devType(self):
            global DevType
            return DevType


class Messages:
    def __init__(self):
        pass

    # convert a buffer (a json string) to a dictionary
    def bufferToDict(self, buffer):
        return(json.loads(buffer))

    def dictToBuffer(self, dict):
        return(json.dumps(dict))

    def createOriginatingHeader(self, devType, id, cmd):
        dict = {}
        dict['devType'] = devType()
        dict['id'] = id()
        dict['cmd'] = cmd
        return dict

# building a hiya message to be sent
# There is no data
class HiyaMsg:
    def __init__(self):
        self.cmd = "00"
    # build a json message

    def buildDict(self, id, buffer):
        dict = {"id": id, "devtp": buffer[0:2], "cmd": buffer[2:4]}
        return dict

    def buildMsg(self):
        buffer = ('{}00'.format(devType()))
        return buffer

class DataMsg:
    def __init__(self):
        self.cmd = "01"

    # build a dictionary from an incomming message
    def buildDict(self, id, buffer):
        dict = {"id": id, "devtp": buffer[0:2], "cmd": buffer[2:4], "data": buffer[4:]}
        return dict

    # build an outgoing data message
    def buildMsg(self, data):
        buffer = ('{}01{}'.format(devType(), data))
        return buffer


class InBuf:

    def __init__(self, buf):
        self.dict = json.loads(buf)

    def id(self):
        return self.dict['id']

    def cmdInt(self):
        return int(self.dict['cmd'])

    def cmd(self):
        return self.dict['cmd']

    def data(self):
        return self.dict['data']
