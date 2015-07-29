__author__ = 'root'
__author__ = 'arthurvandermerwe'

import struct
import binascii
import string

from Data_Structures.AS2805_Structs.AS2805Errors import *
from Shared.ByteUtils import HexToByte, ByteToHex


class AS2805:
    #Attributes
    # Bits to be set 00000000 -> _BIT_POSITION_1 ... _BIT_POSITION_8
    _BIT_POSITION_1 = 128 # 10 00 00 00
    _BIT_POSITION_2 = 64 # 01 00 00 00
    _BIT_POSITION_3 = 32 # 00 10 00 00
    _BIT_POSITION_4 = 16 # 00 01 00 00
    _BIT_POSITION_5 = 8 # 00 00 10 00
    _BIT_POSITION_6 = 4 # 00 00 01 00
    _BIT_POSITION_7 = 2 # 00 00 00 10
    _BIT_POSITION_8 = 1 # 00 00 00 01

    #Array to translate bit to position
    _TMP = [0, _BIT_POSITION_8, _BIT_POSITION_1, _BIT_POSITION_2, _BIT_POSITION_3, _BIT_POSITION_4, _BIT_POSITION_5,
            _BIT_POSITION_6, _BIT_POSITION_7]
    _EMPTY_VALUE = 0


    #2805 contants
    _DEF = {}
    # Every _DEF has:
    # _DEF[N] = [X, Y, Z, W, K, P, Q, W]
    # N = bitnumber
    # X = smallStr representation of the bit meanning
    # Y = large str representation
    # Z = length indicator of the bit (F, LL, LLL, LLLL, LLLLL, LLLLLL)
    # W = size of the information
    # K = type of values a, an, ans, as, b, ns, s, x, z, this is also the type of the length indicator
    # P = format of the message
    """
    Type	Meaning
    'b'	Binary format. Outputs the number in base 2.
    'c'	Character. Converts the integer to the corresponding unicode character before printing.
    'd'	Decimal Integer. Outputs the number in base 10.
    'o'	Octal format. Outputs the number in base 8.
    'x'	Hex format. Outputs the number in base 16, using lower- case letters for the digits above 9.
    'X'	Hex format. Outputs the number in base 16, using upper- case letters for the digits above 9.
    'n'	Number. This is the same as 'd', except that it uses the current locale setting to insert the appropriate number separator characters.
     None	The same as 'd'.
    """
    # Q = padding of the message - 0 / F or none
    # W = justification, left / right or none
    _DEF[1] = ['BM', 'Bit Map Extended',                         'b',    '8']
    _DEF[2] = ['2', 'Primary Account Number (PAN)',              'n', '..19']
    _DEF[3] = ['3', 'Processing Code',                           'n',    '6']
    _DEF[4] = ['4', 'Amount Transaction',                        'n',   '12']
    _DEF[5] = ['5', 'Amount Settlement',                         'n',   '12']
    _DEF[6] = ['6', 'Amount Cardholder Billing',                 'n',   '12']
    _DEF[7] = ['7', 'Transmission Date and Time',                'n',   '10']
    _DEF[8] = ['8', 'Amount Cardholder Billing Fee',             'n',    '8']
    _DEF[9] = ['9', 'Conversion Rate, Settlement',               'n',    '8']
    _DEF[10] = ['10', 'Conversion Rate, Cardholder Billing',     'n',    '8']
    _DEF[11] = ['11', 'Systems Trace Audit Number',              'n',    '8']
    _DEF[12] = ['12', 'Time, Local Transaction',                 'n',    '6']
    _DEF[13] = ['13', 'Date, Local Transaction',                 'n',    '4']
    _DEF[14] = ['14', 'Date, Expiration',                        'n',    '4']
    _DEF[15] = ['15', 'Date, Settlement',                        'n',    '4']
    _DEF[16] = ['16', 'Date, Conversion',                        'n',    '4']
    _DEF[17] = ['17', 'Date, Capture',                           'n',    '4']
    _DEF[18] = ['18', 'Merchant Type',                           'n',    '4']
    _DEF[19] = ['19', 'Acquiring Institution Country Code',      'n',    '3']
    _DEF[20] = ['20', 'PAN Extended Country Code',               'n',    '3']
    _DEF[21] = ['21', 'Forwarding Institution Country Code',     'n',    '3']
    _DEF[22] = ['22', 'POS Entry Mode',                          'n',    '3']
    _DEF[23] = ['23', 'Card Sequence Number',                    'n',    '3']
    _DEF[24] = ['24', 'International Identifier',                'n',    '3']
    _DEF[25] = ['25', 'POS Condition Code',                      'n',    '2']
    _DEF[26] = ['26', 'POS PIN Capture Code',                    'n',    '2']
    _DEF[27] = ['27', 'Auth ID Response Length',                 'n',    '1']
    _DEF[28] = ['28', 'Amount, Transaction Fee',               'x+n',    '9']
    _DEF[29] = ['29', 'Amount, Settlement Fee',                'x+n',    '9']
    _DEF[30] = ['30', 'Amount, Processing Fee',                'x+n',    '9']
    _DEF[31] = ['31', 'Amount, Settlement Processing Fee',     'x+n',    '9']
    _DEF[32] = ['32', 'Acquiring Institution ID Code',          'n',  '..11']
    _DEF[33] = ['33', 'Forwarding Institution ID Code',         'n',  '..11']
    _DEF[34] = ['34', 'PAN Extended'                            'ns', '..28']
    _DEF[35] = ['35', 'Track 2 Data',                           'z',  '..37']
    _DEF[36] = ['36', 'Track 3 Data',                           'z','...104']
    _DEF[37] = ['37', 'Retrieval Reference Number',            'an',    '12']
    _DEF[38] = ['38', 'Authorization ID Response',             'an',     '6']
    _DEF[39] = ['39', 'Response Code',                         'an',     '2']
    _DEF[40] = ['40', 'Service Restriction Code',              'an',     '3']
    _DEF[41] = ['41', 'Card Acceptor Terminal ID',             'an',     '8']
    _DEF[42] = ['42', 'Card Acceptor ID Code',                 'ans',   '15']
    _DEF[43] = ['43', 'Card Acceptor Name Location',           'ans',   '40']
    _DEF[44] = ['44', 'Additional Response Data',              'ans', '..25']
    _DEF[45] = ['45', 'Track 1 Data',                          'ans', '..76']
    _DEF[46] = ['46', 'Additional  Data ISO ',                'ans','...999']
    _DEF[47] = ['47', 'Additional Data National',             'ans','...999']
    _DEF[48] = ['48', 'Additional Data Private',              'ans','...999']
    _DEF[49] = ['49', 'Currency Code, Transaction',              'n',    '3']
    _DEF[50] = ['50', 'Currency Code, Settlement',               'n',    '3']
    _DEF[51] = ['51', 'Currency Code, Billing',                  'n',    '3']
    _DEF[52] = ['52', 'PIN Data',                                'b',   '16']
    _DEF[53] = ['53', 'Security Related Control Information',    'n',   '16']
    _DEF[54] = ['54', 'Additional Amounts',                    'an','...120']
    _DEF[55] = ['55', 'ICC Data',                               'b','...999']
    _DEF[57] = ['57', 'Amount Cash',                            'n',    '12']
    _DEF[58] = ['58', 'Ledger Balance',                         'n',    '12']
    _DEF[59] = ['59', 'Account Balance',                        'n',    '12']
    _DEF[64] = ['64', 'Message Authentication Code',            'b',    '16']
    _DEF[66] = ['66', 'Settlement Code',                         'n',    '1']
    _DEF[67] = ['67', 'Extended Payment Code',                   'n',    '2']
    _DEF[68] = ['68', 'Receiving Institution Country Code',      'n',    '3']
    _DEF[69] = ['69', 'Settlement Institution Country Code',     'n',    '3']
    _DEF[70] = ['70', 'Network Management Information Code',     'n',    '3']
    _DEF[71] = ['71', 'Message Number',                          'n',    '4']
    _DEF[72] = ['72', 'Message Number Last',                     'n',    '4']
    _DEF[73] = ['73', 'Date Action',                             'n',    '6']
    _DEF[74] = ['74', 'Credits, Number',                         'n',   '10']
    _DEF[75] = ['75', 'Credits, Reversal Number',                'n',   '10']
    _DEF[76] = ['76', 'Debits, Number',                          'n',   '10']
    _DEF[77] = ['77', 'Debits, Reversal Number',                 'n',   '10']
    _DEF[78] = ['78', 'Transfer, Number',                        'n',   '10']
    _DEF[79] = ['79', 'Transfer, Reversal Number',               'n',   '10']
    _DEF[80] = ['80', 'Inquiries, Number',                       'n',   '10']
    _DEF[81] = ['81', 'Authorizations, Number',                  'n',   '10']
    _DEF[82] = ['82', 'Credits, Processing Fee Amount',          'n',   '12']
    _DEF[83] = ['83', 'Credits, Transaction Fee Amount',         'n',   '12']
    _DEF[84] = ['84', 'Debits, Processing Fee Amount',           'n',   '12']
    _DEF[85] = ['85', 'Debits, Transaction Fee Amount',          'n',   '12']
    _DEF[86] = ['86', 'Credits, Amount',                         'n',   '16']
    _DEF[87] = ['87', 'Credits, Reversal Amount',                'n',   '16']
    _DEF[88] = ['88', 'Debits, Amount',                          'n',   '16']
    _DEF[89] = ['89', 'Debits, Reversal Amount',                 'n',   '16']
    _DEF[90] = ['90', 'Original Data Elements',                  'n',   '42']
    _DEF[91] = ['91', 'File Update Code',                        'an',   '1']
    _DEF[92] = ['92', 'File Security Code',                      'an',   '2']
    _DEF[93] = ['93', 'Response Indicator',                      'an',   '5']
    _DEF[94] = ['94', 'Service Indicator',                       'an',   '7']
    _DEF[95] = ['95', 'Replacement Amounts',                     'an',  '42']
    _DEF[96] = ['96', 'Message Security Code',                   'b',   '64']
    _DEF[97] = ['97', 'Amount, Net Settlement',                  'x+n', '16']
    _DEF[98] = ['98', 'Payee'                                   'ans','..25']
    _DEF[99] = ['99', 'Settlement Institution ID Code',          'n', '..11']
    _DEF[100] = ['100', 'Receiving Institution ID Code',         'n', '..11']
    _DEF[101] = ['101', 'File Name',                            'ans','..17']
    _DEF[102] = ['102', 'Account Identification 1',             'ans','..28']
    _DEF[103] = ['103', 'Account Identification 2',             'ans','..28']
    _DEF[104] = ['104', 'Transaction Description',            'ans','...100']
    _DEF[112] = ['112', 'Key Management Data',                 'b', '...999']
    _DEF[117] = ['117', 'Card Status Update Code',              'an',    '2']
    _DEF[118] = ['118', 'Cash Total Number',                     'n',   '10']
    _DEF[119] = ['119', 'Cash Total Amount',                     'n',   '16']
    _DEF[128] = ['128',  'MAC Extended',                         'b',   '16']


    def __init__(self, iso="", debug=False):
        """Default Constructor of AS2805 Package.
        It initialize a "brand new" AS2805 package
        Example: To Enable debug you can use:
        pack = AS2895(debug=True)
        @param: iso a String that represents the ASCII of the package. The same that you need to pass to setIsoContent() method.
        @param: debug (True or False) default False -> Used to print some debug infos. Only use if want that messages!
        """
        #Bitmap internal representation
        self.BITMAP = []

        #Values
        self._VALUES = []

        #Bitmap ASCII representantion
        self.BITMAP_HEX = ''

        # MTI
        self.MESSAGE_TYPE_INDICATION = ''
        #Debug ?
        self.DEBUG = debug

        self.__initializeBitmap()
        self.__initializeValues()

        if iso != "":
            self.setIsoContent(iso)

    ################################################################################################

    def getLengthType(self, bit):
        """Method that return the bit Type
        @param: bit -> Bit that will be searched and whose type will be returned
        @return: str that represents the type of the bit
        """
        return self._DEF[bit][2]

    ################################################################################################

    def getMaxLength(self, bit):
        """Method that return the bit limit (Max size)
        @param: bit -> Bit that will be searched and whose limit will be returned
        @return: int that indicate the limit of the bit
        """
        return self._DEF[bit][3]

    ################################################################################################


    def getBitName(self, bit):
        """Method that return the large bit name
        @param: bit -> Bit that will be searched and whose name will be returned
        @return: str that represents the name of the bit
        """
        return self._DEF[bit][1]

    ################################################################################################

    def setTransationType(self, type):
        """Method that set Transation Type (MTI)
        @param: type -> MTI to be setted
        """

        self.MESSAGE_TYPE_INDICATION = ("0000%s" % type)[-4:]

    ################################################################################################

    def setMTI(self, type):
        """Method that set Transation Type (MTI)
        In fact, is an alias to "setTransationType" method
        @param: type -> MTI to be setted
        """
        self.setTransationType(type)

    ################################################################################################

    def __initializeBitmap(self):
        """Method that inicialize/reset a internal bitmap representation
        It's a internal method, so don't call!
        """

        if self.DEBUG:
            print 'Init bitmap'

        if len(self.BITMAP) == 16:
            for cont in range(0, 16):
                self.BITMAP[cont] = self._EMPTY_VALUE
        else:
            for cont in range(0, 16):
                self.BITMAP.append(self._EMPTY_VALUE)


                ################################################################################################

    def __initializeValues(self):
        """Method that inicialize/reset a internal array used to save bits and values
        It's a internal method, so don't call!
        """
        if self.DEBUG:
            print 'Init bitmap_values'

        if len(self._VALUES) == 129:
            for cont in range(0, 129):
                self._VALUES[cont] = self._EMPTY_VALUE
        else:
            for cont in range(0, 129):
                self._VALUES.append(self._EMPTY_VALUE)



    def __get_AS2805_Valiable_Length_Prefix(self, bit):

        Length_Indicator = str(self._DEF[bit][3])









                ################################################################################################

    def setBit(self, bit, value):
        """Method used to set a bit with a value.
        It's one of the most important method to use when using this library
        @param: bit -> bit number that want to be setted
        @param: value -> the value of the bit
        @return: True/False default True -> To be used in the future!
        @raise: BitInexistent Exception, ValueToLarge Exception
        """



        if bit < 1 or bit > 129:
            raise BitInexistent("Bit number %s dosen't exist!" % bit)

        if self.DEBUG:
            print 'Setting Bit %s (%s) = [%s]' % (bit, self.getBitName(bit), ReadableAscii(value))

        Length_Indicator = str(self._DEF[bit][3]).count('.')

        if Length_Indicator == 0:
            self.__setBitFixedLength(bit, value)
        else:
            self.__setBitVariableLength(bit, value)

        if self.DEBUG:
            print 'Bit was set to %s (%s) = [%s]' % (bit, self.getBitName(bit), str(self._VALUES[bit]))



        #Continuation bit?
        if bit > 64:
            self.BITMAP[0] |= self._TMP[2]  # need to set bit 1 of first "bit" in bitmap

        if (bit % 8) == 0:
            pos = (bit / 8) - 1
        else:
            pos = (bit / 8)

        #need to check if the value can be there .. AN , N ... etc ... and the size

        self.BITMAP[pos] |= self._TMP[(bit % 8) + 1]

        return True

        ################################################################################################

    def showBitmap(self):
        """Method that print the bitmap in ASCII form
        Hint: Try to use getBitmap method and format your own print :)
        """

        self.__buildBitmap()

        # printing
        print self.BITMAP_HEX

    ################################################################################################

    def __buildBitmap(self):
        """Method that build the bitmap ASCII
        It's a internal method, so don't call!
        """

        self.BITMAP_HEX = ''
        self.BITMAP_BIN = ''

        for c in range(0, 16):
            if (self.BITMAP[0] & self._BIT_POSITION_1) != self._BIT_POSITION_1:
            # Only has the first bitmap
            #				if self.DEBUG == True:
            #					print '%d Bitmap = %d(Decimal) = %s (hexa) ' %(c, self.BITMAP[c], hex(self.BITMAP[c]))

                tm = hex(self.BITMAP[c])[2:]
                if len(tm) != 2:
                    tm = '0' + tm
                self.BITMAP_HEX += tm
                self.BITMAP_BIN += chr(self.BITMAP[c])
                if c == 7:
                    break
            else: # second bitmap
            #				if self.DEBUG == True:
            #					print '%d Bitmap = %d(Decimal) = %s (hexa) ' %(c, self.BITMAP[c], hex(self.BITMAP[c]))

                tm = hex(self.BITMAP[c])[2:]
                if len(tm) != 2:
                    tm = '0' + tm
                self.BITMAP_HEX += tm
                self.BITMAP_BIN += chr(self.BITMAP[c])


    ################################################################################################

    def __getBitmapFromStr(self, bitmap):
            """Method that receive a bitmap str and transfor it to ISO8583 object readable.
            @param: bitmap -> bitmap str to be readable
            It's a internal method, so don't call!
            """
            #Need to check if the size is correct etc...
            cont = 0

            if self.BITMAP_HEX != '':
                    self.BITMAP_HEX = ''

            for x in range(0,32,2):
                    if (int(bitmap[0:2],16) & self._BIT_POSITION_1) != self._BIT_POSITION_1: # Only 1 bitmap
                            if self.DEBUG:
                                    print 'Token[%d] %s converted to int is = %s' %(x, bitmap[x:x+2], int(bitmap[x:x+2],16))

                            self.BITMAP_HEX += bitmap[x:x+2]
                            self.BITMAP[cont] = int(bitmap[x:x+2],16)
                            if x == 14:
                                    break
                    else: # Second bitmap
                            if self.DEBUG:
                                    print 'Token[%d] %s converted to int is = %s' %(x, bitmap[x:x+2], int(bitmap[x:x+2],16))

                            self.BITMAP_HEX += bitmap[x:x+2]
                            self.BITMAP[cont] = int(bitmap[x:x+2],16)
                    cont += 1


    ################################################################################################

    def showBitsFromBitmapStr(self, bitmap):
        """Method that receive a bitmap str, process it, and print a array with bits this bitmap string represents.
        Usualy is used to debug things.
        @param: bitmap -> bitmap str to be analized and translated to "bits"
        """
        bits = self.__initializeBitsFromBitmapStr()
        print 'Bits inside %s  = %s' % (bitmap, bits)

    ################################################################################################

    def __initializeBitsFromBitmapStr(self):
        """Method that receive a bitmap str, process it, and prepare AS2805 object to understand and "see" the bits and values inside the ISO ASCII package.
        It's a internal method, so don't call!
        @param: bitmap -> bitmap str to be analized and translated to "bits"
        """
        bits = []
        for c in range(0, 16):
            for d in range(1, 9):
                #if self.DEBUG == True:
                #print 'Value (%d)-> %s & %s = %s' % (d,self.BITMAP[c] , self._TMP[d], (self.BITMAP[c] & self._TMP[d]) )
                if (self.BITMAP[c] & self._TMP[d]) == self._TMP[d]:
                    if d == 1: #  e o 8 bit
                        if self.DEBUG:
                            print 'Bit %s is present !!!' % ((c + 1) * 8)
                        bits.append((c + 1) * 8)
                        self._VALUES[(c + 1) * 8] = 'X'
                    else:
                        if (c == 0) & (d == 2): # Continuation bit
                            if self.DEBUG:
                                print 'Bit 1 is present !!!'

                            bits.append(1)

                        else:
                            if self.DEBUG:
                                print 'Bit %s is present !!!' % (c * 8 + d - 1)

                            bits.append(c * 8 + d - 1)
                            self._VALUES[c * 8 + d - 1] = 'X'

        bits.sort()

        return bits

    ################################################################################################

    def __getBitsFromBitmap(self):
        """Method that process the bitmap and return a array with the bits presents inside it.
        It's a internal method, so don't call!
        """
        bits = []
        for c in range(0, 16):
            for d in range(1, 9):
            #				if self.DEBUG == True:
            #					print 'Value (%d)-> %s & %s = %s' % (d,self.BITMAP[c] , self._TMP[d], (self.BITMAP[c] & self._TMP[d]) )
                if (self.BITMAP[c] & self._TMP[d]) == self._TMP[d]:
                    if d == 1: #  e o 8 bit
                        if self.DEBUG:
                            print 'Bit %s is present !!!' % ((c + 1) * 8)

                        bits.append((c + 1) * 8)
                    else:
                        if (c == 0) & (d == 2): # Continuation bit
                            if self.DEBUG:
                                print 'Bit 1 is present !!!'

                            bits.append(1)

                        else:
                            if self.DEBUG:
                                print 'Bit %s is present !!!' % (c * 8 + d - 1)

                            bits.append(c * 8 + d - 1)

        bits.sort()

        return bits

    ################################################################################################

    def __setBitVariableLength(self, bit, value):

        value_data = self.__set_Octet_Data(value)
        length_data = self.__setLengthIndicator(bit, len(value_data))

        self._VALUES[bit] = "%s%s" % (length_data, value_data)
        #print "Setting Bits: " + self._VALUES[bit] + " type: " + type + " Variable"



    def __setLengthIndicator(self, bit, length):
        if (str(self._DEF[bit][3]).count('.') == 3) and  (self._DEF[bit][2] == 'b'):#0LLL 2 octets
            return str(length).zfill(2).encode('hex')

        elif (str(self._DEF[bit][3]).count('.') == 3) and  (self._DEF[bit][2] == 'n' or self._DEF[bit][2] == 'z'): #0LLL 2 octets
            return str(length).zfill(2).encode('hex')

        elif (str(self._DEF[bit][3]).count('.') == 3) and (self._DEF[bit][2] == 'a' or self._DEF[bit][2] == 'ans' or self._DEF[bit][2] == 'ns' or self._DEF[bit][2] == 'x'): #LLL 3 octets
            return str(length).zfill(3).encode('hex')

        elif (str(self._DEF[bit][3]).count('.') == 2) and  (self._DEF[bit][2] == 'n' or self._DEF[bit][2] == 'z'): #LL 2 octets
            return str(length).zfill(2).encode('hex')

        elif (str(self._DEF[bit][3]).count('.') == 2) and (self._DEF[bit][2] == 'a' or self._DEF[bit][2] == 'ans' or self._DEF[bit][2] == 'ns' or self._DEF[bit][2] == 'x'): #LL 2 octets
            return str(length).zfill(2).encode('hex')


    def __set_Octet_Data(self, value):
        return str(value).encode('hex')





    def __setBitFixedLength(self, bit, value):
        result = self.__set_Octet_Data(value)
        #bit_limit = int(self.getMaxLength(bit))
        self._VALUES[bit] = result


    ################################################################################################

    def dumpFields(self):
        """Method that show in detail a list of bits , values and types inside the object
        Example: output to
            (...)
            iso.setBit(2,2)
            iso.setBit(4,4)
            (...)
            iso.showIsoBits()
            (...)
            Bit[2] of type LL has limit 19 = 012
            Bit[4] of type N has limit 12 = 000000000004
            (...)
        """
        res = '\n%s:\n' % self.MESSAGE_TYPE_INDICATION

        for bit in range(0, 129):
            if self._VALUES[bit] <> self._EMPTY_VALUE:

                res += " [%s] " % bit
                res += " [%s%s ] " % (self._DEF[bit][2], self._DEF[bit][3])
                res += " [%s] " % ReadableAscii(self.getBit(bit))
                res += self.getBitName(bit)
                res += '\n'

                #print res

        return res

        ################################################################################################

    def showRawIso(self):
        """Method that print AS2805 ASCII complete representation
        Example:
        iso = AS2805()
        iso.setMTI('0800')
        iso.setBit(2,2)
        iso.setBit(4,4)
        iso.setBit(12,12)
        iso.setBit(17,17)
        iso.setBit(99,99)
        iso.showRawIso()
        output (print) -> 0800d010800000000000000000002000000001200000000000400001200170299
        Hint: Try to use getRawIso method and format your own print :)
        """

        resp = self.getRawIso()
        print resp

    ################################################################################################

    def getRawIso(self):
        """Method that return AS2805 ASCII complete representation
        Example:
        iso = AS2805()
        iso.setMTI('0800')
        iso.setBit(2,2)
        iso.setBit(4,4)
        iso.setBit(12,12)
        iso.setBit(17,17)
        iso.setBit(99,99)
        str = iso.getRawIso()
        print 'This is the ASCII package %s' % str
        output (print) -> This is the ASCII package 0800d010800000000000000000002000000001200000000000400001200170299

        @return: str with complete ASCII AS2805
        @raise: InvalidMTI Exception
        """

        self.__buildBitmap()

        if self.MESSAGE_TYPE_INDICATION == '':
            raise InvalidMTI('Check MTI! Do you set it?')

        resp = ""

        resp += self.MESSAGE_TYPE_INDICATION
        resp += binascii.hexlify(self.BITMAP_BIN)

        for cont in range(0, 129):
            if self._VALUES[cont] <> self._EMPTY_VALUE:
                resp = "%s%s" % (resp, self._VALUES[cont])

        return resp

    ################################################################################################


    def __setMTIFromStr(self, iso):
        """Method that get the first 4 characters to be the MTI.
         It's a internal method, so don't call!
         """
        if self.DEBUG:
            print '__setMTIFromStr(%s)' % ReadableAscii(iso)

        self.MESSAGE_TYPE_INDICATION = iso[0:4]

        if self.DEBUG:
            print 'MTI found was [%s]' % self.MESSAGE_TYPE_INDICATION

            ################################################################################################

    def getMTI(self):
        """Method that return the MTI of the package
        @return: str -> with the MTI
        """

        #Need to validate if the MTI was setted ...etc ...
        return self.MESSAGE_TYPE_INDICATION

    ################################################################################################

    def getBitmap(self):
        """Method that return the ASCII Bitmap of the package
        @return: str -> with the ASCII Bitmap
        """
        if self.BITMAP_HEX == '':
            self.__buildBitmap()

        return self.BITMAP_HEX

    ################################################################################################

    def getValuesArray(self):
        """Method that return an internal array of the package
        @return: array -> with all bits, presents or not in the bitmap
        """
        return self._VALUES

    ################################################################################################

    def __getBitFromStr(self, strWithoutMtiBitmap):
        """Method that receive a string (ASCII) without MTI and Bitmaps (first and second), understand it and remove the bits values
        @param: str -> with all bits presents whithout MTI and bitmap
        It's a internal method, so don't call!
        """

        if self.DEBUG:
            print '__getBitFromStr(%s)' % ReadableAscii(strWithoutMtiBitmap)





        offset = 0
        # jump bit 1 because it was alread defined in the "__initializeBitsFromBitmapStr"
        for cont in range(2, 129):
            if self._VALUES[cont] <> self._EMPTY_VALUE:
                if self.DEBUG:
                    print 'String = %s offset = %s bit = %s' % (strWithoutMtiBitmap[offset:], offset, cont)

                if cont == 55:
                    pass

                #valiable length field
                if str(self._DEF[cont][3]).count('.') > 0:
                    valueSize = 0

                    if (str(self._DEF[cont][3]).count('.') == 3)   and  (self._DEF[cont][2] == 'b'):#0LLL 2 octets
                        lengthIndicator = 4

                    elif (str(self._DEF[cont][3]).count('.') == 3) and  (self._DEF[cont][2] == 'n' or self._DEF[cont][2] == 'z'): #0LLL 2 octets
                        lengthIndicator = 4

                    elif (str(self._DEF[cont][3]).count('.') == 3) and (self._DEF[cont][2] == 'a' or self._DEF[cont][2] == 'ans' or self._DEF[cont][2] == 'ns' or self._DEF[cont][2] == 'x'): #LLL 3 octets
                        lengthIndicator = 6

                    elif (str(self._DEF[cont][3]).count('.') == 2) and  (self._DEF[cont][2] == 'n' or self._DEF[cont][2] == 'z'): #LL 2 octets
                        lengthIndicator = 4

                    elif (str(self._DEF[cont][3]).count('.') == 2) and (self._DEF[cont][2] == 'a' or self._DEF[cont][2] == 'ans' or self._DEF[cont][2] == 'ns' or self._DEF[cont][2] == 'x'): #LL 2 octets
                        lengthIndicator = 4




                    if valueSize > self.getMaxLength(cont):
                        raise ValueToLarge("This bit is larger than the specification!")

                    valueSize = int(binascii.unhexlify(strWithoutMtiBitmap[offset:offset + lengthIndicator]))
                    #valueSize *= 2

                    if self.DEBUG:
                        print 'Variable Length Field (%s) Size = [%s]' % ('L' * lengthIndicator, valueSize / 2)


                    if valueSize > self.getMaxLength(cont):
                        raise ValueToLarge("This bit is larger than the specification!")


                    self._VALUES[cont] = strWithoutMtiBitmap[offset:offset + lengthIndicator] + strWithoutMtiBitmap[offset + lengthIndicator:offset + lengthIndicator + valueSize]

                    if self.DEBUG:
                        print '\tSetting bit [%s] Value=[%s]' % (cont, binascii.unhexlify(self._VALUES[cont]))
                    offset += valueSize + lengthIndicator

                #fixed length field
                else:

                    length = int(self.getMaxLength(cont))

                    length *= 2
                    new_offset = length + offset

                    self._VALUES[cont] = strWithoutMtiBitmap[offset: new_offset]
                    offset += length


                    if self.DEBUG:
                        print 'Fixed Length Field Size = [%s]' % (length / 2)
                        print '\tSetting bit [%s] Value=[%s]' % (cont, binascii.unhexlify(str(self._VALUES[cont])))


                    ################################################################################################

    def setIsoContent(self, iso):

        if len(iso) < 20:
            raise InvalidAS2805('This is not a valid iso!!')
        if self.DEBUG:
            print 'ASCII to process <%s>' % iso

        self.__setMTIFromStr(iso)
        isoT = iso[4:]
        self.__getBitmapFromStr(isoT)
        self.__initializeBitsFromBitmapStr()
        if self.DEBUG:
            print 'This is the array of bits (before) %s ' % self._VALUES

        self.__getBitFromStr(iso[4+len(self.BITMAP_HEX):])
        if self.DEBUG:
            print 'This is the array of bits (after) %s ' % self._VALUES

            ################################################################################################

    def getBitsAndValues(self):

        ret = []
        for cont in range(2, 126):
            if self._VALUES[cont] != self._EMPTY_VALUE:
                _TMP = {'bit': "%d" % cont, 'type': self.getLengthType(cont), 'value': self.getBit(cont), 'format': self.getDataType(cont)}
                #print _TMP
                ret.append(_TMP)
        return ret

    ################################################################################################

    def getBit(self, bit):


        if bit < 1 or bit > 128:
            raise BitInexistent("Bit number %s dosen't exist!" % bit)

        if self._VALUES[bit] == self._EMPTY_VALUE:
            raise BitNotSet("Bit number %s was not set!" % bit)

        if (str(self._DEF[bit][3]).count('.') == 3) and  (self._DEF[bit][2] == 'b'):#0LLL 2 octets
            value = binascii.unhexlify(self._VALUES[bit][4:])

        elif (str(self._DEF[bit][3]).count('.') == 3) and  (self._DEF[bit][2] == 'n' or self._DEF[bit][2] == 'z'): #0LLL 2 octets
            value = binascii.unhexlify(self._VALUES[bit][4:])

        elif (str(self._DEF[bit][3]).count('.') == 3) and (self._DEF[bit][2] == 'a' or self._DEF[bit][2] == 'ans' or self._DEF[bit][2] == 'ns' or self._DEF[bit][2] == 'x'): #LLL 3 octets
            value = binascii.unhexlify(self._VALUES[bit][6:])

        elif (str(self._DEF[bit][3]).count('.') == 2) and  (self._DEF[bit][2] == 'n' or self._DEF[bit][2] == 'z'): #LL 2 octets
            value = binascii.unhexlify(self._VALUES[bit][4:])

        elif (str(self._DEF[bit][3]).count('.') == 2) and (self._DEF[bit][2] == 'a' or self._DEF[bit][2] == 'ans' or self._DEF[bit][2] == 'ns' or self._DEF[bit][2] == 'x'): #LL 2 octets
            value = binascii.unhexlify(self._VALUES[bit][4:])

        else:
            value =   binascii.unhexlify(self._VALUES[bit])

        return value

    ################################################################################################

    def getNetworkISO(self, bigEndian=True):


        asciiIso = self.getRawIso()

        if bigEndian:
            netIso = struct.pack('!H', len(asciiIso))
            if self.DEBUG:
                print 'Pack Big-endian'
        else:
            netIso = struct.pack('<H', len(asciiIso))
            if self.DEBUG:
                print 'Pack Little-endian'

        netIso += asciiIso

        return netIso

    ################################################################################################

    """
    determine if the given string is hex
    """
    @staticmethod
    def __isStringHex(s):
        return all(c in string.hexdigits for c in s)

    ################################################################################################
    def setNetworkISO(self, iso, bigEndian=True):

        if len(iso) < 24:
            raise InvalidAS2805('This is not a valid iso!!Invalid Size')

        size = iso[0:2]
        if bigEndian:
            if self.DEBUG:
                print 'Unpack Big-endian'
        else:
            if self.DEBUG:
                print 'Unpack Little-endian'

        #if len(iso) != (size[0] + 2):
        #    raise InvalidAS2805('This is not a valid iso!!The AS2805 ASCII(%s) is less than the size %s!' % (len(iso[2:]), size[0]))

        self.setIsoContent(iso)

################################################################################################


def ReadableAscii(s):
    """
    Print readable ascii string, non-readable characters are printed as periods (.)
    """
    r = ''
    for c in s:
        if 32 <= ord(c) <= 126:
            r += c
        else:
            r += '.'
    return r

################################################################################################


def BinaryDump(s):
    """
    Returns a hexdump in postilion trace format. It also removes the leading tcp length indicator

    0000(0000)  30 32 31 30 F2 3E 44 94  2F E0 84 20 00 00 00 00   0210.>D./.. ....
    0016(0010)  04 00 00 22 31 36 2A 2A  2A 2A 2A 2A 2A 2A 2A 2A   ..."16**********
    0032(0020)  2A 2A 2A 2A 2A 2A 30 31  31 30 30 30 30 30 30 30   ******0110000000
    0048(0030)  30 30 30 35 30 30 30 30  31 30 30 34 30 36 34 30   0005000010040640
    ...
    0576(0240)  36 3C 2F 44 61 74 61 3E  3C 2F 52 65 74 72 69 65   6</Data></Retrie
    0592(0250)  76 61 6C 52 65 66 4E 72  3E 3C 2F 42 61 73 65 32   valRefNr></Base2
    0608(0260)  34 44 61 74 61 3E								  4Data>
    """
    #Remove TCP length indicator
    s = s[2:]
    dumphex(s)


def dumphex(s):
  global i
  hex_str = ''
  str = ""
  for i in range(0,len(s)):
    if s[i] in string.whitespace:
      str += '.'
      continue
    if s[i] in string.printable:
      str = str + s[i]
      continue
    str += '.'
  bytes = map(lambda x: '%.2x' % x, map(ord, s))
  print
  for i in xrange(0,len(bytes)/16):
    hex_str +=  '    %s' % string.join(bytes[i * 16:(i + 1) * 16])
    hex_str +=  '    %s\n' % str[i*16:(i+1)*16]
  hex_str += '    %-51s' % string.join(bytes[(i + 1) * 16:])
  hex_str += '%s\n' % str[(i+1)*16:]

  return hex_str



################################################################################################

if __name__ == '__main__':
    iso = AS2805(debug=True)
    iso.setMTI('0200')
    #Set a Fixed Length Field
    iso.setBit(3, '011000')
    iso.setBit(4, '000000002000')
    iso.setBit(7, '0107235144')
    iso.setBit(11, '00000518')
    iso.setBit(12, '105144')
    iso.setBit(13, '0108')
    iso.setBit(15, '0108')
    iso.setBit(18, '6011')
    iso.setBit(22, '051')
    iso.setBit(23, '000')
    iso.setBit(25, '41')
    iso.setBit(28, 'D00000200')
    iso.setBit(32, '56025800000')
    iso.setBit(33, '61100016')
    iso.setBit(35, '5188680100002932')
    iso.setBit(37, '500810510518')
    iso.setBit(39, '00')
    iso.setBit(41, 'S9218163')
    iso.setBit(42, 'TYME           ')
    iso.setBit(43, '800 LANGDON ST,          MADISON      AU')
    iso.setBit(47, 'TCC01\\EFC00000000\\CCI0\FBKV\\')
    iso.setBit(48, '61E29E04896786B3950552E9118A655D0CD054BF3DC1E35E829C704030DBC8F6')
    iso.setBit(52, 'A8FB4E47EACB0FA1')
    iso.setBit(53, '0000000000000002')
    iso.setBit(55, '9F02060000000020009F03060000000000009')
    iso.setBit(57, 'D00000045000')

    iso.setBit(64, '29365A0400000000')
    iso.setBit(70, '301')
    iso.setBit(99, '1234567')
    iso.setBit(100, '579944')
    iso.setBit(128, '027980E700000000')


    print iso.getRawIso()

    print HexToByte(iso.getRawIso())


    print iso.dumpFields()
    print "Binary Data: \n"

    print dumphex(iso.getNetworkISO())



    iso_new = AS2805(debug=True)
    iso_new.setIsoContent(iso.getNetworkISO()[2:])
    print iso_new.dumpFields()
    print iso_new.getNetworkISO()
    another_iso = AS2805(debug=True)
    print another_iso.setIsoContent(iso_new.getNetworkISO()[2:])

    print iso_new.getBit(3)
    print iso_new.getBit(4)
    print iso_new.getBit(7)
    print iso_new.getBit(11)
    print iso_new.getBit(12)
    print iso_new.getBit(13)
    print iso_new.getBit(15)
    print iso_new.getBit(18)
    print iso_new.getBit(22)
    print iso_new.getBit(23)
    print iso_new.getBit(25)
    print iso_new.getBit(28)
    print iso_new.getBit(32)
    print iso_new.getBit(33)
    print iso_new.getBit(35)
    print iso_new.getBit(37)
    print iso_new.getBit(39)
    print iso_new.getBit(41)
    print iso_new.getBit(42)
    print iso_new.getBit(43)
    print iso_new.getBit(47)
    print iso_new.getBit(48)
    print iso_new.getBit(52)
    print iso_new.getBit(53)
    print iso_new.getBit(55)
    print iso_new.getBit(57)

    print iso_new.getBit(64)
    print iso_new.getBit(70)
    print iso_new.getBit(99)
    print iso_new.getBit(100)
    print iso_new.getBit(128)

