# IOT2Host
IOT to host project
This is a proof of concept project for a network that can pass information from IOT devices to a user connected via a 
web server on a host.  The network uses ZeroMQ as it’s network infrastructure.


ZeroMQ

ZeroMQ is an asynchronous messaging library, that provides a message queue. But unlike message-oriented middleware, 
a ZeroMQ system can run without a dedicated message broker.   The Dealer/Router ZeroMQ design pattern is used entirely in this project.  

Network Message Syntax

All messages in the system use the JSON syntax which is converted to an associative array in the software.  
One benefit of using JSON, is that the data element in a message can be a JSON subset with fields unique to the 
message command.  

Node Identities

Every node in the network creates and stores an Id using a secure random generator to generate a cryptographically 
strong 16 byte random hex number that will guarantee uniqueness across the network.  On messages that a node sends
up stream as a client (a fan-in configuration), the client’s id is automatically sent as a separate frame.  
When the server sends a message to a client, it must also send a separate frame with the id of the intended client.

Round Trip Messages

Each time a client sends a message upstream to a server, it appends it’s Id to a “ReturnList” that is sent with 
each message.  The ReturnList is a FIFO (a deque) that essentially provides a return path of node Id’s that can be 
followed for a return trip.  If the ReturnList that is associated with a node (e.g. a device) is stored with a
logical description of the node (e.g. “Living room device at 2345 Elm Street, Longmont) the Host can easily send a 
message to that node with a minimum amount of work.

Node Discovery 

Since the system utilizes the CurveCP Security Handshake implementation in ZeroMQ (CurveZMQ), the initial discovery 
process in the network uses a highly secure authorization process before a node is accepted into the system.  
This initial authorization is automatically done when a node, in it’s initial state, sends an “Iam” command upstream 
to it’s server.  Since the Iam command contains all of the information about a node, it can be relayed up to the 
Host Database Process to be persisted in a database.

Heartbeating

Nodes send Heartbeat messages up and down stream to determine path integrity.  To decrease network traffic, 
a Heartbeat message is only sent if no other message has been sent during the heartbeat interval.

Device

The IOT Devices talk to the Device controller on a local network that is typically a Wifi network located behind a 
firewall on a router.  The Devices cannot be initially contacted from outside the device network, they talk only t
o the device controller. 

Device Controller

The Device controller is responsible for and controls the network of devices.  It collects,  queues and saves i
nformation coming from a device and relays it on to the Host.  Since the network of devices can consist of different d
evice types, e.g. temperature and humidity sensors, proximity detectors, etc., the device’s device type is unique 
to the purpose of the device.  In addition to the logical location or description of a device, the Device Controller 
stores the different properties of a device.

The Device controller also has the ability to talk to a user via a web application in the Device controller itself  
The user sets up the network properties, e.g. Wifi access point and password, and can assign plain language descriptions 
and locations to a device e.g. “Temp sensor in Living Room”.  When the device information changes, the Device controller 
sends it to the Host.

For convenience and security, a user account can only be setup at the Device Controller level.  After checking with the 
Host Controller for an unused name, the name and password is saved at the Host level and the Device Controller level.  
Account information can only be entered or changed at the Device Controller.

Depending on the size of the device network, the Device controller could coexist with a device.

Host Controller

The Host controller typically lives at the Host.  It collects all of the device reporting information coming from the 
Device controllers and relays it to a Host Processor.  

Host Processors

The host processors are at the highest point in the network.  It could have the job of saving the data and information 
from down stream into a database.  Or, another Host Processor could be an interface to a Web App.

Host Web App

The web app on the host allows a user to log in from anywhere and check their device information that has been saved 
at the host.  Under certain circumstances, the user can also send commands to a device.  


