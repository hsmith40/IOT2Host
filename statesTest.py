from devStates import DevStates


class StatesTest:
    def __init__(self):
        # instantiate the DevStates class and pass along a pointer back to me
        # This is necessary because the function in the FunctTable class
        # will be calling functions in my class
        self.devTab = DevStates(self)

    def doSomething(self, a):
        print("doSomething, a=", a)

    def testit(self):
        devTab = DevStates(self)
        cmd = 'hiya'
        print('\ncurrent state={}, cmd={}'.format(devTab.getCurrentState(), cmd))
        print(' action=funct1, next state=2')
        act = devTab.getAction(cmd)
        inBuf = {'a':'1','b':'2'}
        act(inBuf)

        cmd="info"
        print('\ncurrent state={}, cmd={}'.format(devTab.getCurrentState(), cmd))
        print(' action=funct4, next state=1')
        act = devTab.getAction(cmd)
        act(1)

        cmd="data"
        print('\ncurrent state={}, cmd={}'.format(devTab.getCurrentState(), cmd))
        print(' action=funct2, next state=3')
        act = devTab.getAction(cmd)
        act(1)

        cmd ="info"
        print('\ncurrent state={}, cmd={}'.format(devTab.getCurrentState(), cmd))
        print(' action=funct3, next state=3')
        act = devTab.getAction(cmd)
        act(1)

def main():
    my_server = StatesTest()
    my_server.testit()

if __name__ == '__main__':
        	main()
