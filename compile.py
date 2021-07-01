import marshal  
import sys
import dis
import binascii

def print_opcode(cobj1):  
    print '--------code--------'
    print binascii.hexlify(bytearray(cobj1.co_code))


def print_dis(obj):
    print '--------dis--------'
    try:
        dis.dis(obj)
    except Exception as e:
        print e

def print_names(obj):
    print '--------name--------'
    print obj.co_varnames

def print_names2(obj):
    print '--------name--------'
    print obj.co_names

def print_consts(obj):
    print '--------consts--------'
    print obj.co_consts

def print_obj(obj):
    print '---------------------------------------'
    print_opcode(obj)
    print_consts(obj)
    print_names(obj)
    print_names2(obj)
    print_dis(obj)

    for const1 in obj.co_consts:
        if hasattr(const1, 'co_code'):
            print_obj(const1)

    pass

def main():  
    if len(sys.argv) != 2:
        print 'error arguments'
        return


    filename = sys.argv[1]  
    if ".pyc" in filename:
        
        cobj1 = open(filename, 'r')
        co = marshal.loads(cobj1.read())

        print_obj(co)
        
        cobj1.close() 

    else:

        cobj1 = open(filename, 'r')
        cobj2 = open(filename+'.pyc', 'wb')
        x = compile(cobj1.read(), '', 'exec')
        marshal.dump(x, cobj2)

        cobj2 = open(filename+'.pyc', 'r')
        co = marshal.loads(cobj2.read())


        print '--------consts--------'
        print co.co_consts
        print_opcode(co)
        print_dis(co)
    
        cobj1.close() 
        cobj2.close() 

if __name__ == '__main__':  
    main()
