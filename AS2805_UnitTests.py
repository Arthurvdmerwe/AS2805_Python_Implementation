__author__ = 'root'
import unittest
from AS2805 import AS2805
from Shared.ByteUtils import ByteToHex, HexToByte


"""
            Key Exchnage Test Cases
"""

class AS2805_0820_TestCases(unittest.TestCase):
    def setUp(self):
        self.AS205 = AS2805()
        self.Host_Request = "08208220000080010800040000001000000001041021410084400861100016303332aa0dba804fa9f9032432e9e1239eeb4db2260b76f343ccdd90823af354f3f2a00000000000000002010106579944"
        self.Host_Response = "083082200000820108000400000010000000010410520700036008611000163030303036dee885d32313000000000000000201010861100016"
        self.Switch_Request = "0820822000008001080004000000100000000104105142000360065799443033320f5e4728ede11727ad5df16add5074d820fe8223fd250762e55faebb715ef682000000000000000201010861100016"
        self.Switch_Response = "0830822000008201080004000000100000000104102141008440086110001630303030365e728f034b200000000000000002010106579944"

class Default_0820TestCasePack(AS2805_0820_TestCases):

    def runTest(self):

        print "Switch 0820 Test"

        iso_pack = AS2805(debug=False)
        iso_pack.setMTI('0820')
        iso_pack.setBit(7, '0104105142')
        iso_pack.setBit(11, '000360')
        iso_pack.setBit(33, '579944')
        iso_pack.setBit(48, '0F5E4728EDE11727AD5DF16ADD5074D820FE8223FD250762E55FAEBB715EF682')
        iso_pack.setBit(53, '0000000000000002')
        iso_pack.setBit(70, '101')
        iso_pack.setBit(100, '61100016')

        net_iso = iso_pack.getNetworkISO()

        self.assertEqual(net_iso[4:].encode('hex'), self.Switch_Request, 'Message is not a Match')


class Default_0820TestCaseUnPack(AS2805_0820_TestCases):

    def runTest(self):

        print "Switch 0830 Test"

        iso_resp = AS2805(debug=False)
        iso_resp.setNetworkISO(HexToByte('ffffffff' + self.Host_Request))
        host_iso = iso_resp.getNetworkISO()

        self.assertEqual(host_iso[4:].encode('hex'), self.Host_Request, 'Message is not a Match')


class Default_0830UnTestCasePack(AS2805_0820_TestCases):
    def runTest(self):

        print "Switch 0820 Test"

        iso_pack = AS2805(debug=False)
        iso_pack.setMTI('0830')
        iso_pack.setBit(7, '0104102141')
        iso_pack.setBit(11, '008440')
        iso_pack.setBit(33, '61100016')
        iso_pack.setBit(39, '00')
        iso_pack.setBit(48, '5E728F034B20')
        iso_pack.setBit(53, '0000000000000002')
        iso_pack.setBit(70, '101')
        iso_pack.setBit(100, '579944')

        net_iso = iso_pack.getNetworkISO()

        self.assertEqual(net_iso[4:].encode('hex'), self.Switch_Response, 'Message is not a Match')


class Default_0830UnTestCaseUnPack(AS2805_0820_TestCases):
    def runTest(self):

        print "Switch 0830 Test"

        iso_resp = AS2805(debug=False)
        iso_resp.setNetworkISO(HexToByte('ffffffff' + self.Host_Response))
        host_iso = iso_resp.getNetworkISO()

        self.assertEqual(host_iso[4:].encode('hex'), self.Host_Response, 'Message is not a Match')


class AS2805_0800_TestCases(unittest.TestCase):
    def setUp(self):

        self.AS205 = AS2805()

        self.Host_Request    = "0800822000008001000004000000100000000218070354008698086110001630303857a0d5c993a6e154000106579944"
        self.Host_Response   = "08108220000082010000040000001000000002180703540000650861100016313230303000010861100016"
        self.Switch_Request  = "08008220000080010000040000001000000002181803550000650861100016303038b029fd7859c9591d00010861100016"
        self.Switch_Response = "081082200000820100000400000010000000021818035500869809437586002f30303030382c4403562df3c2e0000109437586002f"



class Default_0810UTestCaseUnPack(AS2805_0800_TestCases):
    def runTest(self):

        print "Switch 0810 Test"
        iso_resp = AS2805(debug=False)
        iso_resp.setNetworkISO(HexToByte('ffffffff' + self.Host_Response))
        host_iso = iso_resp.getNetworkISO()

        self.assertEqual(host_iso[4:].encode('hex'), self.Host_Response, 'Message is not a Match')

        print "Switch 0810 Test"
        iso_resp = AS2805(debug=False)
        iso_resp.setNetworkISO(HexToByte('ffffffff' + self.Switch_Response))
        host_iso = iso_resp.getNetworkISO()

        self.assertEqual(host_iso[4:].encode('hex'), self.Switch_Response, 'Message is not a Match')



class Default_0800TestCasePack(AS2805_0800_TestCases):
    def runTest(self):

        print "Switch 0800 Test"

        iso_resp = AS2805(debug=False)
        iso_resp.setMTI('0800')
        iso_resp.setBit(7, '0218070354')
        iso_resp.setBit(11, '008698')
        iso_resp.setBit(33, '61100016')
        iso_resp.setBit(48, '57A0D5C993A6E154')
        iso_resp.setBit(70, '001')
        iso_resp.setBit(100, '579944')

        host_iso = iso_resp.getNetworkISO()
        self.assertEqual(host_iso[4:].encode('hex'), self.Host_Request, 'Message is not a Match')

        print "Switch 0800 Test"

        iso_resp = AS2805(debug=False)
        iso_resp.setMTI('0800')
        iso_resp.setBit(7, '0218180355')
        iso_resp.setBit(11, '000065')
        iso_resp.setBit(33, '61100016')
        iso_resp.setBit(48, 'B029FD7859C9591D')
        iso_resp.setBit(70, '001')
        iso_resp.setBit(100, '61100016')

        host_iso = iso_resp.getNetworkISO()
        self.assertEqual(host_iso[4:].encode('hex'), self.Switch_Request, 'Message is not a Match')



class AS2805_0200_TestCases(unittest.TestCase):
    def setUp(self):
        self.AS205 = AS2805()
        self.Host_Response =  "02103222001182c008810110000000000020000107234745000506010844000002000656025808611000163030533932313831363334333735383630303020202020202000000000000000010000000000009550fec000000000"
        self.Switch_Request = "0200323a449128e218810110000000000020000107234721000506104721010801085811002141440000020006560258375188680100002932d15122015076719950000f3530303831303437303530365339323138313633343337353836303030202020202020383030204c414e47444f4e2053542c202020202020202020204d414449534f4e202020202020415530323854434330315c45464330303030303030305c434349305c46424b565ca8fb4e47eacb0fa1000000000000000200000000000029365a0400000000"
        self.Switch_RequestEMV = ""
        self.Host_ResponseMEV = ""

class Default_0200PackTestCase(AS2805_0200_TestCases):
    def runTest(self):

        iso_resp = AS2805(debug=False)

        iso_resp.setMTI('0200')
        iso_resp.setBit(3, '011000')
        iso_resp.setBit(4, '000000002000')
        iso_resp.setBit(7, '0107234721')
        iso_resp.setBit(11, '000506')
        iso_resp.setBit(12, '104721')
        iso_resp.setBit(13, '0108')
        iso_resp.setBit(15, '0108')
        iso_resp.setBit(18, '5811')
        iso_resp.setBit(22, '021')
        iso_resp.setBit(25, '41')
        iso_resp.setBit(28, 'D00000200')
        iso_resp.setBit(32, '560258')
        iso_resp.setBit(35, '5188680100002932D15122015076719950000')
        iso_resp.setBit(37, '500810470506')
        iso_resp.setBit(41, 'S9218163')
        iso_resp.setBit(42, '437586000      ')
        iso_resp.setBit(43, '800 LANGDON ST,          MADISON      AU')
        iso_resp.setBit(47, 'TCC01\\EFC00000000\\CCI0\\FBKV\\')
        iso_resp.setBit(52, 'A8FB4E47EACB0FA1')
        iso_resp.setBit(53, '0000000000000002')
        iso_resp.setBit(57, '000000000000')
        iso_resp.setBit(64, '29365A0400000000')


        host_iso = iso_resp.getNetworkISO()

        self.assertEqual(host_iso[4:].encode('hex'), self.Switch_Request, 'Message is not a Match')


class Default_0210UnPackTestCase(AS2805_0200_TestCases):
    def runTest(self):

        print "Switch 0810 Test"

        iso_resp = AS2805(debug=False)
        iso_resp.setNetworkISO(HexToByte('ffffffff' + self.Host_Response))
        host_iso = iso_resp.getNetworkISO()

        self.assertEqual(host_iso[4:].encode('hex'), self.Host_Response, 'Message is not a Match')



"""
class Default_0200EMVPackTestCase(AS2805_0200_TestCases):
    def runTest(self):
        self.assertEqual(11, (50,50), 'incorrect default size')

class Default_0210EMVUnPackTestCase(AS2805_0200_TestCases):
    def runTest(self):
        self.assertEqual(111, (100,150), 'wrong size after resize')
        
"""
           # Reversals Test Cases
"""
class AS2805_0420_TestCases(unittest.TestCase):
    def setUp(self):
        self.AS205 = AS2805()
        self.Host_Request = ""
        self.Host_Response = "02103222001182c008810110000000000020000107235208000518010844000002000656025808611000163030533932313831363354594d4520202020202020202020200000000000000001000000000000409d77ee00000000"
        self.Switch_Request = ""
        self.Switch_Request = "0200323e469128e21a81011000000000002000010723514400051810514401081512010860110051000041440000020006560258375188680100002932d15122015076719950000f353030383130353130353138533932313831363354594d452020202020202020202020383030204c414e47444f4e2053542c202020202020202020204d414449534f4e202020202020415530323854434330375c45464330303030303030305c434349305c46424b565ca8fb4e47eacb0fa1000000000000000200949f02060000000020009f03060000000000009f1a020036950500000000005f2a0200369a031501089c01019f37044dff3952820200009f360200069f3303e0e0809f2701809f2608433b5fdbbc5847fa5f3401009f34030103029f3501220000000000008e7200f000000000"

class Default_0420PackTestCase(AS2805_0420_TestCases):
    def runTest(self):
        self.assertEqual(11, (50,50), 'incorrect default size')

class Default_0430UnPackTestCase(AS2805_0420_TestCases):
    def runTest(self):
        self.assertEqual(111, (100,150), 'wrong size after resize')


"""
            #Link Recon Test Cases
"""

class AS2805_0520_TestCases(unittest.TestCase):
    def setUp(self):
        self.AS205 = AS2805()
        self.Host_Request = ""
        self.Host_Response = "02103222001182c008810110000000000020000107235208000518010844000002000656025808611000163030533932313831363354594d4520202020202020202020200000000000000001000000000000409d77ee00000000"
        self.Switch_Request = ""
        self.Switch_Request = "0200323e469128e21a81011000000000002000010723514400051810514401081512010860110051000041440000020006560258375188680100002932d15122015076719950000f353030383130353130353138533932313831363354594d452020202020202020202020383030204c414e47444f4e2053542c202020202020202020204d414449534f4e202020202020415530323854434330375c45464330303030303030305c434349305c46424b565ca8fb4e47eacb0fa1000000000000000200949f02060000000020009f03060000000000009f1a020036950500000000005f2a0200369a031501089c01019f37044dff3952820200009f360200069f3303e0e0809f2701809f2608433b5fdbbc5847fa5f3401009f34030103029f3501220000000000008e7200f000000000"

class Default_0520PackTestCase(AS2805_0520_TestCases):
    def runTest(self):
        self.assertEqual(11, (50,50), 'incorrect default size')

class Default_0530UnPackTestCase(AS2805_0520_TestCases):
    def runTest(self):
        self.assertEqual(111, (100,150), 'wrong size after resize')

"""