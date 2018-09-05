# This class has a list of functions (func0 ...) that call functions back in
# the main class object.  Example, if the main class object is an instantion
# of the Device class, the functions in this class can call functions in
# the Device class.
#
# This class is a convienence class, it allows the state table to use the
# functions in this class instead of the functions in the main class.  That
# could be rather messy

class DevFuncTable:
    def __init__(self, mainClassObject):
        self.mainClass = mainClassObject

    def func0(self, a):
        print ('func0')
        self.mainClass.doSomething(a)

    def func1(self, a):
        print('func1')

    def func2(self, a):
        print ('func2')

    def func3(self, a):
        print ('func3')

    def func4(self, a):
        print ('func4')

    def func5(self, a):
        print ('func5')
