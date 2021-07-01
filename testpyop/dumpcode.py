import marshal
import binascii
import dis

fd = open('./origin/index73opcode.pyc')
fd2 = open('./game/index73opcode.pyc')
co = marshal.loads(fd.read())
co2 = marshal.loads(fd2.read())
print co.co_consts
print co2.co_consts
print binascii.hexlify(bytearray(co.co_code))
print binascii.hexlify(bytearray(co2.co_code))
print dis.dis(co)
print dis.dis(co2)
