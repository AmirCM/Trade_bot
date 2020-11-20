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

        pattern_values = {"code": code}
        bulk_id = self.sms.send_pattern(
            "4tprjx5g44",  # pattern code
            "+9810000385",  # originator
            phone,  # recipient
            pattern_values,  # pattern values
        )
        print('Sent ', bulk_id)
        return code

