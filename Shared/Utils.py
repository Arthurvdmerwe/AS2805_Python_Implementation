import ConfigParser
import string
from decimal import Decimal

def LoadConfig(file, log, config=None):
    """
    returns a dictionary with key's of the form
    <section>.<option> and the values 
    """
    if not config: config = {}
    log.debug('LoadConfig(%s)' % file)
    config = config.copy()
    cp = ConfigParser.ConfigParser()
    cp.read(file)
    for sec in cp.sections():
        name = string.lower(sec)
        for opt in cp.options(sec):
            config[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
    return config


def StrToDecimal(value):
    if value == "":
        return Decimal("0.00")
    else:
        return Decimal("%s.%s" % (value[:-2], value[-2:]))


def ParseTrack2(Track2):

    separator = Track2.find('=')

    PAN = Track2[0:separator]
    ExpiryYYMM = Track2[separator + 1:separator + 5]
    ServiceCode = Track2[separator + 5:separator + 8]
    endSentinal = Track2.__len__()
    Cleaned = Track2[0:endSentinal].replace('=', 'D')
    Discretionary = Track2[separator + 8:endSentinal]
    Part2 = Track2[separator:]
    BIN = Track2[0:6]
    return {"PAN": PAN, "ExpiryYYMM": ExpiryYYMM, "ServiceCode": ServiceCode, "Cleaned": Cleaned,
            "Discretionary": Discretionary, "Part2": Part2, "BIN": BIN}


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


def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0

def calculate_luhn(partial_card_number):
    check_digit = luhn_checksum(int(partial_card_number) * 10)
    return check_digit if check_digit == 0 else 10 - check_digit

if __name__ == '__main__':
    track2 = ';4103750002189015=13062060000001134000?'
    print track2
    print ParseTrack2(track2)
    