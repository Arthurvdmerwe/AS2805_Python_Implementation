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

__author__ =  'Igor Vitorio Custodio <igorvc@vulcanno.com.br>'
__version__=  '0.2'
__licence__ = 'GPL V3'



from ISOErrors import *
import struct
from bitstring import *


class ISO8583:
	"""Main Class to work with ISO8583 packages.
	Used to create, change, send, receive, parse or work with ISO8593 Package version 1993.
	It's 100% Python :)
	Enjoy it!
	Thanks to: Vulcanno IT Solutions <http://www.vulcanno.com.br>
	Licence: GPL Version 3
	More information: http://code.google.com/p/iso8583py/

	Example:
		from ISO8583.ISO8583 import ISO8583
		from ISO8583.ISOErrors import *
		
		iso = ISO8583()
		try:
			iso.setMTI('0800')
			iso.setBit(2,2)
			iso.setBit(4,4)
			iso.setBit(12,12)
			iso.setBit(21,21)
			iso.setBit(17,17)
			iso.setBit(49,986)
			iso.setBit(99,99)
		except ValueToLarge, e:
				print 'Value too large :( %s' % e
		except InvalidMTI, i:
				print 'This MTI is wrong :( %s' % i
				
		print 'The Message Type Indication is = %s' %iso.getMTI() 
		
		print 'The Bitmap is = %s' %iso.getBitmap() 
		iso.showIsoBits();
		print 'This is the ISO8583 complete package %s' % iso.getRawIso()
		print 'This is the ISO8583 complete package to sent over the TCPIP network %s' % iso.getNetworkISO()
	
	"""
	#Attributes
	# Bitsto be set 00000000 -> _BIT_POSITION_1 ... _BIT_POSITION_8
	_BIT_POSITION_1 = 128 # 10 00 00 00
	_BIT_POSITION_2 =  64 # 01 00 00 00
	_BIT_POSITION_3 =  32 # 00 10 00 00
	_BIT_POSITION_4 =  16 # 00 01 00 00
	_BIT_POSITION_5 =   8 # 00 00 10 00
	_BIT_POSITION_6 =   4 # 00 00 01 00
	_BIT_POSITION_7 =   2 # 00 00 00 10 
	_BIT_POSITION_8 =   1 # 00 00 00 01
	
	#Array to translate bit to position
	_TMP = [0,_BIT_POSITION_8,_BIT_POSITION_1,_BIT_POSITION_2,_BIT_POSITION_3,_BIT_POSITION_4,_BIT_POSITION_5,_BIT_POSITION_6,_BIT_POSITION_7]
	_EMPTY_VALUE = 0

	#ISO8583 contants
	_DEF = {}
	# Every _DEF has:
	# _DEF[N] = [X, Y, Z, W, K]
	# N = bitnumber
	# X = smallStr representation of the bit meanning
	# Y = large str representation
	# Z = length indicator of the bit (F, LL, LLL, LLLL, LLLLL, LLLLLL)
	# W = size of the information that N need to has
	# K = type os values a, an, ans, n, xn, b
	_DEF[1]   = ['BME','Bit Map Extended',                          'F',           8, 'b'  ]
	_DEF[2]   = ['2',  'Primary Account Number (PAN)',              'LL',         19, 'n'  ]
	_DEF[3]   = ['3',  'Processing Code',                           'F',           6, 'n'  ]
	_DEF[4]   = ['4',  'Amount Transaction',                        'F',          12, 'n'  ]
	_DEF[5]   = ['5',  'Amount Settlement',                         'F',          12, 'n'  ]
	_DEF[7]   = ['7',  'Transmission Date and Time',                'F',          10, 'n'  ]
	_DEF[9]   = ['9',  'Conversion Rate, Settlement',               'F',           8, 'n'  ]
	_DEF[11]  = ['11', 'Systems Trace Audit Number',                'F',           6, 'n'  ]
	_DEF[12]  = ['12', 'Time, Local Transaction',                   'F',           6, 'n'  ]
	_DEF[13]  = ['13', 'Date, Local Transaction',                   'F',           4, 'n'  ]
	_DEF[14]  = ['14', 'Date, Expiration',                          'F',           4, 'n'  ]
	_DEF[15]  = ['15', 'Date, Settlement',                          'F',           4, 'n'  ]
	_DEF[16]  = ['16', 'Date, Conversion',                          'F',           4, 'n'  ]
	_DEF[18]  = ['18', 'Merchant Type',                             'F',           4, 'n'  ]
	_DEF[22]  = ['22', 'POS Entry Mode',                            'F',           3, 'n'  ]
	_DEF[23]  = ['23', 'Card Sequence Number',                      'F',           3, 'n'  ]
	_DEF[25]  = ['25', 'POS Condition Code',                        'F',           2, 'n'  ]
	_DEF[26]  = ['26', 'POS PIN Capture Code',                      'F',           2, 'n'  ]
	_DEF[27]  = ['27', 'Authorization ID Response Length',          'F',           1, 'n'  ]
	_DEF[28]  = ['28', 'Amount, Transaction Fee',                   'F',           9, 'xn' ]
	_DEF[29]  = ['29', 'Amount, Settlement Fee',                    'F',           9, 'xn' ]
	_DEF[30]  = ['30', 'Amount, Transaction Processing Fee',        'F',           9, 'xn' ]
	_DEF[31]  = ['31', 'Amount, Settle Processing Fee',             'F',           9, 'xn' ]
	_DEF[32]  = ['32', 'Acquiring Institution ID Code',             'LL',         11, 'n'  ]
	_DEF[33]  = ['33', 'Forwarding Institution ID Code',            'LL',         11, 'n'  ]
	_DEF[35]  = ['35', 'Track 2 Data',                              'LL',         37, 'an' ]
	_DEF[37]  = ['37', 'Retrieval Reference Number',                'F',          12, 'an' ]
	_DEF[38]  = ['38', 'Authorization ID Response',                 'F',           6, 'an' ]
	_DEF[39]  = ['39', 'Response Code',                             'F',           2, 'an' ]
	_DEF[40]  = ['40', 'Service Restriction Code',                  'F',           3, 'an' ]
	_DEF[41]  = ['41', 'Card Acceptor Terminal ID',                 'F',           8, 'ans']
	_DEF[42]  = ['42', 'Card Acceptor ID Code',                     'F',          15, 'ans']
	_DEF[43]  = ['43', 'Card Acceptor Name Location',               'F',          40, 'asn']
	_DEF[44]  = ['44', 'Additional Response Data',                  'LL',         25, 'ans']
	_DEF[45]  = ['45', 'Track 1 Data',                              'LL',         76, 'ans']
	_DEF[48]  = ['48', 'Additional Data',                           'LLL',       999, 'ans']
	_DEF[49]  = ['49', 'Currency Code, Transaction',                'F',           3, 'n'  ]
	_DEF[50]  = ['50', 'Currency Code, Settlement',                 'F',           3, 'n'  ]
	_DEF[52]  = ['52', 'PIN Data',                                  'F',           8, 'b'  ]
	_DEF[53]  = ['53', 'Security Related Control Information',      'F',          48, 'b'  ]
	_DEF[54]  = ['54', 'Additional Amounts',                        'LLL',       120, 'an' ]
	_DEF[56]  = ['56', 'Message Reason Code',                       'LLL',         4, 'n'  ]
	_DEF[57]  = ['57', 'Authorization Life-cycle Code',             'LLL',         3, 'n'  ]
	_DEF[58]  = ['58', 'Authorizing Agent ID Code',                 'LLL',        11, 'n'  ]
	_DEF[59]  = ['59', 'Echo Data',                                 'LLL',       255, 'ans']
	_DEF[66]  = ['66', 'Settlement Code',                           'F',           1, 'n'  ]
	_DEF[67]  = ['67', 'Extended Payment Code',                     'F',           2, 'n'  ]
	_DEF[70]  = ['70', 'Network Management Information Code',       'F',           3, 'n'  ]
	_DEF[73]  = ['73', 'Date, Action',                              'F',           6, 'n'  ]
	_DEF[74]  = ['74', 'Credits, Number',                           'F',          10, 'n'  ]
	_DEF[75]  = ['75', 'Credits, Reversal Number',                  'F',          10, 'n'  ]
	_DEF[76]  = ['76', 'Debits, Number',                            'F',          10, 'n'  ]
	_DEF[77]  = ['77', 'Debits, Reversal Number',                   'F',          10, 'n'  ]
	_DEF[78]  = ['78', 'Transfer, Number',                          'F',          10, 'n'  ]
	_DEF[79]  = ['79', 'Transfer, Reversal Number',                 'F',          10, 'n'  ]
	_DEF[80]  = ['80', 'Inquiries, Number',                         'F',          10, 'n'  ]
	_DEF[81]  = ['81', 'Authorizations, Number',                    'F',          10, 'n'  ]
	_DEF[82]  = ['82', 'Credits, Processing Fee Amount',            'F',          12, 'n'  ]
	_DEF[83]  = ['83', 'Credits, Transaction Fee Amount',           'F',          12, 'n'  ]
	_DEF[84]  = ['84', 'Debits, Processing Fee Amount',             'F',          12, 'n'  ]
	_DEF[85]  = ['85', 'Debits, Transaction Fee Amount',            'F',          12, 'n'  ]
	_DEF[86]  = ['86', 'Credits, Amount',                           'F',          16, 'n'  ]
	_DEF[87]  = ['87', 'Credits, Reversal Amount',                  'F',          16, 'n'  ]
	_DEF[88]  = ['88', 'Debits, Amount',                            'F',          16, 'n'  ]
	_DEF[89]  = ['89', 'Debits, Reversal Amount',                   'F',          16, 'n'  ]
	_DEF[90]  = ['90', 'Original Data Elements',                    'F',          42, 'n'  ]
	_DEF[91]  = ['91', 'File Update Code',                          'F',           1, 'an' ]
	_DEF[95]  = ['95', 'Replacement Amounts',                       'F',          42, 'an' ]
	_DEF[97]  = ['97', 'Amount, Net Settlement',                    'F',          17, 'xn' ]
	_DEF[98]  = ['98', 'Payee',                                     'F',          25, 'ans']
	_DEF[100] = ['100','Receiving Institution ID Code',             'LL',         11, 'n'  ]
	_DEF[101] = ['101','File Name',                                 'LL',         17, 'ans']
	_DEF[102] = ['102','Account Identification 1',                  'LL',         28, 'ans']
	_DEF[103] = ['103','Account Identification 2',                  'LL',         28, 'ans']
	_DEF[118] = ['118','Payments, Number',                          'LLL',        10, 'n'  ]
	_DEF[119] = ['119','Payments, Reversal Number',                 'LLL',        10, 'n'  ]
	_DEF[123] = ['123','POS Data Code',                             'LLL',        15, 'an' ]
	_DEF[125] = ['125','Network Management Information',            'LLL',        40, 'ans']
	_DEF[127] = ['127','Postillion Field 127',                      'LLLLLL', 999999, 'ans']
	_DEF[128] = ['128','MAC Extended',                              'F',           8, 'b'  ]


	#ISO8583 Field 127 contants
	_DEF127 = {}
	# Every _DEF127 has:
	# _DEF127[N] = [X, Y, Z, W, K]
	# N = bitnumber
	# X = smallStr representation of the bit meanning
	# Y = large str representation
	# Z = length indicator of the bit (F, LL, LLL, LLLL, LLLLL, LLLLLL)
	# W = size of the information that N need to has
	# K = type os values a, an, ans, n, xn, b
	_DEF127[1]  = ['BM', 'Bit Map',                                 'F',         8, 'b'  ]
	_DEF127[2]  = ['2',  'Switch Key',                              'LL',       32, 'ans']
	_DEF127[3]  = ['3',  'Routing Information',                     'F',        48, 'ans']
	_DEF127[4]  = ['4',  'POS Data',                                'F',        22, 'ans']
	_DEF127[5]  = ['5',  'Service Station Data',                    'F',        73, 'ans']
	_DEF127[6]  = ['6',  'Authorization Profile',                   'F',         2, 'n'  ]
	_DEF127[7]  = ['7',  'Check Data',                              'LL',       50, 'ans']
	_DEF127[8]  = ['8',  'Retention Data',                          'LLL',     999, 'ans']
	_DEF127[9]  = ['9',  'Additional Node Data',                    'LLL',     999, 'ans']
	_DEF127[10] = ['10', 'CVV2',                                    'F',         3, 'n'  ]
	_DEF127[11] = ['11', 'Original Key',                            'LL',       32, 'ans']
	_DEF127[12] = ['12', 'Terminal Owner',                          'LL',       25, 'ans']
	_DEF127[13] = ['13', 'POS Geographic Data',                     'F',        17, 'ans']
	_DEF127[14] = ['14', 'Sponsor Bank',                            'F',         8, 'ans']
	_DEF127[15] = ['15', 'Address Verification Data',               'LL',       29, 'ans']
	_DEF127[16] = ['16', 'Address Verification Result',             'F',         1, 'ans']
	_DEF127[17] = ['17', 'Cardholder Information',                  'LL',       50, 'ans']
	_DEF127[18] = ['18', 'Validation data',                         'LL',       50, 'ans']
	_DEF127[19] = ['19', 'Bank details',                            'F',        31, 'ans']
	_DEF127[20] = ['20', 'Originator / Authorizer date settlement', 'F',         8, 'n'  ]
	_DEF127[21] = ['21', 'Record identification',                   'LL',       12, 'ans']
	_DEF127[22] = ['22', 'Structured Data',                         'LLLLL', 99999, 'ans']
	_DEF127[23] = ['23', 'Payee name and address',                  'F',       253, 'ans']
	_DEF127[24] = ['24', 'Payer account',                           'LL',       28, 'ans']
	_DEF127[25] = ['25', 'Integrated circuit card (ICC) Data',      'LLLL',   8000, 'ans']
	_DEF127[26] = ['26', 'Original Node',                           'LL',       12, 'ans']
	_DEF127[27] = ['27', 'Card Verification Result',                'F',         1, 'ans']
	_DEF127[28] = ['28', 'American Express Card Identifier (CID)',  'F',         4, 'n'  ]
	_DEF127[29] = ['29', '3D Secure Data',                          'F',        40, 'b'  ]
	_DEF127[30] = ['30', '3D Secure Result',                        'F',         1, 'ans']
	_DEF127[31] = ['31', 'Issuer Network ID',                       'LL',       11, 'ans']
	_DEF127[32] = ['32', 'UCAF data',                               'LL',       33, 'b'  ]
	_DEF127[33] = ['33', 'Extended Transaction Type',               'F',         4, 'n'  ]
	_DEF127[34] = ['34', 'Account Type Qualifiers',                 'F',         2, 'n'  ]
	_DEF127[35] = ['35', 'Acquirer Network ID',                     'LL',       11, 'ans']
	_DEF127[39] = ['39', 'Original Response Code',                  'F',         2, 'an' ]	
	
	################################################################################################

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
		self.BITMAP127 = []
		#Values
		self._VALUES = []
		self._VALUES127 = []
		#Bitmap ASCII representantion
		self.BITMAP_HEX = ''
		self.BITMAP127_HEX = ''
		# MTI
		self.MESSAGE_TYPE_INDICATION = '';
		#Debug ?
		self.DEBUG = debug
		
		self.__initializeBitmap()
		self.__initializeValues()
		
		if iso != "":
			self.setIsoContent(iso)

	################################################################################################
	
	def getLengthType(self,bit):
		"""Method that return the bit Type
		@param: bit -> Bit that will be searched and whose type will be returned
		@return: str that represents the type of the bit
		"""
		return self._DEF[bit][2]

	################################################################################################
	
	def getLengthType127(self,bit):
		"""Method that return the bit Type
		@param: bit -> Bit that will be searched and whose type will be returned
		@return: str that represents the type of the bit
		"""
		return self._DEF127[bit][2]
	
	################################################################################################
	
	def getMaxLength(self,bit):
		"""Method that return the bit limit (Max size)
		@param: bit -> Bit that will be searched and whose limit will be returned
		@return: int that indicate the limit of the bit 
		"""
		return self._DEF[bit][3]
	
	################################################################################################

	def getMaxLength127(self,bit):
		"""Method that return the bit limit (Max size)
		@param: bit -> Bit that will be searched and whose limit will be returned
		@return: int that indicate the limit of the bit 
		"""
		return self._DEF127[bit][3]
	
	################################################################################################
	
	def getDataType(self,bit):
		"""Method that return the bit value type 
		@param: bit -> Bit that will be searched and whose value type will be returned
		@return: str that indicate the valuye type of the bit 
		"""
		return self._DEF[bit][4]

	################################################################################################
	
	def getDataType127(self,bit):
		"""Method that return the bit value type 
		@param: bit -> Bit that will be searched and whose value type will be returned
		@return: str that indicate the valuye type of the bit 
		"""
		return self._DEF127[bit][4]

	################################################################################################
	
	def getBitName(self,bit):
		"""Method that return the large bit name
		@param: bit -> Bit that will be searched and whose name will be returned
		@return: str that represents the name of the bit
		"""
		return self._DEF[bit][1]
	
	################################################################################################

	def getBitName127(self,bit):
		"""Method that return the large bit name
		@param: bit -> Bit that will be searched and whose name will be returned
		@return: str that represents the name of the bit
		"""
		return self._DEF127[bit][1]
	
	################################################################################################

	def setTransationType(self, type):
		"""Method that set Transation Type (MTI)
		@param: type -> MTI to be setted
		"""
		
		self.MESSAGE_TYPE_INDICATION = ("0000%s" % type)[-4:]
	
	################################################################################################
	
	def setMTI(self,type):
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
		
		if self.DEBUG == True:
			print 'Init bitmap'
			
		if len(self.BITMAP) == 16:
			for cont in range(0,16):
				self.BITMAP[cont] = self._EMPTY_VALUE
		else:
			for cont in range(0,16):
				self.BITMAP.append(self._EMPTY_VALUE)
				
		if len(self.BITMAP127) == 8:
			for cont in range(0,8):
				self.BITMAP127[cont] = self._EMPTY_VALUE
		else:
			for cont in range(0,8):
				self.BITMAP127.append(self._EMPTY_VALUE)
	################################################################################################

	def __initializeValues(self):
		"""Method that inicialize/reset a internal array used to save bits and values
		It's a internal method, so don't call!
		"""
		if self.DEBUG == True:
			print 'Init bitmap_values'
			
		if len(self._VALUES) == 128:
			for cont in range(0,128):
				self._VALUES[cont] = self._EMPTY_VALUE
		else:
			for cont in range(0,128):
				self._VALUES.append(self._EMPTY_VALUE)

		if len(self._VALUES127) == 64:
			for cont in range(0,64):
				self._VALUES127[cont] = self._EMPTY_VALUE
		else:
			for cont in range(0,64):
				self._VALUES127.append(self._EMPTY_VALUE)

	################################################################################################		
	
	def setBit(self, bit, value):
		"""Method used to set a bit with a value.
		It's one of the most important method to use when using this library
		@param: bit -> bit number that want to be setted
		@param: value -> the value of the bit
		@return: True/False default True -> To be used in the future!
		@raise: BitInexistent Exception, ValueToLarge Exception
		"""
		if bit < 1 or bit > 128:
			raise BitInexistent("Bit number %s dosen't exist!" % bit)
			
		if self.DEBUG == True:
			print 'Setting Bit %s (%s) = [%s]' % (bit, self.getBitName(bit), ReadableAscii(value))
			
		# caculate the position insede bitmap
		pos = 1
		
		if   self.getLengthType(bit) == 'F' :
			self.__setBitFixedLength(bit, value)
		elif self.getLengthType(bit) == 'LL':
			self.__setBitVariableLength(bit, value, 2)
		elif self.getLengthType(bit) == 'LLL':
			self.__setBitVariableLength(bit, value, 3)
		elif self.getLengthType(bit) == 'LLLL':
			self.__setBitVariableLength(bit, value, 4)
		elif self.getLengthType(bit) == 'LLLLL':
			self.__setBitVariableLength(bit, value, 5)
		elif self.getLengthType(bit) == 'LLLLLL':
			self.__setBitVariableLength(bit, value, 6)
		
		#Continuation bit?
		if bit > 64:
			self.BITMAP[0] = self.BITMAP[0] |  self._TMP[2] # need to set bit 1 of first "bit" in bitmap
			
		if (bit % 8) == 0:
			pos = (bit / 8) - 1
		else:
			pos = (bit /8) 

		#need to check if the value can be there .. AN , N ... etc ... and the size
		
		self.BITMAP[pos] = self.BITMAP[pos] | self._TMP[ (bit%8) +1]
		
		return True

	################################################################################################

	def setBit127(self, bit, value):
		"""Method used to set a bit with a value.
		It's one of the most important method to use when using this library
		@param: bit -> bit number that want to be setted
		@param: value -> the value of the bit
		@return: True/False default True -> To be used in the future!
		@raise: BitInexistent Exception, ValueToLarge Exception
		"""
		if self.DEBUG == True:
			print 'Setting Bit 127.%s (%s) = [%s]' % (bit, self.getBitName127(bit), ReadableAscii(value))
			
		if bit < 1 or bit > 64:
			raise BitInexistent("Bit number %s dosen't exist!" % bit)
			
		# caculate the position insede bitmap
		pos = 1
		
		if   self.getLengthType127(bit) == 'F' :
			self.__setBit127FixedLength(bit, value)
		elif self.getLengthType127(bit) == 'LL':
			self.__setBit127VariableLength(bit, value, 2)
		elif self.getLengthType127(bit) == 'LLL':
			self.__setBit127VariableLength(bit, value, 3)
		elif self.getLengthType127(bit) == 'LLLL':
			self.__setBit127VariableLength(bit, value, 4)
		elif self.getLengthType127(bit) == 'LLLLL':
			self.__setBit127VariableLength(bit, value, 5)
		elif self.getLengthType127(bit) == 'LLLLLL':
			self.__setBit127VariableLength(bit, value, 6)
							
		if (bit % 8) == 0:
			pos = (bit / 8) - 1
		else:
			pos = (bit /8) 

		#need to check if the value can be there .. AN , N ... etc ... and the size
		
		self.BITMAP127[pos] = self.BITMAP127[pos] | self._TMP[ (bit%8) +1]
		
		self.__getRawIso127()
		
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
		
		for c in range(0,16):
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

	def __buildBitmap127(self):
		"""Method that build the bitmap ASCII fr field 127
		It's a internal method, so don't call!
		"""
		
		self.BITMAP127_HEX = ''
		self.BITMAP127_BIN = ''
		
		for c in range(0,8):
			if (self.BITMAP127[0] & self._BIT_POSITION_1) != self._BIT_POSITION_1:
				# Only has the first bitmap
#				if self.DEBUG == True:
#					print '%d Bitmap 127 = %d(Decimal) = %s (hexa) ' %(c, self.BITMAP127[c], hex(self.BITMAP127[c]))	
					
				tm = hex(self.BITMAP127[c])[2:]
				if len(tm) != 2:
					tm = '0' + tm
				self.BITMAP127_HEX += tm
				self.BITMAP127_BIN += chr(self.BITMAP127[c])  
				if c == 7:
					break
				
	################################################################################################	
	
	def __getBitmapFromStr(self, bitmap):
		"""Method that receive a bitmap str and transfor it to ISO8583 object readable.
		@param: bitmap -> bitmap str to be readable
		It's a internal method, so don't call!
		"""
		if self.DEBUG == True:
			print '__getBitmapFromStr(%s)' % ReadableAscii(bitmap)

		#Need to check if the size is correct etc...
		cont = 0
		
		if self.BITMAP_HEX != '':
			self.BITMAP_HEX = ''
			
		self.BITMAP_BIN = ''
		
		for x in range(0,16):
			if (ord(bitmap[0]) & self._BIT_POSITION_1) != self._BIT_POSITION_1: # Only 1 bitmap
				if self.DEBUG == True:
					print 'Token[%d] = %s' %(x, hex(ord(bitmap[x])))
					
				self.BITMAP_BIN += bitmap[x]
				tm = '00' + hex(ord(bitmap[x]))[2:]
				self.BITMAP_HEX += tm[-2:]
				self.BITMAP[cont] = int(tm,16)
				if x == 7:
					break
			else: # Second bitmap
				if self.DEBUG == True:
					print 'Token[%d] = %s' %(x, hex(ord(bitmap[x])))
					
				self.BITMAP_BIN += bitmap[x]
				tm = '00' + hex(ord(bitmap[x]))[2:]
				self.BITMAP_HEX += tm[-2:]
				self.BITMAP[cont] = int(tm,16)
			cont += 1	

	
	################################################################################################

	def __getBitmap127FromStr(self, bitmap):
		"""Method that receive a bitmap str and transfor it to ISO8583 object readable.
		@param: bitmap -> bitmap str to be readable
		It's a internal method, so don't call!
		"""
		if self.DEBUG == True:
			print '__getBitmap127FromStr(%s)' % ReadableAscii(bitmap)

		#Need to check if the size is correct etc...
		cont = 0
		
		if self.BITMAP127_HEX != '':
			self.BITMAP127_HEX = ''
			
		self.BITMAP127_BIN = ''
		
		for x in range(0,7):
			if (ord(bitmap[0]) & self._BIT_POSITION_1) != self._BIT_POSITION_1: # Only 1 bitmap
				if self.DEBUG == True:
					print 'Token[%d] = %s' %(x, hex(ord(bitmap[x])))
					
				self.BITMAP127_BIN += bitmap[x]
				tm = '00' + hex(ord(bitmap[x]))[2:]
				self.BITMAP127_HEX += tm[-2:]
				self.BITMAP127[cont] = int(tm,16)
			cont += 1	

	
	################################################################################################

	def showBitsFromBitmapStr(self, bitmap):
		"""Method that receive a bitmap str, process it, and print a array with bits this bitmap string represents.
		Usualy is used to debug things.
		@param: bitmap -> bitmap str to be analized and translated to "bits"
		"""
		bits = self.__initializeBitsFromBitmapStr(bitmap)
		print 'Bits inside %s  = %s' % (bitmap,bits)	

	################################################################################################	
	
	def __initializeBitsFromBitmapStr(self, bitmap):
		"""Method that receive a bitmap str, process it, and prepare ISO8583 object to understand and "see" the bits and values inside the ISO ASCII package.
		It's a internal method, so don't call!
		@param: bitmap -> bitmap str to be analized and translated to "bits"
		"""
		bits = []
		for c in range(0,16):
			for d in range(1,9):
#				if self.DEBUG == True:
#					print 'Value (%d)-> %s & %s = %s' % (d,self.BITMAP[c] , self._TMP[d], (self.BITMAP[c] & self._TMP[d]) )
				if (self.BITMAP[c] & self._TMP[d]) ==  self._TMP[d]:
					if d == 1: #  e o 8 bit
						if self.DEBUG == True:
							print 'Bit %s is present !!!' % ((c +1)* 8)
						bits.append((c +1)* 8)
						self._VALUES[(c +1)* 8] = 'X'
					else:
						if (c == 0) & (d == 2): # Continuation bit
							if self.DEBUG == True:
								print 'Bit 1 is present !!!' 
								
							bits.append(1)
	
						else:
							if self.DEBUG == True:
								print 'Bit %s is present !!!' % (c * 8 + d - 1)
								
							bits.append(c * 8 + d - 1)
							self._VALUES[c * 8 + d - 1] = 'X'
					
		bits.sort()

		return bits	
	
	################################################################################################

	def __initializeBits127FromBitmapStr(self, bitmap):
		"""Method that receive a bitmap str, process it, and prepare ISO8583 object to understand and "see" the bits and values inside the ISO ASCII package.
		It's a internal method, so don't call!
		@param: bitmap -> bitmap str to be analized and translated to "bits"
		"""
		bits = []
		for c in range(0,8):
			for d in range(1,9):
#				if self.DEBUG == True:
#					print 'Value (%d)-> %s & %s = %s' % (d,self.BITMAP127[c] , self._TMP[d], (self.BITMAP127[c] & self._TMP[d]) )
				if (self.BITMAP127[c] & self._TMP[d]) ==  self._TMP[d]:
					if self.DEBUG == True:
						print 'Bit %s is present !!!' % (c * 8 + d - 1)
						
					bits.append(c * 8 + d - 1)
					self._VALUES127[c * 8 + d - 1] = 'X'
					
		bits.sort()

		return bits	
	
	################################################################################################

	def __getBitsFromBitmap(self):
		"""Method that process the bitmap and return a array with the bits presents inside it.
		It's a internal method, so don't call!
		"""
		bits = []
		for c in range(0,16):
			for d in range(1,9):
#				if self.DEBUG == True:
#					print 'Value (%d)-> %s & %s = %s' % (d,self.BITMAP[c] , self._TMP[d], (self.BITMAP[c] & self._TMP[d]) )
				if (self.BITMAP[c] & self._TMP[d]) ==  self._TMP[d]:
					if d == 1: #  e o 8 bit
						if self.DEBUG == True:
							print 'Bit %s is present !!!' % ((c +1)* 8)
							
						bits.append((c +1)* 8)
					else:
						if (c == 0) & (d == 2): # Continuation bit
							if self.DEBUG == True:
								print 'Bit 1 is present !!!' 
	
							bits.append(1)
	
						else:
							if self.DEBUG == True:
								print 'Bit %s is present !!!' % (c * 8 + d - 1)
								
							bits.append(c * 8 + d - 1)
					
		bits.sort()

		return bits	

	################################################################################################

	def __setBitVariableLength(self, bit, value, length):
		"""Method that set a bit with value in form LL
		It put the size in front of the value
		Example: pack.setBit(99,'123') -> Bit 99 is a LL type, so this bit, in ASCII form need to be 03123. To understand, 03 is the size of the information and 123 is the information/value
		@param: bit -> bit to be setted
		@param: value -> value to be setted
		@raise: ValueToLarge Exception
		It's a internal method, so don't call!
		"""
		
		value = "%s" % value
	
		if len(value) > 10 ** length - 1:
			raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (bit,self.getLengthType(bit),self.getMaxLength(bit)) )
		if len(value) > self.getMaxLength(bit):
			raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (bit,self.getLengthType(bit),self.getMaxLength(bit)) )	
			
		size ="%s"% len(value)	
	
		self._VALUES[bit] = "%s%s" %( size.zfill(length), value)
	
	################################################################################################

	def __setBit127VariableLength(self, bit, value, length):
		"""Method that set a bit with value in form LL
		It put the size in front of the value
		Example: pack.setBit127(2,'123') -> Bit 127.2 is a LL type, so this bit, in ASCII form need to be 03123. To understand, 03 is the size of the information and 123 is the information/value
		@param: bit -> bit to be setted
		@param: value -> value to be setted
		@raise: ValueToLarge Exception
		It's a internal method, so don't call!
		"""
		
		value = "%s" % value
	
		if len(value) > 10 ** length - 1:
			raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (bit,self.getLengthType127(bit),self.getMaxLength127(bit)) )
		if len(value) > self.getMaxLength127(bit):
			raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (bit,self.getLengthType127(bit),self.getMaxLength127(bit)) )	
			
		size ="%s"% len(value)	
	
		self._VALUES127[bit] = "%s%s" %( size.zfill(length), value)
	
	################################################################################################

	def __setBitFixedLength(self, bit, value):
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
	
		if len(value) > self.getMaxLength(bit):
			value = value[0:self.getMaxLength(bit)]
			raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (bit,self.getLengthType(bit),self.getMaxLength(bit)) )
				
		self._VALUES[bit] = value.zfill(self.getMaxLength(bit))
		
	################################################################################################

	def __setBit127FixedLength(self, bit, value):
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
	
		if len(value) > self.getMaxLength127(bit):
			value = value[0:self.getMaxLength127(bit)]
			raise ValueToLarge('Error: value up to size! Bit[%s] of type %s limit size = %s' % (bit,self.getLengthType127(bit),self.getMaxLength127(bit)) )
				
		self._VALUES127[bit] = value.zfill(self.getMaxLength127(bit))
		
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

		for bit in range(0,126):
			if self._VALUES[bit] <> self._EMPTY_VALUE:
				res += '  '
				if   self.getLengthType(bit) == 'LL':
					res += "[LL     "
				elif self.getLengthType(bit) == 'LLL':
					res += "[LLL    "
				elif self.getLengthType(bit) == 'LLLL':
					res += "[LLLL   "
				elif self.getLengthType(bit) == 'LLLLL':
					res += "[LLLLL  "
				elif self.getLengthType(bit) == 'LLLLLL':
					res += "[LLLLLL "
				else:
					res += "[Fixed  "
				res += self.getDataType(bit)
				res += " " * (5 - len(self.getDataType(bit)))
				res += "%6d] " % self.getMaxLength(bit)
				res += ("000%s" % bit)[-3:]
				#PCI-DSS Masking of card holder data
				if bit == 2:	# PAN
					res += " [%s] " % ReadableAscii(self.getBit(bit))
				else:				
					res += " [%s] " % ReadableAscii(self.getBit(bit))				
				res += self.getBitName(bit)
				res += '\n'

		if self._VALUES[127] <> self._EMPTY_VALUE:
			for bit in range(1,64):
				if self._VALUES127[bit] <> self._EMPTY_VALUE:
					res += '  '
					if   self.getLengthType127(bit) == 'LL':
						res += "[LL     "
					elif self.getLengthType127(bit) == 'LLL':
						res += "[LLL    "
					elif self.getLengthType127(bit) == 'LLLL':
						res += "[LLLL   "
					elif self.getLengthType127(bit) == 'LLLLL':
						res += "[LLLLL  "
					elif self.getLengthType127(bit) == 'LLLLLL':
						res += "[LLLLLL "
					else:
						res += "[Fixed  "
					res += self.getDataType127(bit)
					res += " " * (5 - len(self.getDataType127(bit)))
					res += "%6d] " % self.getMaxLength127(bit)
					res += "127." + ("000%s" % bit)[-3:]
					res += " [%s] " % ReadableAscii(self.getBit127(bit))				
					res += self.getBitName127(bit)
					res += '\n'
		
		return res		
				
	################################################################################################

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
		print 'This is the ASCII package %s' % str 
		output (print) -> This is the ASCII package 0800d010800000000000000000002000000001200000000000400001200170299
		
		@return: str with complete ASCII ISO8583
		@raise: InvalidMTI Exception
		"""
		
		self.__buildBitmap()
			
		if self.MESSAGE_TYPE_INDICATION == '':
			raise InvalidMTI('Check MTI! Do you set it?')

		resp = "";
		
		resp += self.MESSAGE_TYPE_INDICATION
		resp += self.BITMAP_BIN
		
		for cont in range(0,128):
			if self._VALUES[cont] <> self._EMPTY_VALUE:
				resp = "%s%s"%(resp, self._VALUES[cont]) 
		
		return resp
	
	################################################################################################

	def __getRawIso127(self):
		"""Method that builds ISO8583 Field 127 ASCII complete representation
		"""
		
		self.__buildBitmap127()
			
		resp = "";
		
		resp += self.BITMAP127_BIN
		
		for cont in range(0,64):
			if self._VALUES127[cont] <> self._EMPTY_VALUE:
				resp = "%s%s"%(resp, self._VALUES127[cont]) 
		
		if self.BITMAP127_HEX != "0000000000000000":
			self.setBit(127, resp)
	
	################################################################################################	

	def __setMTIFromStr(self, iso):
		"""Method that get the first 4 characters to be the MTI. 
		It's a internal method, so don't call!
		"""
		if self.DEBUG == True:
			print '__setMTIFromStr(%s)' % ReadableAscii(iso)
		
		self.MESSAGE_TYPE_INDICATION = iso[0:4]
		
		if self.DEBUG == True:
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

	def __getBitFromStr(self,strWithoutMtiBitmap):
		"""Method that receive a string (ASCII) without MTI and Bitmaps (first and second), understand it and remove the bits values
		@param: str -> with all bits presents whithout MTI and bitmap
		It's a internal method, so don't call!
		"""
	
		if self.DEBUG == True:
			print '__getBitFromStr(%s)' % ReadableAscii(strWithoutMtiBitmap)
			
		offset = 0;
		# jump bit 1 because it was alread defined in the "__initializeBitsFromBitmapStr"
		for cont in range(2,128):
			if self._VALUES[cont] <> self._EMPTY_VALUE:
				if self.DEBUG == True:
					print 'String = %s offset = %s bit = %s' % (strWithoutMtiBitmap[offset:],offset,cont)
					
				lengthIndicator = 0
				if   self.getLengthType(cont) == 'LL':
					lengthIndicator = 2
				elif self.getLengthType(cont) == 'LLL':
					lengthIndicator = 3
				elif self.getLengthType(cont) == 'LLLL':
					lengthIndicator = 4
				elif self.getLengthType(cont) == 'LLLLL':
					lengthIndicator = 5
				elif self.getLengthType(cont) == 'LLLLLL':
					lengthIndicator = 6

				if lengthIndicator >= 2:
					valueSize = int(strWithoutMtiBitmap[offset:offset + lengthIndicator])
					if self.DEBUG == True:
						print 'Variable Length Field (%s) Size = [%s]' % ('L'*lengthIndicator, valueSize)
						
					if valueSize > self.getMaxLength(cont):
						raise ValueToLarge("This bit is larger than the especification!")
					self._VALUES[cont] = strWithoutMtiBitmap[offset:offset+lengthIndicator]+strWithoutMtiBitmap[offset + lengthIndicator:offset+lengthIndicator+valueSize]
					
					if self.DEBUG == True:
						print '\tSetting bit [%s] Value=[%s]' % (cont,self._VALUES[cont])
					
					offset += valueSize + lengthIndicator
				else:
					# Fixed Length Field
					self._VALUES[cont] = strWithoutMtiBitmap[offset:self.getMaxLength(cont)+offset]
					
					if self.DEBUG == True:
						print 'Fixed Length Field Size = [%s]' % (self.getMaxLength(cont))
						print '\tSetting bit [%s] Value=[%s]' % (cont,self._VALUES[cont])
					
					offset += self.getMaxLength(cont)
		
	################################################################################################	

	def __getBit127FromStr(self,strWithoutMtiBitmap):
		"""Method that receive a string (ASCII) without MTI and Bitmaps (first and second), understand it and remove the bits values
		@param: str -> with all bits presents whithout MTI and bitmap
		It's a internal method, so don't call!
		"""
	
		if self.DEBUG == True:
			print '__getBit127FromStr(%s)' % ReadableAscii(strWithoutMtiBitmap)
			
		offset = 0;
		# jump bit 1 because it was alread defined in the "__initializeBitsFromBitmapStr"
		for cont in range(2,64):
			if self._VALUES127[cont] <> self._EMPTY_VALUE:
				if self.DEBUG == True:
					print 'String = %s offset = %s bit = %s' % (strWithoutMtiBitmap[offset:],offset,cont)
					
				lengthIndicator = 0
				if   self.getLengthType127(cont) == 'LL':
					lengthIndicator = 2
				elif self.getLengthType127(cont) == 'LLL':
					lengthIndicator = 3
				elif self.getLengthType127(cont) == 'LLLL':
					lengthIndicator = 4
				elif self.getLengthType127(cont) == 'LLLLL':
					lengthIndicator = 5
				elif self.getLengthType127(cont) == 'LLLLLL':
					lengthIndicator = 6

				if lengthIndicator >= 2:
					valueSize = int(strWithoutMtiBitmap[offset:offset + lengthIndicator])
					if self.DEBUG == True:
						print 'Variable Length Field (%s) Size = [%s]' % ('L'*lengthIndicator, valueSize)
						
					if valueSize > self.getMaxLength127(cont):
						raise ValueToLarge("This bit is larger than the especification!")
					self._VALUES127[cont] = strWithoutMtiBitmap[offset:offset+lengthIndicator]+strWithoutMtiBitmap[offset + lengthIndicator:offset+lengthIndicator+valueSize]
					
					if self.DEBUG == True:
						print '\tSetting bit [%s] Value=[%s]' % (cont,self._VALUES127[cont])
					
					offset += valueSize + lengthIndicator
				else:
					# Fixed Length Field
					self._VALUES127[cont] = strWithoutMtiBitmap[offset:self.getMaxLength127(cont)+offset]
					
					if self.DEBUG == True:
						print 'Fixed Length Field Size = [%s]' % (self.getMaxLength127(cont))
						print '\tSetting bit [%s] Value=[%s]' % (cont, self._VALUES127[cont])
					
					offset += self.getMaxLength127(cont)
		
	################################################################################################	
	
	def setIsoContent(self, iso):
		"""Method that receive a complete ISO8583 string (ASCII) understand it and remove the bits values
		Example:
			iso = '0210B238000102C080040000000000000002100000000000001700010814465469421614465701081100301000000N399915444303500019991544986020   Value not allowed009000095492'
			i2 = ISO8583()
			# in this case, we need to redefine a bit because default bit 42 is LL and in this especification is "N"
			# the rest remain, so we use "get" :)
			i2.redefineBit(42, '42', i2.getBitName(42), 'N', i2.getMaxLength(42), i2.getDataType(42) )
			i2.setIsoContent(iso2)
			print 'Bitmap = %s' %i2.getBitmap() 
			print 'MTI = %s' %i2.getMTI() 

			print 'This ISO has bits:'
			v3 = i2.getBitsAndValues()
			for v in v3:
				print 'Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value'])
				
		@param: str -> complete ISO8583 string
		@raise: InvalidIso8583 Exception
		"""
		if len(iso) < 20:
			raise InvalidIso8583('This is not a valid iso!!')
		if self.DEBUG == True:
			print 'setIsoContent(%s)' % ReadableAscii(iso)
			
		self.__setMTIFromStr(iso)
		#Cut off the MTI and process the rest of the message
		isoT = iso[4:]

		self.__getBitmapFromStr(isoT)
		self.__initializeBitsFromBitmapStr(self.BITMAP_HEX)
		if self.DEBUG == True:
			print '_VALUES (before) %s ' % self._VALUES
		self.__getBitFromStr(iso[4+len(self.BITMAP_HEX)/2:])	
		if self.DEBUG == True:
			print '_VALUES (after) %s ' % self._VALUES
		
		if self._VALUES[127] != self._EMPTY_VALUE:
			iso127 = self.getBit(127)
			if self.DEBUG:
				print 'iso127 = [%s]' % ReadableAscii(iso127)
			self.__getBitmap127FromStr(iso127)
			self.__initializeBits127FromBitmapStr(self.BITMAP127_HEX)
			if self.DEBUG == True:
				print '_VALUES127 (before) %s ' % self._VALUES127
			self.__getBit127FromStr(iso127[1+len(self.BITMAP127_HEX)/2:])	
			if self.DEBUG == True:
				print '_VALUES127 (after) %s ' % self._VALUES127
					
	################################################################################################
	
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
				print 'Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value'])
	
		@return: array of values.
		"""
		ret = []
		for cont in range(2,126):
			if self._VALUES[cont] != self._EMPTY_VALUE:
				_TMP = {}
				_TMP['bit'] =  "%d" % cont
				_TMP['type'] = self.getLengthType(cont)
				_TMP['value'] = self.getBit(cont)
				ret.append(_TMP)
		if self._VALUES[127] != self._EMPTY_VALUE:
			for cont in range(2,63):
				if self._VALUES127[cont] <> self._EMPTY_VALUE:
					_TMP = {}
					_TMP['bit'] =  "127.%d" % cont
					_TMP['type'] = self.getLengthType127(cont)
					_TMP['value'] = self.getBit127(cont)
					ret.append(_TMP)
		return ret
		
	################################################################################################	
	
	def getBit(self,bit):
		"""Return the value of the bit
		@param: bit -> the number of the bit that you want the value
		@raise: BitInexistent Exception, BitNotSet Exception
		"""
		
		if bit < 1 or bit > 128:
			raise BitInexistent("Bit number %s dosen't exist!" % bit)	

		if self._VALUES[bit] == self._EMPTY_VALUE:
			raise BitNotSet("Bit number %s was not set!" % bit)	
			
		if   self.getLengthType(bit) == "LL":
			value = self._VALUES[bit][2:]
		elif self.getLengthType(bit) == "LLL":
			value = self._VALUES[bit][3:]
		elif self.getLengthType(bit) == "LLLL":
			value = self._VALUES[bit][4:]
		elif self.getLengthType(bit) == "LLLLL":
			value = self._VALUES[bit][5:]
		elif self.getLengthType(bit) == "LLLLLL":
			value = self._VALUES[bit][6:]
		else:
			value = self._VALUES[bit]
		
		return value
		
	################################################################################################	

	def getBit127(self,bit):
		"""Return the value of the bit
		@param: bit -> the number of the bit that you want the value
		@raise: BitInexistent Exception, BitNotSet Exception
		"""
		
		if bit < 1 or bit > 128:
			raise BitInexistent("Bit number %s dosen't exist!" % bit)	

		if self._VALUES127[bit] == self._EMPTY_VALUE:
			raise BitNotSet("Bit number %s was not set!" % bit)	
			
		if   self.getLengthType127(bit) == "LL":
			value = self._VALUES127[bit][2:]
		elif self.getLengthType127(bit) == "LLL":
			value = self._VALUES127[bit][3:]
		elif self.getLengthType127(bit) == "LLLL":
			value = self._VALUES127[bit][4:]
		elif self.getLengthType127(bit) == "LLLLL":
			value = self._VALUES127[bit][5:]
		elif self.getLengthType127(bit) == "LLLLLL":
			value = self._VALUES127[bit][6:]
		else:
			value = self._VALUES127[bit]
		
		return value
		
	################################################################################################	
		
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
			print 'This <%s> the same that <%s>' % (iso.getNetworkISO(),netIso)
		
		@param: bigEndian (True|False) -> if you want that the size be represented in this way. 
		@return: size + ASCII ISO8583 package ready to go to the network!
		@raise: InvalidMTI Exception
		"""
		
		netIso = ""
		asciiIso = self.getRawIso()
		
		if bigEndian:
			netIso = struct.pack('!h',len(asciiIso))
			if self.DEBUG == True:
				print 'Pack Big-endian'
		else:
			netIso = struct.pack('<h',len(asciiIso))
			if self.DEBUG == True:
				print 'Pack Little-endian'

		netIso += asciiIso
		
		return netIso

	################################################################################################		
	
	def setNetworkISO(self,iso, bigEndian=True):
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
				print 'Bit %s Type %s Value = %s' % (v['bit'],v['type'],v['value'])
			
			@param: iso -> str that represents size + ASCII ISO8583 package
			@param: bigEndian (True|False) -> Codification of the size.
			@raise: InvalidIso8583 Exception
		"""
		
		if len(iso) < 24:
			raise InvalidIso8583('This is not a valid iso!!Invalid Size')
		
		size = iso[0:2]
		if bigEndian:
			size = struct.unpack('!h',size)
			if self.DEBUG == True:
				print 'Unpack Big-endian'
		else:
			size = struct.unpack('<h',size)
			if self.DEBUG == True:
				print 'Unpack Little-endian'
		
		if len(iso) != (size[0] + 2):
			raise InvalidIso8583('This is not a valid iso!!The ISO8583 ASCII(%s) is less than the size %s!' % (len(iso[2:]),size[0]))
			
		self.setIsoContent(iso[2:])	
	
	################################################################################################
	
def ReadableAscii(s):
	"""
	Print readable ascii string, non-readable characters are printed as periods (.)
	"""
	r = ''
	for c in s:
		if ord(c) >= 32 and ord(c) <= 126:
			r += c
		else:
			r += '.'
	return r
			
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
	# Remove TCP length indicator
	s = s[2:]
	while s != '':
		part = s[:16]
		s = s[16:]


	
if __name__ == '__main__':
	iso = ISO8583(debug=True)
	iso.setMTI('0800')
	#Set a Fixed Length Field
	iso.setBit(3,  '123456')	
	#Set a LL Variable Length Field
	iso.setBit(2,  '12222221')
	iso.setBit127(2, '321')

	print iso.dumpFields()
	v1 = iso.getBitsAndValues()
	for v in v1:
		print 'Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value'])
	
	message = iso.getNetworkISO()
	print "message = [%s]" % (ReadableAscii(message))
	print BinaryDump(message)

	print "-"*120
	isoAns = ISO8583(debug=True)
	isoAns.setNetworkISO(message)
	print isoAns.dumpFields()
