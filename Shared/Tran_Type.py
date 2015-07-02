__author__ = 'root'
Tran = {'0100': 'Network Management Request', '0200': 'Financial Message Request',
        '0300': 'File Actions Message Request', '0400': 'Reversal / Chargeback Message Request',
        '0500': 'Reconciliation Message Request', '0600': 'Administrative Message Request',
        '0700': 'Fee Collection Message Request', '0800': 'Network Management Message Request',
        '0110': 'Network Management Request Response', '0210': 'Financial Message Request Response',
        '0310': 'File Actions Message Request Response', '0410': 'Reversal / Chargeback Message Request Response',
        '0510': 'Reconciliation Message Request Response', '0610': 'Administrative Message Request Response',
        '0710': 'Fee Collection Message Request Response', '0810': 'Network Management Message Request Response',
        '0120': 'Network Management Advice', '0220': 'Financial Message Advice', '0320': 'File Actions Message Advice',
        '0420': 'Reversal / Chargeback Message Advice', '0520': 'Reconciliation Message Advice',
        '0620': 'Administrative Message Advice', '0720': 'Fee Collection Message Advice',
        '0820': 'Network Management Message Advice', '0130': 'Network Management Advice Response',
        '0230': 'Financial Message Advice Response', '0330': 'File Actions Message Advice Response',
        '0430': 'Reversal / Chargeback Message Advice Response', '0530': 'Reconciliation Message Advice Response',
        '0630': 'Administrative Message Advice Response', '0730': 'Fee Collection Message Advice Response',
        '0830': 'Network Management Message Advice Response'}


def GetMessagesescription(mti):
    return mti + ':' + Tran[mti]