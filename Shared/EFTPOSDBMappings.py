"""
This file maps the database field names with the AS2805 bit numbers
"""

import MySQLdb


AS2805_to_DB = {"2": "p2_pan", "3": "p3_processing_code", "4": "p4_amount_tran", "5": "p5_amount_settlement",
                "6": "p6_amount_billing", "7": "p7_transmit_dt", "9": "p9_conversion_rate_settlement",
                "10": "p10_conversion_rate_billing", "11": "p11_stan", "12": "p12_time_local_tran",
                "13": "p13_date_local_tran", "14": "p14_date_expiration", "15": "p15_date_settlement",
                "16": "p16_date_conversion", "18": "p18_merchant_type", "22": "p22_pos_entry_mode",
                "23": "p23_card_seq_no", "25": "p25_pos_condition_code", "28": "p28_amt_tran_fee",
                "32": "p32_acq_inst_id", "33": "p33_fwd_inst_id", "35": "p35_track2", "37": "p37_ret_ref_no",
                "38": "p38_auth_id_response", "39": "p39_response_code", "41": "p41_terminal_id",
                "42": "p42_card_acceptor_id", "43": "p43_name_location", "44": "p44_additional_response_data",
                "47": "p47_additional_response_national", "48": "p48_additional_response_private", "49": "p49_currency",
                "50": "p50_currency_settle", "51": "p51_currency_biling", "52": "p52_pin_block",
                "53": "p53_security_block", "54": "p54_aditional_amounts", "55": "p55_icc_data",
                "57": "p57_amount_cash", "58": "p58_ledger_balance", "59": "p59_account_balance", "64": "p64_mac",
                "66": "p66_settlement_code", "70": "p70_network_mgt_info_code", "74": "p74_credits_no",
                "75": "p75_credits_rev_no", "76": "p76_debits_no", "77": "p77_debits_rev_no", "78": "p78_transfers_no",
                "79": "p79_transfers_rev_no", "80": "p80_inquiries_no", "81": "p81_auths_no",
                "83": "p83_credits_tran_fee", "85": "p85_debits_tran_fee", "86": "p86_credits_amt",
                "87": "p87_credits_rev_amt", "88": "p88_debits_amt", "89": "p89_debits_rev_amt",
                "90": "p90_original_data", "97": "p97_amt_net_settle", "99": "p99_settle_id_code",
                "100": "p100_receving_id_code", "112": "p112_key_mng_data", "118": "p118_cash_no",
                "119": "p119_cash_amount", "128": "p128_mac_extended", "125": "p125_network_management_info"}


def BuildISOInsertFieldAndValues(log, iso, extra=None):
    """
    Builds an insert statement to save all the fields from an AS2805 message into the database.eftpos_terminals table
    extra = a dictionary with extra field/value pairs that you want to insert that is not part of the ISO message
    """
    if not extra: extra = {}
    v1 = iso.getBitsAndValues()
    field_list = ''
    value_list = ''
    fields_in_row = 0
    for v in v1:
        # log.debug('Bit %s of type %s with value = %s' % (v['bit'], v['type'], v['value']))
        # Add a comma between the fields
        try:
            field_name = AS2805_to_DB[v['bit']]
            if field_list != '':
                fields_in_row += 1
                field_list += ', '
                value_list += ', '
                # Add a new line every 5 fields.
            if fields_in_row >= 5:
                field_list += '\n  '
                value_list += '\n  '
                fields_in_row = 0
            field_list += field_name
            value_list += '"' + MySQLdb.escape_string(v['value']) + '"'
        except KeyError as e:
            log.critical("DB Field Mapping does not exist %s" % e)

    for extra_field in extra.keys():
        field_list += ',\n  %s' % extra_field
        v = str(extra[extra_field])
        value_list += ',\n   "%s"' % MySQLdb.escape_string(v)

        # Chop off the extra comma's if there are extra fields
    # if extra != {}:
    # field_list = field_list[:-2]
    #        value_list = value_list[:-2]

    sql = 'INSERT INTO eftpos_terminals (\n'
    sql += '  message,\n'
    sql += '  ' + field_list + ')\n'
    sql += 'VALUES (\n'
    sql += '  "%s",\n' % (iso.getMTI())
    sql += '  ' + value_list + ')'
    return sql
