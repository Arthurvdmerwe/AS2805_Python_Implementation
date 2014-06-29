from socket import *

from AS2805 import AS2805
from AS2805Errors import *


# Configure the server
serverIP = "127.0.0.1"
serverPort = 9002
maxConn = 5
bigEndian = True
#bigEndian = False


# Create a TCP socket
s = socket(AF_INET, SOCK_STREAM)
# bind it to the server port
s.bind((serverIP, serverPort))
# Configure it to accept up to N simultaneous Clients waiting...
s.listen(maxConn)


# Run forever
while 1:
    #wait new Client Connection
    connection, address = s.accept()
    while 1:
        # receive message
        isoStr = connection.recv(2048)
        if isoStr:
            print "\nInput ASCII |%s|" % isoStr
            pack = AS2805()
            #parse the iso
            try:
                if bigEndian:
                    pack.setNetworkISO(isoStr)
                else:
                    pack.setNetworkISO(isoStr, False)

                v1 = pack.getBitsAndValues()
                for v in v1:
                    print 'Bit %s of type %s with value = %s' % (v['bit'], v['type'], v['value'])

                if pack.getMTI() == '0800':
                    print "\tThat's great !!! The client send a correct message !!!"
                else:
                    print "The client dosen't send the correct message!"
                    break


            except InvalidAS2805, ii:
                print ii
                break
            except:
                print 'Error Occured'
                break

            #send answer
            pack.setMTI('0810')
            pack.setBit(39, '00')  # Successful
            if bigEndian:
                ans = pack.getNetworkISO()

            else:
                ans = pack.getNetworkISO(False)

            print 'Sending answer %s' % ans
            connection.send(ans)

        else:
            break
        # close socket          
    connection.close()
    print "Closing..."