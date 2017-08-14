#!/usr/bin/env python
from flask import render_template, request, make_response
from handlers.security import Security
from handlers.logout import Logout
class Home:
    def __init__(self):
        self.page_path = 'home.html'
        self.security = Security()
        self.logout = Logout()


    def render_page(self, error='', username=''):
        if 'user_session' in request.cookies:
            username = self.security.read_secure_cookie(request.cookies.get('user_session'))
            if not username:
                response = make_response(render_template(self.page_path,
                               error=error,
                               username=username))
                self.security.clear_cookie(response)
                return response
        return render_template(self.page_path,
                               error=error,
                               username=username)