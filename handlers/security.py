#!/usr/bin/env python
import bcrypt
import hmac
class Security:
    def __init__(self, secret='super_secret', salt_rounds=12, cookie_name='user_session'):
        self.SECRET = secret
        self.SALT_ROUNDS = salt_rounds
        self.cookie_name = cookie_name

    def validate_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)


    def generate_hash(self, raw):
        return bcrypt.hashpw(raw.encode('utf-8'), bcrypt.gensalt(self.SALT_ROUNDS))


    def make_secure_cookie(self, raw):
        return '%s|%s' % (raw, hmac.new(self.SECRET.encode('utf-8'), raw.encode('utf-8')).hexdigest())


    def clear_cookie(self, response):
        response.set_cookie(self.cookie_name, '', expires=0)


    def set_cookie(self, response, username = ''):
        if username:
            cookie_val = self.make_secure_cookie(username)
            response.set_cookie('%s=%s; Path=/' % (self.cookie_name, cookie_val))


    def read_secure_cookie(self, cookie):
        if cookie:
            cookie_val = cookie.split('|')
            username = cookie_val[0]
            if cookie == self.make_secure_cookie(username):
                return username