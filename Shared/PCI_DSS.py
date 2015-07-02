def PCI_Mask_PAN(pan):
    """
    Return a masked PAN based on PCI-DSS specifications
    The length of the result will match the original length of the PAN
    input  = 123456112233447890 
    result = 123456********7890
    """
    return pan[:6] + ("*" * (len(pan) - 10)) + pan[-4:]


if __name__ == '__main__':
    pass