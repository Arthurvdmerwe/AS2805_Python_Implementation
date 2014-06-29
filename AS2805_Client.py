import socket
import sys
import time
from datetime import datetime

from AS2805 import AS2805
from AS2805Errors import *



# Configure the client
#serverIP = "196.26.173.115" 
#serverPort = 50089
serverIP = "127.0.0.1"
serverPort = 9002
numberEcho = 1
timeBetweenEcho = 5 # in seconds

bigEndian = True
#bigEndian = False

s = None
for res in socket.getaddrinfo(serverIP, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error, msg:
        s = None
        continue
    try:
        s.connect(sa)
    except socket.error, msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print 'Could not connect :('
    sys.exit(1)


def Alaric_Login():
    res = False
    d = datetime.now()
    iso = AS2805(debug=False)
    iso.setMTI('0800')
    iso.setBit(7, d.strftime("%m%d%H%M%S"))
    iso.setBit(11, '000001')
    iso.setBit(12, d.strftime("%H%M%S"))
    iso.setBit(13, d.strftime("%m%d"))
    iso.setBit(70, '001')
    try:
        message = iso.getNetworkISO()
        s.send(message)
        print 'Sending ... %s' % message
        ans = s.recv(2048)
        print "Response  = %s" % ans
        isoAns = AS2805()
        isoAns.setNetworkISO(ans)
        v1 = isoAns.getBitsAndValues()
        for v in v1:
            print 'Bit %s of type %s with value = %s' % (v['bit'], v['type'], v['value'])

        if isoAns.getMTI() == '0810':
            if isoAns.getBit(39) == '00':
                print "0800 Login sucessful"
                res = True
            else:
                print "0800 Response Code = %s, Login Failed" % (isoAns.getBit(39),)
        else:
            print "Could not login with 0800"

    except InvalidAS2805, ii:
        print ii

    return res


def Alaric_KeyExchange():
    print "PostBridge_KeyExchange()"
    res = False
    d = datetime.now()
    iso = AS2805(debug=False)
    iso.setMTI('0800')
    iso.setBit(7, d.strftime("%m%d%H%M%S"))
    iso.setBit(11, '000001')
    iso.setBit(12, d.strftime("%H%M%S"))
    iso.setBit(13, d.strftime("%m%d"))
    iso.setBit(70, '101')
    try:
        message = iso.getNetworkISO()
        s.send(message)
        print 'Sending ... %s' % message
        ans = s.recv(2048)
        print "Response  = %s" % ans
        isoAns = AS2805()
        isoAns.setNetworkISO(ans)
        v1 = isoAns.getBitsAndValues()
        for v in v1:
            print 'Bit %s of type %s with value = %s' % (v['bit'], v['type'], v['value'])

        if isoAns.getMTI() == '0810':
            if isoAns.getBit(39) == '00':
                print "0800 Key Exchange sucessful"
                Value = isoAns.getBit(125)[3:]
                Key = Value[0:32]
                Check = Value[32:]
                print "Key = %s, Check = %s" % (Key, Check,)
                res = True
            else:
                print "0800 Response Code = %s, Key Exchange Failed" % (isoAns.getBit(39),)
        else:
            print "Could not key exchange with 0800"

    except InvalidAS2805, ii:
        print ii


if __name__ == '__main__':
    if Alaric_Login():
        Alaric_KeyExchange()

    s.settimeout(5)
    print "timeout = %s" % (s.gettimeout())
    while (True):
        try:
            ans = s.recv(2048)
        except socket.error as e:
            print "%s, Noting Received, Error = %s" % (datetime.now(), e)
        time.sleep(10)
