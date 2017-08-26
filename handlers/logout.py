#!/usr/bin/env python
from flask import make_response, redirect
from handlers.security import Security


class Logout:
    def __init__(self):
        self.data = []
        self.security = Security()

    def do_logout(self, redirect_path='/'):
        response = make_response(redirect(redirect_path))
        self.security.clear_cookie(response)
        return response