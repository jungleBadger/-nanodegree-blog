#!/usr/bin/env python
from flask import render_template, make_response, redirect, request
from handlers.datastore import Datastore
from handlers.security import Security
from handlers.home import Home
class Login:
    def __init__(self):
        self.datastore = Datastore()
        self.security = Security()
        self.home = Home()
        self.page_path = 'login.html'


    def render_page(self, error='', username=''):
        if 'user_session' in request.cookies:
            return redirect('/')
        else:
            return render_template(self.page_path,
                                   error=error,
                                   username=username)


    def do_login(self, username='', password=''):
        error = ''
        if username == '' or password == '':
            error = "Can not proceed without username or password"

        user = self.datastore.do_query('User', 'username', username)
        if user == 0 or not user or not self.security.validate_password(password, user[0].get('password')):
            error = "Invalid credentials"
        if error:
            return self.render_page(error, username)
        else:
            response = make_response(redirect('/'))
            self.security.set_cookie(response, username)
            return response