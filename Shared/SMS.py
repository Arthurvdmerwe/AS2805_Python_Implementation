import datetime

from twilio.rest import TwilioRestClient


class SMS:

    def __init__(self, Message):

        try:
            self.CellNumber = "+61405025365"
            text = "%s\n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            text += Message
            self.account_sid = "AC6a4a68fa058d4a3c8a9e1c53f6a0235f"
            self.auth_token = "d24efcc4ad310535ae9776d26ed05020"
            client = TwilioRestClient(self.account_sid, self.auth_token)
            self.Message = text


        except:
            pass

if __name__ == "__main__":
    sms =  "SMS System:\n"
    sms += "This is a test"
    
    SMS(sms)