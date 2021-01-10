from calendar import c
from time import sleep
from ErroHandler.merry import Merry, MyMerry
import inspect
import asyncio
merry = Merry()

@merry._try
def write_to_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)

@merry._except(IOError)
def ioerror():
    print('Error: cant write to file')

@merry._except(Exception)
def catch_all(e):
    print('Unexpected error: ' + str(e))



# write_to_file('some_file', 'some_data')

merry = Merry()

class A():
    def __init__(self) :
        merry.setObject(self)

    @merry._try
    def func(self):
        print('1')

    @merry._except(Exception)
    def erro(self,e):
        print(self.test_value)

    @merry._except(IOError)
    def ioerror(self):
        print("Error: can't write to file")

    @merry._except(KeyboardInterrupt)
    def catch_KeyboardInterrupt(self,e):
        print('KeyboardInterrupt ' + str(e))

A().func()

class B(A):
    def __init__(self) -> None:
        super().__init__()
        self.value = 'test'

    @merry._try
    def funcB(self,string:str):
        print('23')

    #Rewrite the Exception handler and read the obj.
    @merry._except(Exception)
    def getObjet(self,e):
        print(self.value,str(e))

    #Reuse the @merry._except(IOError)

B().funcB()


    @merry._else
    def test_else(self):
        print('nothing')

    @merry._finally
    def test_fi(self):
        return self.test_value

def check(obj:object):
    if isinstance(obj,object):
        obj.test_1()
    return isinstance(obj,object)


class C(B):
    def __init__(self) -> None:
        super().__init__()
        # merry.setObject(self)
        
    @merry._try
    def test_2(self, string: str):
        sleep(5)
        # raise KeyboardInterrupt('sadsad')
        # print("this is subclass's test_2" )
        # sleep(5)


    async def _async(self):
        print('test async')
    
    
    # @merry._except(ValueError)
    # def hanldeValue(self,e):
    #     print('value erro.')
    
    
    @merry._except(Exception)
    def hanldeValue(self,e):
        # if isinstance(e,KeyboardInterrupt):
        #     print('Input erro has been handled.')
        print('value erro2.')
    
    @merry._except(KeyboardInterrupt)
    def hanldekey(self,e):
        print('key erro2.')
    

    @merry._try
    def run(self):
        asyncio.run(self._async())




def testKeyInput():
    try:
        raise Exception('asd')
    except BaseException as e:
        print(e,type(e))
        
        if isinstance(e,KeyboardInterrupt):
            print(1)
        print('input erro is handled.')
import signal

def exit_t(signum, frame):
    from sys import exit
    print('You choose to stop me.')
    exit()


if __name__ == "__main__":
    # res = merry.except_
    # print(res)
    # signal.signal(signal.SIGINT, exit_t)
    # signal.signal(signal.SIGTERM, exit_t)
    
    # while 1:
    #     pass
    
    
    
    
    a = C()
    res = a.test_2('test')
    print(res)
    # res = a.run()
    # print(res)
    # testKeyInput()
    
    
    
    # awrgs_func:list = inspect.getfullargspec(a.test_2)
    # for each in awrgs_func:
    #     print(each)
    #     print(type(each))
        # print(name)
        # print(obj)
        # print('========')
        # if inspect.isclass(obj):
        #     print(obj.__name__)
    
    # print(B)
    # # print(check(a))
    # print(a.test_2)
    