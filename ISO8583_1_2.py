"""

(C) Copyright 2009 Igor V. Custodio

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

__author__ = 'Igor Vitorio Custodio <igorvc@vulcanno.com.br>'
__version__ = '1.2'
__licence__ = 'GPL V3'

from ISOErrors import *
import struct


class ISO8583:
    # Attributes
    # Bitsto be set 00000000 -> _BIT_POSITION_1 ... _BIT_POSITION_8
    _BIT_POSITION_1 = 128  # 10 00 00 00
    _BIT_POSITION_2 = 64  # 01 00 00 00
    _BIT_POSITION_3 = 32  # 00 10 00 00
    _BIT_POSITION_4 = 16  # 00 01 00 00
    _BIT_POSITION_5 = 8  # 00 00 10 00
    _BIT_POSITION_6 = 4  # 00 00 01 00
    _BIT_POSITION_7 = 2  # 00 00 00 10
    _BIT_POSITION_8 = 1  # 00 00 00 01

    #Array to translate bit to position
    _TMP = [0, _BIT_POSITION_8, _BIT_POSITION_1, _BIT_POSITION_2, _BIT_POSITION_3, _BIT_POSITION_4, _BIT_POSITION_5,
            _BIT_POSITION_6, _BIT_POSITION_7]
    _BIT_DEFAULT_VALUE = 0


    """
        # Every _BITS_VALUE_TYPE has:
        # _BITS_VALUE_TYPE[N] = [ X,Y, Z, W,K]
        # N = bitnumber
        # X = smallStr representation of the bit meanning
        # Y = large str representation
        # Z = type of the bit (B, N, A, AN, ANS, LL, LLL)
        #W = size of the information that N need to has
        # K = type os values a, an, n, ansb, b
         # Every _DEF has:
        # _DEF[N] = [X, Y, Z, W, K]
        # N = bitnumber
        # X = smallStr representation of the bit meanning
        # Y = large str representation
        # Z = length indicator of the bit (F, LL, LLL, LLLL, LLLLL, LLLLLL)
        # W = size of the information that N need to has
        # K = type os values a, an, ans, n, xn, b
    """
    _BITS_VALUE_TYPE = {}
    _BITS_VALUE_TYPE[1] = ['BM', 'Bit Map Extended', 'B', 8, 'b']
    _BITS_VALUE_TYPE[2] = ['2', 'Primary Account Number (PAN)', 'LL', 19, 'n']
    _BITS_VALUE_TYPE[3] = ['3', 'Processing Code', 'N', 6, 'n']
    _BITS_VALUE_TYPE[4] = ['4', 'Amount Transaction', 'N', 12, 'n']
    _BITS_VALUE_TYPE[5] = ['5', 'Amount Settlement', 'N', 12, 'n']
    _BITS_VALUE_TYPE[7] = ['7', 'Transmission Date and Time', 'N', 10, 'n']
    _BITS_VALUE_TYPE[9] = ['9', 'Conversion Rate, Settlement', 'N', 8, 'n']
    _BITS_VALUE_TYPE[10] = ['10', 'Conversion Rate, Cardholder Billing', 'N', 8, 'n']
    _BITS_VALUE_TYPE[11] = ['11', 'Systems Trace Audit Number', 'N', 6, 'n']
    _BITS_VALUE_TYPE[12] = ['12', 'Time, Local Transaction', 'N', 6, 'n']
    _BITS_VALUE_TYPE[13] = ['13', 'Date, Local Transaction', 'N', 4, 'n']
    _BITS_VALUE_TYPE[14] = ['14', 'Date, Expiration', 'N', 4, 'n']
    _BITS_VALUE_TYPE[15] = ['15', 'Date, Settlement', 'N', 4, 'n']
    _BITS_VALUE_TYPE[16] = ['16', 'Date, Conversion', 'N', 4, 'n']
    _BITS_VALUE_TYPE[18] = ['18', 'Merchant Type', 'N', 4, 'n']
    _BITS_VALUE_TYPE[22] = ['22', 'POS Entry Mode', 'N', 3, 'n']
    _BITS_VALUE_TYPE[23] = ['23', 'Card Sequence Number', 'N', 3, 'n']
    _BITS_VALUE_TYPE[25] = ['25', 'POS Condition Code', 'N', 2, 'n']
    _BITS_VALUE_TYPE[28] = ['28', 'Amount, Transaction Fee', 'AN', 9, 'an']
    _BITS_VALUE_TYPE[32] = ['32', 'Acquiring Institution ID Code', 'LL', 11, 'n']
    _BITS_VALUE_TYPE[33] = ['33', 'Forwarding Institution ID Code', 'LL', 11, 'n']
    _BITS_VALUE_TYPE[35] = ['35', 'Track 2 Data', 'LL', 37, 'an']
    _BITS_VALUE_TYPE[37] = ['37', 'Retrieval Reference Number', 'AN', 12, 'an']
    _BITS_VALUE_TYPE[38] = ['38', 'Authorization ID Response', 'AN', 6, 'an']
    _BITS_VALUE_TYPE[39] = ['39', 'Response Code', 'AN', 2, 'an']
    _BITS_VALUE_TYPE[41] = ['41', 'Card Acceptor Terminal ID', 'AN', 8, 'ans']
    _BITS_VALUE_TYPE[42] = ['42', 'Card Acceptor ID Code', 'AN', 15, 'ans']
    _BITS_VALUE_TYPE[43] = ['43', 'Card Acceptor Name Location', 'AN', 40, 'ans']
    _BITS_VALUE_TYPE[44] = ['44', 'Additional Response Data', 'LL', 25, 'ans']
    _BITS_VALUE_TYPE[47] = ['47', 'Additional Data National', 'LLL', 999, 'ans']
    _BITS_VALUE_TYPE[48] = ['48', 'Key Management data', 'LLLANS', 999, 'b']
    _BITS_VALUE_TYPE[49] = ['49', 'Currency Code, Transaction', 'AN', 3, 'n']
    _BITS_VALUE_TYPE[50] = ['50', 'Currency Code, Settlement', 'AN', 3, 'n']
    _BITS_VALUE_TYPE[51] = ['51', 'Currency Code, Billing', 'AN', 3, 'n']
    _BITS_VALUE_TYPE[52] = ['52', 'PIN Data', 'B', 8, 'b']
    _BITS_VALUE_TYPE[53] = ['53', 'Security Related Control Information', 'N', 16, 'n']
    _BITS_VALUE_TYPE[55] = ['55', 'ICC Data', 'LLL', 999, 'b']
    _BITS_VALUE_TYPE[57] = ['57', 'Amount Cash', 'N', 12, 'n']
    _BITS_VALUE_TYPE[58] = ['58', 'Ledger Balance', 'N', 12, 'n']
    _BITS_VALUE_TYPE[59] = ['59', 'Account Balance', 'N', 12, 'n']
    _BITS_VALUE_TYPE[64] = ['64', 'Message Authentication Code', 'B', 8, 'b']
    _BITS_VALUE_TYPE[66] = ['66', 'Settlement Code', 'N', 1, 'n']
    _BITS_VALUE_TYPE[70] = ['70', 'Network Management Information Code', 'N', 3, 'n']
    _BITS_VALUE_TYPE[74] = ['74', 'Credits, Number', 'N', 10, 'n']
    _BITS_VALUE_TYPE[75] = ['75', 'Credits, Reversal Number', 'N', 10, 'n']
    _BITS_VALUE_TYPE[76] = ['76', 'Debits, Number', 'N', 10, 'n']
    _BITS_VALUE_TYPE[77] = ['77', 'Debits, Reversal Number', 'N', 10, 'n']
    _BITS_VALUE_TYPE[78] = ['78', 'Transfer, Number', 'N', 10, 'n']
    _BITS_VALUE_TYPE[79] = ['79', 'Transfer, Reversal Number', 'N', 10, 'n']
    _BITS_VALUE_TYPE[80] = ['80', 'Inquiries, Number', 'N', 10, 'n']
    _BITS_VALUE_TYPE[81] = ['81', 'Authorizations, Number', 'N', 10, 'n']
    _BITS_VALUE_TYPE[83] = ['83', 'Credits, Transaction Fee Amount', 'N', 12, 'n']
    _BITS_VALUE_TYPE[85] = ['85', 'Debits, Transaction Fee Amount', 'N', 12, 'n']
    _BITS_VALUE_TYPE[86] = ['86', 'Credits, Amount', 'N', 16, 'n']
    _BITS_VALUE_TYPE[87] = ['87', 'Credits, Reversal Amount', 'N', 16, 'n']
    _BITS_VALUE_TYPE[88] = ['88', 'Debits, Amount', 'N', 16, 'n']
    _BITS_VALUE_TYPE[89] = ['89', 'Debits, Reversal Amount', 'N', 16, 'n']
    _BITS_VALUE_TYPE[90] = ['90', 'Original Data Elements', 'N', 42, 'n']
    _BITS_VALUE_TYPE[97] = ['97', 'Amount, Net Settlement', 'AN', 17, 'an']
    _BITS_VALUE_TYPE[95] = ['95', 'Replacement Amounts', 'AN', 42, 'ans']
    _BITS_VALUE_TYPE[99] = ['99', 'Settlement Institution ID Code', 'LL', 11, 'n']
    _BITS_VALUE_TYPE[100] = ['100', 'Receiving Institution ID Code', 'N', 6, 'n']
    _BITS_VALUE_TYPE[112] = ['112', 'Key Management Data', 'LLL', 999, 'b']
    _BITS_VALUE_TYPE[118] = ['118', 'Cash Total Number', 'LLL', 10, 'n']
    _BITS_VALUE_TYPE[119] = ['119', 'Cash Total Amount', 'LLL', 10, 'n']
    _BITS_VALUE_TYPE[125] = ['125', 'Network Management Information', 'LLL', 40, 'ans']
    _BITS_VALUE_TYPE[128] = ['128', 'MAC Extended', 'B', 16, 'b']



    # ###############################################################################################
    #Default constructor of the ISO8583 Object
    def __init__(self, iso="", debug=False):
        """Default Constructor of ISO8583 Package.
            It inicialize a "brand new" ISO8583 package
            Example: To Enable debug you can use:
                pack = ISO8583(debug=True)
            @param: iso a String that represents the ASCII of the package. The same that you need to pass to setIsoContent() method.
            @param: debug (True or False) default False -> Used to print some debug infos. Only use if want that messages!
            """
        #Bitmap internal representation
        self.BITMAP = []
        #Values
        self.BITMAP_VALUES = []
        #Bitmap ASCII representantion
        self.BITMAP_HEX = ''
        # MTI
        self.MESSAGE_TYPE_INDICATION = '';
        #Debug ?
        self.DEBUG = debug

        self.__inicializeBitmap()
        self.__inicializeBitmapValues()

        if iso != "":
            self.setIsoContent(iso)


    ################################################################################################

    ################################################################################################
    #Return bit type
    def getBitType(self, bit):
        """Method that return the bit Type
            @param: bit -> Bit that will be searched and whose type will be returned
            @return: str that represents the type of the bit
            """
        return self._BITS_VALUE_TYPE[bit][2]


    ################################################################################################

    ################################################################################################
    #Return bit limit
    def getBitLimit(self, bit):
        """Method that return the bit limit (Max size)
            @param: bit -> Bit that will be searched and whose limit will be returned
            @return: int that indicate the limit of the bit
            """
        return self._BITS_VALUE_TYPE[bit][3]


    ################################################################################################

    ################################################################################################
    #Return bit value type
    def getBitValueType(self, bit):
        """Method that return the bit value type
            @param: bit -> Bit that will be searched and whose value type will be returned
            @return: str that indicate the valuye type of the bit
            """
        return self._BITS_VALUE_TYPE[bit][4]


    ################################################################################################

    ################################################################################################
    #Return large bit name
    def getLargeBitName(self, bit):
        """Method that return the large bit name
            @param: bit -> Bit that will be searched and whose name will be returned
            @return: str that represents the name of the bit
            """
        return self._BITS_VALUE_TYPE[bit][1]


    ################################################################################################


    ################################################################################################
    # Set the MTI
    def setTransationType(self, type):
        """Method that set Transation Type (MTI)
            @param: type -> MTI to be setted
            @raise: ValueToLarge Exception
            """

        type = "%s" % type
        if len(type) > 4:
            type = type[0:3]
            raise ValueToLarge('Error: value up to size! MTI limit size = 4')

        typeT = "";
        if len(type) < 4:
            for cont in range(len(type), 4):
                typeT += "0"

        self.MESSAGE_TYPE_INDICATION = "%s%s" % (typeT, type)


    ################################################################################################

    ################################################################################################
    # setMTI too
    def setMTI(self, type):
        """Method that set Transation Type (MTI)
            In fact, is an alias to "setTransationType" method
            @param: type -> MTI to be setted
            """
        self.setTransationType(type)


    ################################################################################################

    ################################################################################################
    #Method that put "zeros" inside bitmap
    def __inicializeBitmap(self):
        """Method that inicialize/reset a internal bitmap representation
            It's a internal method, so don't call!
            """

        if self.DEBUG == True:
            print ('Init bitmap')

        if len(self.BITMAP) == 16:
            for cont in range(0, 16):
                self.BITMAP[cont] = self._BIT_DEFAULT_VALUE
        else:
            for cont in range(0, 16):
                self.BITMAP.append(self._BIT_DEFAULT_VALUE)


    ################################################################################################

    ################################################################################################
    #init with "0" the array of values
    def __inicializeBitmapValues(self):
        """Method that inicialize/reset a internal array used to save bits and values
            It's a internal method, so don't call!
            """
        if self.DEBUG == True:
            print ('Init bitmap_values')

        if len(self.BITMAP_VALUES) == 128:
            for cont in range(0, 128):
                self.BITMAP_VALUES[cont] = self._BIT_DEFAULT_VALUE
        else:
            for cont in range(0, 128):
                self.BITMAP_VALUES.append(self._BIT_DEFAULT_VALUE)


    ################################################################################################

    ################################################################################################
    # Set a value to a bit
    def setBit(self, bit, value):
        """Method used to set a bit with a value.
            It's one of the most important method to use when using this library
            @param: bit -> bit number that want to be setted
            @param: value -> the value of the bit
            @return: True/False default True -> To be used in the future!
            @raise: BitInexistent Exception, ValueToLarge Exception
            """
        if self.DEBUG == True:
            print ('Setting bit inside bitmap bit[%s] = %s') % (bit, value)

        if bit < 1 or bit > 128:
            raise BitInexistent("Bit number %s dosen't exist!" % bit)

        # caculate the position insede bitmap
        pos = 1

        if self.getBitType(bit) == 'LL':
            self.__setBitTypeLL(bit, value)

        if self.getBitType(bit) == 'LLL':
            self.__setBitTypeLLL(bit, value)

        if self.getBitType(bit) == 'N':
            self.__setBitTypeN(bit, value)

        if self.getBitType(bit) == 'A':
            self.__setBitTypeA(bit, value)

        if self.getBitType(bit) == 'ANS' or self.getBitType(bit) == 'B':
            self.__setBitTypeANS(bit, value)

        if self.getBitType(bit) == 'B':
            self.__setBitTypeB(bit, value)

        if self.getBitType(bit) == 'LLLANS':
            self.__setBitTypeLLLANS(bit, value)



        #Continuation bit?
        if bit > 64:
            self.BITMAP[0] = self.BITMAP[0] | self._TMP[2]  # need to set bit 1 of first "bit" in bitmap

        if (bit % 8) == 0:
            pos = (bit / 8) - 1
        else:
            pos = (bit / 8)

        #need to check if the value can be there .. AN , N ... etc ... and the size

        self.BITMAP[pos] = self.BITMAP[pos] | self._TMP[(bit % 8) + 1]

        return True


    ################################################################################################

    ################################################################################################
    #print bitmap
    def showBitmap(self):
        """Method that print the bitmap in ASCII form
            Hint: Try to use getBitmap method and format your own print :)
            """

        self.__buildBitmap()

        # printing
        print self.BITMAP_HEX


    ################################################################################################

    ################################################################################################
    #Build a bitmap
    def __buildBitmap(self):
        """Method that build the bitmap ASCII
            It's a internal method, so don't call!
            """

        self.BITMAP_HEX = ''

        for c in range(0, 16):
            if (self.BITMAP[0] & self._BIT_POSITION_1) != self._BIT_POSITION_1:
                # Only has the first bitmap
                if self.DEBUG == True:
                    print ('%d Bitmap = %d(Decimal) = %s (hexa) ' % (c, self.BITMAP[c], hex(self.BITMAP[c])))

                tm = hex(self.BITMAP[c])[2:]
                if len(tm) != 2:
                    tm = '0' + tm
                self.BITMAP_HEX += tm
                if c == 7:
                    break
            else:  # second bitmap
                if self.DEBUG == True:
                    print ('%d Bitmap = %d(Decimal) = %s (hexa) ' % (c, self.BITMAP[c], hex(self.BITMAP[c])))

                tm = hex(self.BITMAP[c])[2:]
                if len(tm) != 2:
                    tm = '0' + tm
                self.BITMAP_HEX += tm

            ################################################################################################


    ################################################################################################
    #Get a bitmap from str
    def __getBitmapFromStr(self, bitmap):
        """Method that receive a bitmap str and transfor it to ISO8583 object readable.
            @param: bitmap -> bitmap str to be readable
            It's a internal method, so don't call!
            """
        #Need to check if the size is correct etc...
        cont = 0

        if self.BITMAP_HEX != '':
            self.BITMAP_HEX = ''

        for x in range(0, 32, 2):
            if (int(bitmap[0:2], 16) & self._BIT_POSITION_1) != self._BIT_POSITION_1:  # Only 1 bitmap
                if self.DEBUG == True:
                    print ('Token[%d] %s converted to int is = %s' % (x, bitmap[x:x + 2], int(bitmap[x:x + 2], 16)))

                self.BITMAP_HEX += bitmap[x:x + 2]
                self.BITMAP[cont] = int(bitmap[x:x + 2], 16)
                if x == 14:
                    break
            else:  # Second bitmap
                if self.DEBUG == True:
                    print ('Token[%d] %s converted to int is = %s' % (x, bitmap[x:x + 2], int(bitmap[x:x + 2], 16)))

                self.BITMAP_HEX += bitmap[x:x + 2]
                self.BITMAP[cont] = int(bitmap[x:x + 2], 16)
            cont += 1


    ################################################################################################

    ################################################################################################
    # print bit array that is present in the bitmap
    def showBitsFromBitmapStr(self, bitmap):
        """Method that receive a bitmap str, process it, and print a array with bits this bitmap string represents.
            Usualy is used to debug things.
            @param: bitmap -> bitmap str to be analized and translated to "bits"
            """
        bits = self.__inicializeBitsFromBitmapStr(bitmap)
        print ('Bits inside %s  = %s' % (bitmap, bits))


    ################################################################################################

    ################################################################################################
    #inicialize a bitmap using ASCII str
    def __inicializeBitsFromBitmapStr(self, bitmap):
        """Method that receive a bitmap str, process it, and prepare ISO8583 object to understand and "see" the bits and values inside the ISO ASCII package.
            It's a internal method, so don't call!
            @param: bitmap -> bitmap str to be analized and translated to "bits"
            """
        bits = []
        for c in range(0, 16):
            for d in range(1, 9):
                if self.DEBUG == True:
                    print (
                        'Value (%d)-> %s & %s = %s' % (d, self.BITMAP[c], self._TMP[d], (self.BITMAP[c] & self._TMP[d]) ))
                if (self.BITMAP[c] & self._TMP[d]) == self._TMP[d]:
                    if d == 1:  #  e o 8 bit
                        if self.DEBUG == True:
                            print ('Bit %s is present !!!' % ((c + 1) * 8))
                        bits.append((c + 1) * 8)
                        self.BITMAP_VALUES[(c + 1) * 8] = 'X'
                    else:
                        if (c == 0) & (d == 2):  # Continuation bit
                            if self.DEBUG == True:
                                print ('Bit 1 is present !!!')

                            bits.append(1)

                        else:
                            if self.DEBUG == True:
                                print ('Bit %s is present !!!' % (c * 8 + d - 1))

                            bits.append(c * 8 + d - 1)
                            self.BITMAP_VALUES[c * 8 + d - 1] = 'X'

        bits.sort()

        return bits


    ################################################################################################

    ################################################################################################
    #return a array of bits, when processing the bitmap
    def __getBitsFromBitmap(self):
        """Method that process the bitmap and return a array with the bits presents inside it.
            It's a internal method, so don't call!
            """
        bits = []
        for c in range(0, 16):
            for d in range(1, 9):
                if self.DEBUG == True:
                    print (
                        'Value (%d)-> %s & %s = %s' % (d, self.BITMAP[c], self._TMP[d], (self.BITMAP[c] & self._TMP[d]) ))
                if (self.BITMAP[c] & self._TMP[d]) == self._TMP[d]:
                    if d == 1:  #  e o 8 bit
                        if self.DEBUG == True:
                            print ('Bit %s is present !!!' % ((c + 1) * 8))

                        bits.append((c + 1) * 8)
                    else:
                        if (c == 0) & (d == 2):  # Continuation bit
                            if self.DEBUG == True:
                                print ('Bit 1 is present !!!')

                            bits.append(1)

                        else:
                            if self.DEBUG == True:
                                print ('Bit %s is present !!!' % (c * 8 + d - 1))

                            bits.append(c * 8 + d - 1)

        bits.sort()

        return bits


    ################################################################################################

    ################################################################################################
    #Set of type LL
    def __setBitTypeLL(self, bit, value):
        """Method that set a bit with value in form LL
            It put the size in front of the value
            Example: pack.setBit(99,'123') -> Bit 99 is a LL type, so this bit, in ASCII form need to be 03123. To understand, 03 is the size of the information and 123 is the information/value
            @param: bit -> bit to be setted
            @param: value -> value to be setted
            @raise: ValueToLarge Exception
            It's a internal method, so don't call!
            """

        value = "%s" % value

        if len(value) > 99:
            #value = value[0:99]
            raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (
                bit, self.getBitType(bit), self.getBitLimit(bit)))
        if len(value) > self.getBitLimit(bit):
            raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (
                bit, self.getBitType(bit), self.getBitLimit(bit)))

        size = "%s" % len(value)

        self.BITMAP_VALUES[bit] = "%s%s" % ( size.zfill(2), value)


    ################################################################################################

    ################################################################################################
    #Set of type LLL
    def __setBitTypeLLL(self, bit, value):
        """Method that set a bit with value in form LLL
            It put the size in front of the value
            Example: pack.setBit(104,'12345ABCD67890') -> Bit 104 is a LLL type, so this bit, in ASCII form need to be 01412345ABCD67890.
                To understand, 014 is the size of the information and 12345ABCD67890 is the information/value
            @param: bit -> bit to be setted
            @param: value -> value to be setted
            @raise: ValueToLarge Exception
            It's a internal method, so don't call!
            """

        value = "%s" % value

        if len(value) > 999:
            raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (
                bit, self.getBitType(bit), self.getBitLimit(bit)))
        if len(value) > self.getBitLimit(bit):
            raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (
                bit, self.getBitType(bit), self.getBitLimit(bit)))

        size = "%s" % len(value)

        self.BITMAP_VALUES[bit] = "%s%s" % ( size.zfill(3), value)


    ################################################################################################

    ################################################################################################
    # Set of type N,
    def __setBitTypeN(self, bit, value):
        """Method that set a bit with value in form N
            It complete the size of the bit with a default value
            Example: pack.setBit(3,'30000') -> Bit 3 is a N type, so this bit, in ASCII form need to has size = 6 (ISO especification) so the value 30000 size = 5 need to receive more "1" number.
                In this case, will be "0" in the left. In the package, the bit will be sent like '030000'
            @param: bit -> bit to be setted
            @param: value -> value to be setted
            @raise: ValueToLarge Exception
            It's a internal method, so don't call!
            """

        value = "%s" % value

        if len(value) > self.getBitLimit(bit):
            value = value[0:self.getBitLimit(bit)]
            raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (
                bit, self.getBitType(bit), self.getBitLimit(bit)))

        self.BITMAP_VALUES[bit] = value.zfill(self.getBitLimit(bit))


    ################################################################################################

    ################################################################################################
    # Set of type A
    def __setBitTypeA(self, bit, value):
        """Method that set a bit with value in form A
            It complete the size of the bit with a default value
            Example: pack.setBit(3,'30000') -> Bit 3 is a A type, so this bit, in ASCII form need to has size = 6 (ISO especification) so the value 30000 size = 5 need to receive more "1" number.
                In this case, will be "0" in the left. In the package, the bit will be sent like '030000'
            @param: bit -> bit to be setted
            @param: value -> value to be setted
            @raise: ValueToLarge Exception
            It's a internal method, so don't call!
            """

        value = "%s" % value

        if len(value) > self.getBitLimit(bit):
            value = value[0:self.getBitLimit(bit)]
            raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (
                bit, self.getBitType(bit), self.getBitLimit(bit)))

        self.BITMAP_VALUES[bit] = value.zfill(self.getBitLimit(bit))


    ################################################################################################

    ################################################################################################
    # Set of type B
    def __setBitTypeB(self, bit, value):
        """Method that set a bit with value in form B
            It complete the size of the bit with a default value
            Example: pack.setBit(3,'30000') -> Bit 3 is a B type, so this bit, in ASCII form need to has size = 6 (ISO especification) so the value 30000 size = 5 need to receive more "1" number.
                In this case, will be "0" in the left. In the package, the bit will be sent like '030000'
            @param: bit -> bit to be setted
            @param: value -> value to be setted
            @raise: ValueToLarge Exception
            It's a internal method, so don't call!
            """

        value = "%s" % value

        if len(value) > self.getBitLimit(bit):
            value = value[0:self.getBitLimit(bit)]
            raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (
                bit, self.getBitType(bit), self.getBitLimit(bit)))

        self.BITMAP_VALUES[bit] = value.zfill(self.getBitLimit(bit))


    ################################################################################################


    def __setBitTypeLLLANS(self, bit, value):
        """Method that set a bit with value in form ANS
        It complete the size of the bit with a default value
        Example: pack.setBit(3,'30000') -> Bit 3 is a ANS type, so this bit, in ASCII form need to has size = 6 (ISO especification) so the value 30000 size = 5 need to receive more "1" number.
            In this case, will be "0" in the left. In the package, the bit will be sent like '030000'
        @param: bit -> bit to be setted
        @param: value -> value to be setted
        @raise: ValueToLarge Exception
        It's a internal method, so don't call!
        """

        value = "%s" % value
        value = value[0:6]
        ascii_limit = int(''.join(chr(int(value[i:i+2], 16)) for i in range(0, len(value), 2)))
        if len(value) > self.getBitLimit(bit):
            value = value[0:ascii_limit]
            raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (bit, self.getBitType(bit), self.getBitLimit(bit)))

        self.BITMAP_VALUES[bit] = value.zfill(ascii_limit)


    ################################################################################################
    # Set of type ANS
    def __setBitTypeANS(self, bit, value):
        """Method that set a bit with value in form ANS
            It complete the size of the bit with a default value
            Example: pack.setBit(3,'30000') -> Bit 3 is a ANS type, so this bit, in ASCII form need to has size = 6 (ISO especification) so the value 30000 size = 5 need to receive more "1" number.
                In this case, will be "0" in the left. In the package, the bit will be sent like '030000'
            @param: bit -> bit to be setted
            @param: value -> value to be setted
            @raise: ValueToLarge Exception
            It's a internal method, so don't call!
            """

        value = "%s" % value

        if len(value) > self.getBitLimit(bit):
            value = value[0:self.getBitLimit(bit)]
            raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (
                bit, self.getBitType(bit), self.getBitLimit(bit)))

        self.BITMAP_VALUES[bit] = value.zfill(self.getBitLimit(bit))


    ################################################################################################

    ################################################################################################
    # print os bits insede iso
    def showIsoBits(self):
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

        for cont in range(0, 128):
            if self.BITMAP_VALUES[cont] != self._BIT_DEFAULT_VALUE:
                print("Bit[%s] of type %s has limit %s = %s" % (
                    cont, self.getBitType(cont), self.getBitLimit(cont), self.BITMAP_VALUES[cont]) )


    ################################################################################################

    ################################################################################################
    # print Raw iso
    def showRawIso(self):
        """Method that print ISO8583 ASCII complete representation
            Example:
            iso = ISO8583()
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

    ################################################################################################
    # Return raw iso
    def getRawIso(self):
        """Method that return ISO8583 ASCII complete representation
            Example:
            iso = ISO8583()
            iso.setMTI('0800')
            iso.setBit(2,2)
            iso.setBit(4,4)
            iso.setBit(12,12)
            iso.setBit(17,17)
            iso.setBit(99,99)
            str = iso.getRawIso()
            print ('This is the ASCII package %s' % str)
            output (print) -> This is the ASCII package 0800d010800000000000000000002000000001200000000000400001200170299

            @return: str with complete ASCII ISO8583
            @raise: InvalidMTI Exception
            """

        self.__buildBitmap()

        if self.MESSAGE_TYPE_INDICATION == '':
            raise InvalidMTI('Check MTI! Do you set it?')

        resp = "";

        resp += self.MESSAGE_TYPE_INDICATION
        resp += self.BITMAP_HEX

        for cont in range(0, 128):
            if self.BITMAP_VALUES[cont] != self._BIT_DEFAULT_VALUE:
                resp = "%s%s" % (resp, self.BITMAP_VALUES[cont])

        return resp


    ################################################################################################

    ################################################################################################
    #Redefine a bit
    def redefineBit(self, bit, smallStr, largeStr, bitType, size, valueType):
        """Method that redefine a bit structure in global scope!
            Can be used to personalize ISO8583 structure to another specification (ISO8583 1987 for example!)
            Hint: If you have a lot of "ValueToLarge Exception" maybe the especification that you are using is different of mine. So you will need to use this method :)
            @param: bit -> bit to be redefined
            @param: smallStr -> a small String representantion of the bit, used to build "user friendly prints", example "2" for bit 2
            @param: largeStr -> a large String representantion of the bit, used to build "user friendly prints" and to be used to inform the "main use of the bit",
                example "Primary account number (PAN)" for bit 2
            @param: bitType -> type the bit, used to build the values, example "LL" for bit 2. Need to be one of (B, N, AN, ANS, LL, LLL)
            @param: size -> limit size the bit, used to build/complete the values, example "19" for bit 2.
            @param: valueType -> value type the bit, used to "validate" the values, example "n" for bit 2. This mean that in bit 2 we need to have only numeric values.
                Need to be one of (a, an, n, ansb, b)
            @raise: BitInexistent Exception, InvalidValueType Exception

            """

        if self.DEBUG == True:
            print ('Trying to redefine the bit with (self,%s,%s,%s,%s,%s,%s)' % (
                bit, smallStr, largeStr, bitType, size, valueType))

        #validating bit position
        if bit == 1 or bit == 64 or bit < 0 or bit > 128:
            raise BitInexistent("Error %d cannot be changed because has a invalid number!" % bit)

        #need to validate if the type and size is compatible! example slimit = 100 and type = LL

        if bitType == "B" or bitType == "N" or bitType == "AN" or bitType == "ANS" or bitType == "LL" or bitType == "LLL":
            if valueType == "a" or valueType == "n" or valueType == "ansb" or valueType == "ans" or valueType == "b" or valueType == "an":
                self._BITS_VALUE_TYPE[bit] = [smallStr, largeStr, bitType, size, valueType]
                if self.DEBUG == True:
                    print ('Bit %d redefined!' % bit)

            else:
                raise InvalidValueType(
                    "Error bit %d cannot be changed because %s is not a valid valueType (a, an, n ansb, b)!" % (
                        bit, valueType))
            #return
        else:
            raise InvalidBitType(
                "Error bit %d cannot be changed because %s is not a valid bitType (Hex, N, AN, ANS, LL, LLL)!" % (
                    bit, bitType))
        #return


    ################################################################################################

    ################################################################################################
    #a partir de um trem de string, pega o MTI
    def __setMTIFromStr(self, iso):
        """Method that get the first 4 characters to be the MTI.
            It's a internal method, so don't call!
            """

        self.MESSAGE_TYPE_INDICATION = iso[0:4]

        if self.DEBUG == True:
            print ('MTI found was %s' % self.MESSAGE_TYPE_INDICATION)


    ################################################################################################

    ################################################################################################
    #return the MTI
    def getMTI(self):
        """Method that return the MTI of the package
            @return: str -> with the MTI
            """

        #Need to validate if the MTI was setted ...etc ...
        return self.MESSAGE_TYPE_INDICATION


    ################################################################################################

    ################################################################################################
    #Return the bitmap
    def getBitmap(self):
        """Method that return the ASCII Bitmap of the package
            @return: str -> with the ASCII Bitmap
            """
        if self.BITMAP_HEX == '':
            self.__buildBitmap()

        return self.BITMAP_HEX


    ################################################################################################

    ################################################################################################
    #return the Varray of values
    def getValuesArray(self):
        """Method that return an internal array of the package
            @return: array -> with all bits, presents or not in the bitmap
            """
        return self.BITMAP_VALUES


    ################################################################################################

    ################################################################################################
    #Receive a str and interpret it to bits and values
    def __getBitFromStr(self, strWithoutMtiBitmap):
        """Method that receive a string (ASCII) without MTI and Bitmaps (first and second), understand it and remove the bits values
            @param: str -> with all bits presents whithout MTI and bitmap
            It's a internal method, so don't call!
            """

        if self.DEBUG == True:
            print ('This is the input string <%s>' % strWithoutMtiBitmap)

        offset = 0;
        # jump bit 1 because it was alread defined in the "__inicializeBitsFromBitmapStr"
        for cont in range(2, 128):
            if self.BITMAP_VALUES[cont] != self._BIT_DEFAULT_VALUE:
                if self.DEBUG == True:
                    print ('String = %s offset = %s bit = %s' % (strWithoutMtiBitmap[offset:], offset, cont))

                if self.getBitType(cont) == 'LL':
                    valueSize = int(strWithoutMtiBitmap[offset:offset + 2])
                    if self.DEBUG == True:
                        print ('Size of the message in LL = %s' % valueSize)

                    if valueSize > self.getBitLimit(cont):
                        raise ValueToLarge(
                            "Bit %d (%s) is larger than the specification!" % (cont, self.getLargeBitName(cont),))
                    self.BITMAP_VALUES[cont] = strWithoutMtiBitmap[offset:offset + 2] + strWithoutMtiBitmap[
                                                                                        offset + 2:offset + 2 + valueSize]

                    if self.DEBUG == True:
                        print ('\tSetting bit %s value %s' % (cont, self.BITMAP_VALUES[cont]))

                    offset += valueSize + 2

                if self.getBitType(cont) == 'LLL':
                    valueSize = int(strWithoutMtiBitmap[offset:offset + 3])
                    if self.DEBUG == True:
                        print ('Size of the message in LLL = %s' % valueSize)

                    if valueSize > self.getBitLimit(cont):
                        raise ValueToLarge("This bit is larger than the especification!")
                    self.BITMAP_VALUES[cont] = strWithoutMtiBitmap[offset:offset + 3] + strWithoutMtiBitmap[offset + 3:offset + 3 + valueSize]

                    if self.DEBUG == True:
                        print ('\tSetting bit %s value %s' % (cont, self.BITMAP_VALUES[cont]))

                    offset += valueSize + 3

                # if self.getBitType(cont) == 'LLLL':
                # valueSize = int(strWithoutMtiBitmap[offset:offset +4])
                # if valueSize > self.getBitLimit(cont):
                # raise ValueToLarge("This bit is larger than the especification!")
                # self.BITMAP_VALUES[cont] = '(' + strWithoutMtiBitmap[offset:offset+4] + ')' + strWithoutMtiBitmap[offset+4:offset+4+valueSize]
                # offset += valueSize + 4

                if self.getBitType(cont) == 'N' or self.getBitType(cont) == 'A' or self.getBitType(cont) == 'ANS' or self.getBitType(cont) == 'B' or self.getBitType(cont) == 'AN':
                    self.BITMAP_VALUES[cont] = strWithoutMtiBitmap[offset:self.getBitLimit(cont) + offset]
                    offset += self.getBitLimit(cont)
                    if self.DEBUG == True:
                        print ('\tSetting bit %s value %s' % (cont, self.BITMAP_VALUES[cont]))
                if self.getBitType(cont) == 'LLLANS':
                    valueSize = strWithoutMtiBitmap[offset:offset + 6]

                    valueSize =  int(''.join(chr(int(valueSize[i:i+2], 16)) for i in range(0, len(valueSize), 2)))
                    valueSize = valueSize *2
                    print strWithoutMtiBitmap
                    self.BITMAP_VALUES[cont] = strWithoutMtiBitmap[offset:offset + 6] + strWithoutMtiBitmap[offset + 6:offset + 6 + valueSize]
                    if self.DEBUG == True:
                        print ('\tSetting bit %s value %s' % (cont, self.BITMAP_VALUES[cont]))
                    offset += valueSize + 6


    ################################################################################################

    ################################################################################################
    #Parse a ASCII iso to object
    def setIsoContent(self, iso):
        """Method that receive a complete ISO8583 string (ASCII) understand it and remove the bits values
            Example:
                iso = '0210B238000102C080040000000000000002100000000000001700010814465469421614465701081100301000000N399915444303500019991544986020   Value not allowed009000095492'
                i2 = ISO8583()
                # in this case, we need to redefine a bit because default bit 42 is LL and in this especification is "N"
                # the rest remain, so we use "get" :)
                i2.redefineBit(42, '42', i2.getLargeBitName(42), 'N', i2.getBitLimit(42), i2.getBitValueType(42) )
                i2.setIsoContent(iso2)
                print 'Bitmap = %s' %i2.getBitmap()
                print 'MTI = %s' %i2.getMTI()

                print 'This ISO has bits:'
                v3 = i2.getBitsAndValues()
                for v in v3:
                    print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))

            @param: str -> complete ISO8583 string
            @raise: InvalidIso8583 Exception
            """
        if len(iso) < 20:
            raise InvalidIso8583('This is not a valid iso!!')
        if self.DEBUG == True:
            print ('ASCII to process <%s>' % iso)

        self.__setMTIFromStr(iso)
        isoT = iso[4:]
        self.__getBitmapFromStr(isoT)
        self.__inicializeBitsFromBitmapStr(self.BITMAP_HEX)
        if self.DEBUG == True:
            print ('This is the array of bits (before) %s ' % self.BITMAP_VALUES)

        self.__getBitFromStr(iso[4 + len(self.BITMAP_HEX):])
        if self.DEBUG == True:
            print ('This is the array of bits (after) %s ' % self.BITMAP_VALUES)


    ################################################################################################

    ################################################################################################
    #Method that compare 2 isos
    def __cmp__(self, obj2):
        """Method that compare two objects in "==", "!=" and other things
            Example:
                p1 = ISO8583()
                p1.setMTI('0800')
                p1.setBit(2,2)
                p1.setBit(4,4)
                p1.setBit(12,12)
                p1.setBit(17,17)
                p1.setBit(99,99)

                #get the rawIso and save in the iso variable
                iso = p1.getRawIso()

                p2 = ISO8583()
                p2.setIsoContent(iso)

                print 'Is equivalent?'
                if p1 == p1:
                    print ('Yes :)')
                else:
                    print ('Noooooooooo :(')

            @param: obj2 -> object that will be compared
            @return: <0 if is not equal, 0 if is equal
            """
        ret = -1  # By default is different
        if (self.getMTI() == obj2.getMTI()) and (self.getBitmap() == obj2.getBitmap()) and (
                    self.getValuesArray() == obj2.getValuesArray()):
            ret = 0

        return ret


    ################################################################################################

    ################################################################################################
    # Method that return a array with bits and values inside the iso package
    def getBitsAndValues(self):
        """Method that return an array of bits, values, types etc.
                Each array value is a dictionary with: {'bit':X ,'type': Y, 'value': Z} Where:
                    bit: is the bit number
                    type: is the bit type
                    value: is the bit value inside this object
                so the Generic array returned is:  [ (...),{'bit':X,'type': Y, 'value': Z}, (...)]

            Example:
                p1 = ISO8583()
                p1.setMTI('0800')
                p1.setBit(2,2)
                p1.setBit(4,4)
                p1.setBit(12,12)
                p1.setBit(17,17)
                p1.setBit(99,99)

                v1 = p1.getBitsAndValues()
                for v in v1:
                    print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))

            @return: array of values.
            """
        ret = []
        for cont in range(2, 128):
            if self.BITMAP_VALUES[cont] != self._BIT_DEFAULT_VALUE:
                _TMP = {}
                _TMP['bit'] = "%d" % cont
                _TMP['type'] = self.getBitType(cont)
                _TMP['value'] = self.BITMAP_VALUES[cont]
                ret.append(_TMP)
        return ret


    ################################################################################################

    ################################################################################################
    # Method that return a array with bits and values inside the iso package
    def getBit(self, bit):
        """Return the value of the bit
            @param: bit -> the number of the bit that you want the value
            @raise: BitInexistent Exception, BitNotSet Exception
            """

        if bit < 1 or bit > 128:
            raise BitInexistent("Bit number %s dosen't exist!" % bit)

        #Is that bit set?
        isThere = False
        arr = self.__getBitsFromBitmap()

        if self.DEBUG == True:
            print ('This is the array of bits inside the bitmap %s' % arr)

        for v in arr:
            if v == bit:
                value = self.BITMAP_VALUES[bit]
                isThere = True
                break

        if isThere:
            return value
        else:
            raise BitNotSet("Bit number %s was not set!" % bit)


    ################################################################################################

    ################################################################################################
    #Method that return ISO8583 to TCPIP network form, with the size in the beginning.
    def getNetworkISO(self, bigEndian=True):
        """Method that return ISO8583 ASCII package with the size in the beginning
            By default, it return the package with size represented with big-endian.
            Is the same that:
                import struct
                (...)
                iso = ISO8583()
                iso.setBit(3,'300000')
                (...)
                ascii = iso.getRawIso()
                # Example: big-endian
                # To little-endian, replace '!h' with '<h'
                netIso = struct.pack('!h',len(iso))
                netIso += ascii
                # Example: big-endian
                # To little-endian, replace 'iso.getNetworkISO()' with 'iso.getNetworkISO(False)'
                print ('This <%s> the same that <%s>' % (iso.getNetworkISO(),netIso))

            @param: bigEndian (True|False) -> if you want that the size be represented in this way.
            @return: size + ASCII ISO8583 package ready to go to the network!
            @raise: InvalidMTI Exception
            """

        netIso = ""
        asciiIso = self.getRawIso()

        if bigEndian:
            netIso = struct.pack('!h', len(asciiIso))
            if self.DEBUG == True:
                print ('Pack Big-endian')
        else:
            netIso = struct.pack('<h', len(asciiIso))
            if self.DEBUG == True:
                print ('Pack Little-endian')

        netIso += asciiIso

        return netIso


    ################################################################################################

    ################################################################################################
    # Method that recieve a ISO8583 ASCII package in the network form and parse it.
    def setNetworkISO(self, iso, bigEndian=True):
        """Method that receive sie + ASCII ISO8583 package and transfor it in the ISO8583 object.
                By default, it recieve the package with size represented with big-endian.
                Is the same that:
                import struct
                (...)
                iso = ISO8583()
                iso.setBit(3,'300000')
                (...)
                # Example: big-endian
                # To little-endian, replace 'iso.getNetworkISO()' with 'iso.getNetworkISO(False)'
                netIso = iso.getNetworkISO()
                newIso = ISO8583()
                # Example: big-endian
                # To little-endian, replace 'newIso.setNetworkISO()' with 'newIso.setNetworkISO(False)'
                newIso.setNetworkISO(netIso)
                #Is the same that:
                #size = netIso[0:2]
                ## To little-endian, replace '!h' with '<h'
                #size = struct.unpack('!h',size )
                #newIso.setIsoContent(netIso[2:size])
                arr = newIso.getBitsAndValues()
                for v in arr:
                    print ('Bit %s Type %s Value = %s' % (v['bit'],v['type'],v['value']))

                @param: iso -> str that represents size + ASCII ISO8583 package
                @param: bigEndian (True|False) -> Codification of the size.
                @raise: InvalidIso8583 Exception
            """

        if len(iso) < 24:
            raise InvalidIso8583('This is not a valid iso!!Invalid Size')

        size = iso[0:2]
        if bigEndian:
            size = struct.unpack('!h', size)
            if self.DEBUG == True:
                print ('Unpack Big-endian')
        else:
            size = struct.unpack('<h', size)
            if self.DEBUG == True:
                print ('Unpack Little-endian')

        if len(iso) != (size[0] + 2):
            raise InvalidIso8583(
                'This is not a valid iso!!The ISO8583 ASCII(%s) is less than the size %s!' % (len(iso[2:]), size[0]))

        self.setIsoContent(iso[2:])

        ################################################################################################