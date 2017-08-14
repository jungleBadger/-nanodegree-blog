#!/usr/bin/env python
# [START app]
import logging
import sys
from flask import Flask, request
from livereload import Server
from handlers.signup import Signup
from handlers.login import Login
from handlers.logout import Logout
from handlers.home import Home

app = Flask(__name__)


@app.route("/login",
           methods=['GET', 'POST'])
def login_handler():
    if request.method == 'POST':
        Login().do_login(request.form.get('username'),
                         request.form.get('password'))
    elif request.method == 'GET':
        return Login().render_page()


@app.route("/signup",
           methods=['GET', 'POST'])
def signup_handler():
    if request.method == 'GET':
            return Signup().render_page()
    elif request.method == 'POST':
        return Signup().signup(request.form.get('username'),
                               request.form.get('password'),
                               request.form.get('verify'),
                               request.form.get('email'))

@app.route("/logout",
           methods=['POST'])
def logout_handler():
    Logout().do_logout()


@app.route('/',
           methods=['GET'])
def home_handler():
    return Home().render_page('')


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "local":
        server = Server(app.wsgi_app)
        server.watch('main.py')
        server.serve()
    else:
        app.run(host='127.0.0.1', port=8080, debug=True)


if __name__ == '__main__':
    main()
# [END app]