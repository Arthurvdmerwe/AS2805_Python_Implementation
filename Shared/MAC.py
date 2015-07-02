from operator import *

from Crypto.Cipher import DES3
from Crypto.Cipher import DES


DES_IV = '\0\0\0\0\0\0\0\0'
DES_PAD = [chr(0x80), chr(0), chr(0), chr(0), chr(0), chr(0), chr(0), chr(0)]
DES_PAD_HEX = '8000000000000000'
KENC = '\0\0\0\1'
KMAC = '\0\0\0\2'
DO87 = '870901'
DO8E = '8E08'
DO97 = '9701'
DO99 = '99029000'


def ToBinary(string):
    """convert hex string to binary characters"""
    output = ''
    x = 0
    while x < len(string):
        output += chr(int(string[x:x + 2], 16))
        x += 2
    return output


def DES3MAC(message, key, ssc):
    "iso 9797-1 Algorithm 3 (Full DES3)"
    tdes = DES3.new(key, DES3.MODE_ECB, DES_IV)
    if ssc:
        mac = tdes.encrypt(ToBinary(ssc))
    else:
        mac = DES_IV
    message += PADBlock('')
    for y in range(len(message) / 8):
        current = message[y * 8:(y * 8) + 8]
        left = ''
        right = ''
        for x in range(len(mac)):
            left += '%02x' % ord(mac[x])
            right += '%02x' % ord(current[x])
        machex = '%016x' % xor(int(left, 16), int(right, 16))
        mac = tdes.encrypt(ToBinary(machex))
    # iso 9797-1 says we should do the next two steps for "Output Transform 3"
    # but they're obviously redundant for DES3 with only one key, so I don't bother!
    # mac= tdes.decrypt(mac)
    # mac= tdes.encrypt(mac)
    return mac


def PADBlock(block):
    "add DES padding to data block"
    # call with null string to return an 8 byte padding block
    # call with an unknown sized block to return the block padded to a multiple of 8 bytes
    for x in range(8 - (len(block) % 8)):
        block += DES_PAD[x]
    return block


def DESMAC(message, key, ssc):
    "iso 9797-1 Algorithm 3 (Retail MAC)"
    # DES for all blocks
    # DES3 for last block

    tdesa = DES.new(key[0:8], DES.MODE_ECB, DES_IV)
    tdesb = DES.new(key[8:16], DES.MODE_ECB, DES_IV)
    if ssc:
        mac = tdesa.encrypt(ToBinary(ssc))
    else:
        mac = DES_IV
    message += PADBlock('')
    for y in range(len(message) / 8):
        current = message[y * 8:(y * 8) + 8]
        left = right = ''
        for x in range(len(mac)):
            left += '%02x' % ord(mac[x])
            right += '%02x' % ord(current[x])
        machex = '%016x' % xor(int(left, 16), int(right, 16))
        # print machex
        mac = tdesa.encrypt(ToBinary(machex))
        # print mac
    mac = tdesb.decrypt(mac)

    return tdesa.encrypt(mac)


def ToHex(data):
    "convert binary data to hex printable"
    string = ''
    for x in range(len(data)):
        string += '%02x' % ord(data[x])
    return string


def HexPrint(data):
    return ToHex(data)


def MACVerify(message, key):
    mess = ToBinary(message[:len(message) - 16])
    mac = DESMAC(mess, key, '')
    if not mac == ToBinary(message[len(message) - 16:]):
        print 'MAC Error!'
        print 'Expected MAC: ', message[len(message) - 16:]
        print 'Actual MAC:   ',
        HexPrint(mac)
        return False
    return True


Message = "<STX>000000  td7W0       <FS>9VDD9002       <FS>11<FS>0056<FS>4902370000002348=121210111234123<FS>00006000<FS>00000200<FS>4F50E157E8D544B1<FS><FS><FS>VA5.00.07WV02.70.10 V04.00.19 0  0T  00 000     00000002K0047000000005K005500000000000000000000000000000000000000<FS><FS><ETX>"
ResultMac = "^EB5E 8B9A"
Message_Block = HexPrint(Message)

result = DESMAC(Message_Block, 'F92260FA70A180E1B30D9E95DAD6B823', '')
print result
print ToHex(result).upper()