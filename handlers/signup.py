#!/usr/bin/env python
from flask import render_template
from handlers.datastore import Datastore
from handlers.security import Security
class Signup:
    def __init__(self):
        self.datastore = Datastore()
        self.security = Security()
        self.page_path = 'signup.html'


    def render_page(self, error='', username='', password='', verified_password='', email=''):
        return render_template(self.page_path,
                               error=error,
                               username=username,
                               password=password,
                               verify=verified_password,
                               email=email)


    def signup(self, username='', password='', verified_password='', email=''):
        error = ''
        if username == '' or password == '' or email == '':
            error = "Can not proceed without username or password"
        elif len(password) < 6 or len(password) > 16:
            error = "Invalid password"
        elif password != verified_password:
            error = "Password dont match"
        elif self.datastore.do_query('User', 'username', username) != 0:
            return "User already exists"
        elif self.datastore.do_query('User', 'email', email) != 0:
            error = "Email already in use"
        user = self.datastore.create_entity(username)
        user['username'] = username
        user['password'] = self.security.generate_hash(password)
        user['email'] = email
        self.datastore.save_object(user)
        if error:
            # I dont like the approach of returning rendered pages as results of operations such
            # as login and signup. I believe that we need to send http status and error identifier to be consumed
            # as generic as possible so we can use it on a mobile app for instance along with web app.
            #  But the challenge ask for a solution using templates and this sort of stuff.
            # return signupStatus, 403
            self.render_page(error, username, password, verified_password, email)
        else:
            return "User created successfully", 201