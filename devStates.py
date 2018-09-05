from finitStateMach import FinitStateMach
from devFuncTable import DevFuncTable

# This module declares the finite state tables for the main programs

class DevStates(FinitStateMach):
    def __init__(self, mainClassObject):
        # instantiate the DevFuncTable class with a pointer back to the
        self.f = DevFuncTable(mainClassObject)


#declare the states.  For convienence, you can use a longer name and equate
# it to a stat number, e.g. state0 = readyToGo = 0
        state0 = active = 0
        state1 = 1
        state2 = 2
        state3 = 3
        state4 = 4
        state5 = 5

#declare the Commands
        self.cmdList = {'hiya': 0, 'data': 1, 'info': 2,}


# This is a convienence list of state names in an array.  If indexed by the
# state, it will give you the name of the state

        self.stateName = ['state0', 'active', 'state2', 'state3', 'state4', 'state5']

# State list entries = [[action, nextState], [action, nextState], ....]
# The state list array is indexed by events.  Each event entry consists of
# a 2 entry array of an action (a func), and the next state (a digit)
# This array is indexed by the event

        self.state0List = [[self.f.func0, state0], [self.f.func1, state2], [self.f.func2, state3]]
        self.state1List = [[self.f.func1, state2], [self.f.func2, state3], [self.f.func3, state3]]
        self.state2List = [[self.f.func2, state3], [self.f.func3, state4], [self.f.func4, state1]]
        self.state3List = [[self.f.func3, state4], [self.f.func2, state2], [self.f.func5, state3]]
        self.state4List = [[self.f.func5, state0], [self.f.func2, state2], [self.f.func3, state3]]

# The states array is an array of state lists.  This array is indexed by
# state numbers
# You start here and select the entry that corresponds to the current state.
# This will get you to a state list...

        self.states = [self.state0List, self.state1List, self.state2List, self.state3List, self.state4List]
