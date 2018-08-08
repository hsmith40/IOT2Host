# Messages
#
# A note about Servers and Clients.
# Every node that acts as a controller, i.e. Device Controller, Host Controller,
# has a server side and a client side.  This is because a controller can be called
# upon to relay messages.  If look at the top end of the network being the IOT Host
# and the bottom end being the Device, then we can use 'up' and 'down' as a
# direction of flow, e.g. the Device sends messages 'up' to the Device Controller,
# the Device controller sends messages 'up' to the Host Controller, etc.  It
# even conceivable that a message can be sent all the way up from a Device
# to a Host Processor and a Host Processor can send a message down to a Device
# A controller must therefore be able to originate messages going up or down as
# well and relay messages it receives from either above him or below him.
# In this system, I am using a ZeroMQ Design Pattern called the Router/Dealer
# pattern.  The Router can connect of n+ Dealers but a Dealer can only connect
# to a single Router.  That fits well here because a Device controller must be
# able to connect to multiple devices forming a device network and a Host Controller
# must be able to connect to multiple Device Controllers forming an entire
# IOT network.  Note that scaling could require multiple Host Controllers.
# So, each controller has two sides, a Router (server) side and a Dealer (client)
# side.  The Router/Server side talks down stream and the Dealer/Client talks
# up stream
# Sinc multiple Dealer/Clients can talk to one Router/Server, there must be a
# way for a Router/Server to send a message to a specific Dealer/Client.  This
# is how that is done (ZeroMQ): when a Dealer/Client send a message to it's
# Router/Server, it adds a device id to the message.  Actually, it sends the id
# as a separate frame that proceeds the message.  The Router/Server can simply
# send an id frame that proceeds a data frame back to it's clients and the
# proper client will receive the message.
# In the IOT2Host system, each node that has a server/client combination or a
# client only combination (e.g. a device), creates it's own id using a secret
# random number generator.  The id is long enough so that the chance of
# duplicates is infinitesimal.
#
# The json message . TBD

import secrets
import json


MastId = ""
DevType = "01"

#def id():
#    global MastId
#    if (MastId == ""):
#        MastId = secrets.token_hex(6) # creates a 12 byte string
#        MastId = secrets.token_bytes(6) # creates a 12 byte string

#    return MastId



def devType():
    global DevType
    return DevType

class MasterId:
    def __init__(self):
        pass

    def getDevId(self):
        global MastId
        if (MastId == ""):
            MastId = secrets.token_hex(6)
        devId = MastId
        print("MasterId::getDevId(), id=", devId)
        return devId



    def devType(self):
        global DevType
        return DevType


# A message dictionary is used within the system.  It consists of the following
# {'devType' : 'nn', 'cmd' : 'nn', 'data' : '...data', 'returnList' : [id, id, id]}
# devType = 2 digits, The device type.  Devices are catagoried into types, e.g. temp sensing, etc
# cmd = 2 digits, The command associated with the message, e.g. hiya, data, etc
# data = n chars, The data associated with the message
# returnList = a list, The returnList is a list of the id's of nodes.  When a
#               node receives a message, it appends it's id to the returnList

class Messages:
    def __init__(self):
        pass

    # convert a input buffer (a json string) to a dictionary
    # bufferToDict() parms:  buffer = input buffer, which is a json string,
    #     from a 0MQ read
    #  returns: a dictionary based on the json string
    #
    def bufferToDict(self, buffer):
        return(json.loads(buffer))

    # convert a dictionary into a json string
    # dictToBuffer() parms: dict - a dictionary (message dictionary)
    #  returns: a stringified form of the dictionary in json format
    def dictToBuffer(self, dict):
        return(json.dumps(dict))

    # create a new message dictionary with devType, cmd and returnList
    # createMessageDict() parms: devType, a 2 digit devtype
    #                            cmd, a 2 digit command
    #                            returnList, a LIST of return ids
    #  returns: a dictionary {'devType':devtype, 'cmd':cmd, 'returnList':[id,id,id]}

    def createMessageDict(self, devType, cmd, data, returnList):
        dict = {}
        list = returnList
        dict['devType'] = devType
        dict['cmd'] = cmd
        dict['data'] = data
        list.append(MasterId().getDevId())
        dict['returnList'] = list
        return dict

    # Append my id to a return list
    # appendMyIdToReturnList() parms: dict - the message dictionary
    #  returns: a new list with my id appended

    def appendMyIdToReturnList(self, dict):
        list=dict['returnList']
        list.append(MasterId().getDevId())
        return dict


    # createOutMessage() parms: an internal message dictionary
    # returns: a stringified json message
    def createOutMessage(self, dictionary):
        msg = json.dumps(dictionary)
        return msg

    # Pops the last id in the returnId list from the message dict and returns it
    # popLastReturnId() parms: a message dictionary
    # returns: the last id in the returnList
    # NOTE: the last id is removed from the list

    def popLastReturnId(self, dict):
        returnIds = dict['returnList']
        returnId = returnIds.pop()
        return returnId

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
        buffer = ('{}00'.format(MasterId().devType()))
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

"""
# testMessages.py
#import Messages

# create a brand new message from an orignating node
# pass my devType, cmd, and an empty return list.  This Message
# is a "hiya" message

aNewMessage = Messages().createMessageDict(devType(), '00' ,[])
print("A new message =", aNewMessage)

outBuf = Messages().createOutMessage(aNewMessage)
print("The buffer to be sent (json)=", outBuf)

# now pretend I got a buffer from zmq, I'll use outBuf in this case
# I want to create a message dictionary

inDict = Messages().bufferToDict(outBuf)
# print the new inDict

print("\n")
print("Now I'm the next guy, I got a buffer, I converted to a dict:", inDict)

# now I want to append my id to the end and create a buffer
# that I can send

newOutDict = Messages().appendMyIdToReturnList(inDict)
print("newOutDict with my id appended =", newOutDict)

newOutBuf = Messages().createOutMessage(newOutDict)
print("newOutBuf with my id appended", newOutBuf)

# now I will pretend that I got the above msg and I
# want to return a message back to the sender
# So, I want to get the last return id in the list

# I got a message buffer, so I will convert it to a dict
# I'll just use the buffer I just created

inDict = Messages().bufferToDict(newOutBuf)

# now I want to pop off the last return id

returnId = Messages().popLastReturnId(inDict)
print("\nI want to send a return msg")
print(" the returnId from last message I got=", returnId)

print("The dict is now:", inDict)

print("I can create a new Buffer now and send it")
"""
