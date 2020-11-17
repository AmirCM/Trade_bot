from ippanel import Client
import math
import random


def opt_generator(length):
    digits = "0123456789"
    OTP = ""
    for i in range(length):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


class SMS:
    def __init__(self):
        api_key = "YMQm7ifbEWxFEcStuyBA7yppiRJFgLjBioWOxdU8P1c="
        self.sms = Client(api_key)

    def send(self, phone):
        code = opt_generator(5)

        bulk_id = self.sms.send(
            "+9810000385",  # originator
            [phone],  # recipients
            "Verification code: \n Keep Money"  # message
        )
        print('Sent ', bulk_id)
        return '82463'


"""
pattern_values = {
    "code": "LOVE YOU",
}

bulk_id = sms.send_pattern(
    "1em8y4ixzv",    # pattern code
    "+98sim",      # originator
    "09210118403",  # recipient
    pattern_values,  # pattern values
)"""
