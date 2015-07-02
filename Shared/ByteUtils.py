import logging
import string

FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])
	
def ByteToHex( byteStr ):
	"""
	Convert a byte string to it's hex string representation e.g. for output.
	"""

	# Uses list comprehension which is a fractionally faster implementation than
	# the alternative, more readable, implementation below
	#
	#    hex = []
	#    for aChar in byteStr:
	#        hex.append( "%02X " % ord( aChar ) )
	#
	#    return ''.join( hex ).strip()

	return ''.join( [ "%02X" % ord( x ) for x in byteStr ] ).strip()

#-------------------------------------------------------------------------------

def HexToByte( hexStr ):
	"""
	Convert a string hex byte values into a byte string. The Hex Byte values may
	or may not be space separated.
	"""
	if len(hexStr) % 2 == 1: hexStr += "0"
	return hexStr.decode("hex")
		
def dump(src, length=16):
	"""
	Dump function
	"""
	N=0; result=''
	while src:
		s,src = src[:length],src[length:]
		if length != 16:
			hexa = ' '.join(["%02x"%ord(x) for x in s[:8]])
			hexa += ' | '
			hexa += ' '.join(["%02x"%ord(x) for x in s[8:]])
		else:
			hexa = ' '.join(["%02x"%ord(x) for x in s])
		s = s.translate(FILTER)
		result += "%08x:  %-*s   %s\n" % (N, length*3, hexa, s)
		N+=length
	return result
	
UTILS_valid_ascii = string.digits + \
			  string.letters + \
			  string.punctuation


def to_ascii(s,short=False):
	l=[]
	for c in s:
		if c in UTILS_valid_ascii:
			l.append(c)
			if not short: l.append(' ')
		else:
			l.append(".")
			if not short: l.append('.')
	return "".join(l)
	
def log_bit(v, iso, logger=logging.getLogger()):
	bit = int(v['bit'])
	#if ( v['type'] in ['LL','LLL'] and len(v['value']) > 128 ):
	#	value = "\n" + dump(HexToByte(v['value']))
	#else:
	#	value = str(v['value'])
	value = v['value']
	logger.info('[%-02d] %s:\t%r' % ( bit, iso.getLargeBitName(bit), value))