#!python3

import marshal
import dis
import sys
import binascii


def main():
    if len(sys.argv) != 3:
        print 'error arguments'
        return

    cobj1 = open(sys.argv[1], 'r')
    cobj2 = open(sys.argv[2], 'r')

    lines1 = cobj1.read().splitlines()
    lines2 = cobj2.read().splitlines()

    if len(lines1) != len(lines2):
        print "lines not same %d %d" % (len(lines1), len(lines2))
        return

    i = 0
    opmap = {}
    while i < len(lines1):
        line1 = lines1[i]
        line2 = lines2[i]
        i += 1

        if "--code--" in line1:
            continue

        if len(line1) % 2 != 0:
            raise "error length hexstr"

        if len(line1) != len(line2):
            print 'this line not has same len, pass'
            print line1
            print line2
            continue

        line1bytes = bytearray(binascii.unhexlify(line1))
        line2bytes = bytearray(binascii.unhexlify(line2))

        print "line byte size %d" % len(line1bytes)
        print "line byte size %d" % len(line2bytes)

        j = 0
        need_del = []
        while j < len(line1bytes):
            b = line1bytes[j]
            b2 = line2bytes[j]

            if b >= 90:
                j += 3

                # check opcode
                if j - 1 < len(line1bytes):
                    if line1bytes[j - 1] != line2bytes[j - 1]:
                        print binascii.hexlify(line1bytes[0:j])
                        raise Exception('check opcode error')
                    if line2bytes[j - 2] != line1bytes[j - 2]:
                        print binascii.hexlify(line1bytes[0:j])
                        raise Exception('bytes not equal')

            if b < 90:
                j += 1

            if b in opmap:
                checkb = opmap[b]
                if checkb != b2:
                    print 'maped opcode has new value %d %d %d' % (b, checkb, b2)
                    if b not in need_del:
                        need_del.append(b)

            opmap[b] = b2

    for d in need_del:
        print 'remove %d' % d
        del opmap[d]

    print opmap
    pass


if __name__ == '__main__':
    main()
