# testMessages.py
from Messages import Messages
from Messages import devType

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
