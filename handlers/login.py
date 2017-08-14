#!/usr/bin/env python
from flask import render_template
from handlers.datastore import Datastore
from handlers.security import Security
class Login:
    def __init__(self):
        self.datastore = Datastore()
        self.security = Security()
        self.page_path = 'login.html'


    def render_page(self, error='', username=''):
        return render_template(self.page_path,
                               error=error,
                               username=username)


    def do_login(self, username='', password=''):
        error = ''
        if username == '' or password == '':
            error = "Can not proceed without username or password"
        user = self.datastore.do_query('User', 'username', username)[0]
        if not user or not self.security.validate_password(password, user.get('password')):
            error = "Invalid credentials"

        self.render_page(error, username)