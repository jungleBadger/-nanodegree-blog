#!/usr/bin/env python
from flask import render_template, request
from handlers.security import Security
class Home:
    def __init__(self):
        self.page_path = 'home.html'
        self.security = Security()


    def render_page(self, error='', username=''):
        if 'user_session' in request.cookies:
            username = self.security.read_secure_cookie(request.cookies.get('user_session'))
        return render_template(self.page_path,
                               error=error,
                               username=username)