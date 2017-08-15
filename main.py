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
from handlers.post import Post
from handlers.security import Security

app = Flask(__name__)
signup = Signup()
login = Login()
logout = Logout()
home = Home()
post = Post()
security = Security()

@app.route("/login",
           methods=['GET', 'POST'])
def login_handler():
    if request.method == 'POST':
        return login.do_login(request.form.get('username'),
                         request.form.get('password'))
    elif request.method == 'GET':
        return login.render_page()


@app.route("/signup",
           methods=['GET', 'POST'])
def signup_handler():
    if request.method == 'GET':
        return signup.render_page()
    elif request.method == 'POST':
        return signup.create_account(request.form.get('username'),
                               request.form.get('password'),
                               request.form.get('verify'),
                               request.form.get('email'))


@app.route('/logout',
           methods=['POST'])
def logout_handler():
    return logout.do_logout()


@app.route('/',
           methods=['GET'])
def home_handler():
    permission = security.check_permission(accept_anonymous=True)
    if (permission and permission.get('status') == 1):
        return home.render_page('', permission.get('username'))
    else:
        return permission.get('response')


@app.route('/post/manipulate',
           methods=['GET', 'POST'])
def manipulate_post_handler():
    permission = security.check_permission()
    if (permission and permission.get('status') == 1):
        if request.method == 'GET':
            post_id = request.args.get('id')
            if post_id:
                post_to_be_edited = post.query_post_by_id(post_id)
                if post_to_be_edited:
                    if (permission.get('username') == post_to_be_edited.get("author")):
                        return post.render_edit_page('', permission.get('username'), post_to_be_edited)
                    else:
                        return "Unauthorized operation"

            return post.render_edit_page('', permission.get('username'))
        else:
            return post.create_post(permission.get('username'),
                                    request.form.get('title'),
                                    request.form.get('image'),
                                    request.form.get('text'),
                                    request.form.get('tag'))
    else:
        return permission.get('response')



@app.route('/post',
           methods=['GET'])
def post_handler():
    permission = security.check_permission(accept_anonymous=True)
    if (permission and permission.get('status') == 1):
        if request.method == 'GET':
            post_id = request.args.get('id')
            if post_id:
                post_to_view = post.query_post_by_id(post_id)
                if post_to_view:
                    return post.render_view_page('', permission.get('username'), post_to_view)

            return "Post not found"
    else:
        return permission.get('response')


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