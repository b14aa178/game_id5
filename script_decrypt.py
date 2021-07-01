import zlib
import argparse
import binascii
import os

import rotor  
import marshal  
import binascii  
import argparse  
import marshal  
import pymarshal
import uncompyle6


class PYCEncryptor(object):  
    def __init__(self):
        self.opcode_encrypt_map = {
            1: 46, 2: 38, 3: 12, 4: 37, 5: 66, 10: 81, 11: 32, 12: 35, 13: 67, 15: 63, 19: 9, 20: 23, 21: 36, 22: 44, 23: 49, 24: 52, 25: 13, 26: 57, 28: 39, 30: 24, 31: 25, 32: 26, 33: 27, 40: 14, 41: 15, 42: 16, 43: 17, 50: 86, 51: 87, 52: 88, 53: 89, 54: 82, 55: 55, 56: 21, 57: 8, 58: 65, 59: 6, 60: 34, 61: 22, 62: 5, 63: 19, 64: 71, 65: 60, 66: 43, 67: 58, 68: 30, 71: 85, 72: 78, 73: 31, 74: 74, 75: 75, 76: 84, 77: 42, 78: 47, 79: 53, 80: 83, 81: 33, 83: 51, 84: 48, 85: 45, 87: 50, 88: 64, 89: 54, 90: 125, 91: 157, 93: 159, 94: 149, 96: 153, 97: 132, 99: 111, 101: 114, 102: 99, 103: 96, 104: 135, 105: 90, 106: 151, 107: 101, 108: 156, 109: 105, 110: 134, 111: 116, 112: 155, 113: 148, 114: 172, 115: 137, 116: 130, 119: 110, 120: 128, 121: 103, 122: 158, 130: 100, 131: 124, 132: 131, 133: 136, 140: 141, 141: 142, 142: 143, 143: 94
        }
        self.opcode_decrypt_map = {self.opcode_encrypt_map[key]: key for key in self.opcode_encrypt_map}
        self.pyc27_header = "\x03\xf3\x0d\x0a\x00\x00\x00\x00"

    def _decrypt_file(self, filename):
        os.path.splitext(filename)
        content = open(filename).read()
        try:
            m = pymarshal.loads(content)
        except Exception as e:
            print("[!] error: %s" % str(e))
            try:
                m = marshal.loads(content)
            except Exception as e:
                print("[!] error: %s" % str(e))
                return None
        return m.co_filename.replace('\\', '/'), pymarshal.dumps(m, self.opcode_decrypt_map)

    def decrypt_file(self, input_file, output_file=None):
        result = self._decrypt_file(input_file)
        if not result:
            return
        pyc_filename, pyc_content = result
        if not output_file:
            output_file = os.path.basename(pyc_filename) + '.pyc'
        with open(output_file, 'wb') as fd:
            fd.write(self.pyc27_header + pyc_content)
    
        output_file2 = output_file + '_noheader.pyc'
        with open(output_file2, 'wb') as fd:
            fd.write(pyc_content)

def main():  
    parser = argparse.ArgumentParser(description='onmyoji py decrypt tool')
    parser.add_argument("INPUT_NAME", help='input file')
    parser.add_argument("OUTPUT_NAME", help='output file')
    args = parser.parse_args()

def _reverse_string(s):
    l = list(s)
    l = map(lambda x: chr(ord(x) ^ 154), l[0:128]) + l[128:]
    l.reverse()
    return ''.join(l)


def unnpk(data):
    asdf_dn = 'j2h56ogodh3se'
    asdf_dt = '=dziaq.'
    asdf_df = '|os=5v7!"-234'
    asdf_tm = asdf_dn * 4 + (asdf_dt + asdf_dn + asdf_df) * 5 + '!' + '#' + asdf_dt * 7 + asdf_df * 2 + '*' + '&' + "'"
    import rotor
    rotor = rotor.newrotor(asdf_tm)
    data = rotor.decrypt(data)
    data = zlib.decompress(data)
    data = _reverse_string(data)
    return data

def main():

    for f in os.listdir('.'):
        if "unnpk" in f:
            continue

        if ".py" in f:
            continue


         
        encryptor = PYCEncryptor()
        encryptor.decrypt_file(f, f+'.pyc')

        try:
            with open(f+'.py', "w") as fileobj:
                uncompyle6.uncompyle_file(f+'.pyc', fileobj)
        except Exception as e:
            print e

if __name__ == '__main__':
    main()
