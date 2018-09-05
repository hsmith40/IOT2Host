# Base class that implements the functions for the finite state machine
class FinitStateMach:
    _CurrentState = 0



# _convertCmd() converts a command in it's string form to a number

    def _convertCmd(self, cmdStr):
        print("_convertCmd() cmdStr=", cmdStr)
        cmdInt = self.cmdList[cmdStr]
        return cmdInt

# _getNextStateList() returns a state entry based on current state and event
# use the currentState parm to index into the s

    def _getStateEntry (self, currentState, cmdInt):
        currentStateList = self.states[currentState]
        currentStateEntry = currentStateList[cmdInt]
        return currentStateEntry

# from current state entry and event, get action and next state
    def _getNextStateAction(self, currentStateEntry, cmdInt):
        nextStateList = self._getStateEntry(currentStateEntry, cmdInt)
        action = nextStateList[0]
        nextState = nextStateList[1]
        return [nextState, action]

    def getStateName(self, state):
        return self.stateName[state]

    def getCurrentState(self):
        return self.stateName[self._CurrentState]

    def getCurState(self):
        return self.getStateName(self._CurrentState)

# doAction()  Parms: cmdStr string version of command
#             Returns: no return
#   1. Converts string version of command into an integer
#   2. Gets nextState and action by calling getNextStateAction()
#   3. Sets _CurrentState to nextState
#   4. Calls action()

    def doAction(self, cmdStr):
        cmdInt = self._convertCmd(cmdStr)
        [nextState, action] = self._getNextStateAction(self._CurrentState, int(cmdInt))
        print("doAction() current state={}, cmd={}, next state={}"
        .format(self._CurrentState, cmdStr, nextState))

        self._CurrentState = nextState
        action()

# getActionOnly() Parms: cmdStr = the string version of the command, e.g. "hiya"
#                 Returns: the action to be performed
#   1. Converts the string version of the command into an integer
#   2. Gets the nextState and action from the state tables (getNextStateAction())
#   3. Sets the _CurrentState to the nextState
#   4. Returns the action

    def getAction(self, cmdStr):
        cmdInt = self._convertCmd(cmdStr)
        [nextState, action] = self._getNextStateAction(self._CurrentState, int(cmdInt))
        print("getAction() current state={}, cmdInt={}, next state={}"
        .format(self._CurrentState, cmdInt, nextState))

        self._CurrentState = nextState
        return action
