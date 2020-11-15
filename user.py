class User:
    def __init__(self, username, phone):
        self.username = username
        self.phone = phone
        self.is_auth = False
        self.is_joined = False
