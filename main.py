#!/usr/bin/env python
# [START app]
import logging
import sys
import os
from flask import Flask, request, redirect, Response
from livereload import Server
from handlers.signup import Signup
from handlers.login import Login
from handlers.logout import Logout
from handlers.home import Home
from handlers.post import Post
from handlers.security import Security
import base64
import datetime

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
           methods=['POST', 'GET'])
def logout_handler():
    return logout.do_logout()


@app.route('/',
           methods=['GET'])
def home_handler():
    permission = security.check_permission(accept_anonymous=True)
    if (permission and permission.get('status') == 1):
        latest_posts = post.query_latest_posts()
        return home.render_page(error='', username=permission.get('username'), posts=latest_posts)
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
            image = ''
            if (request.files['image']):
                image = base64.b64encode(request.files['image'].read()).decode()
            operation_result = 0
            if request.form.get('post_id'):
                operation_result = post.edit_post(request.form.get('post_id'),
                                      permission.get('username'),
                                      request.form.get('title'),
                                      image,
                                      request.form.get('text'),
                                      request.form.get('tag'))
            else:
                operation_result = post.create_post(permission.get('username'),
                                        request.form.get('title'),
                                        image,
                                        request.form.get('text'),
                                        request.form.get('tag'))

            if operation_result and operation_result.get('status') == 1:
                return redirect('/post?id=%s' % operation_result.get('post_id'))
            else:
                return operation_result.get('response')
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
                if post_to_view != 0:
                    return post.render_view_page(post=post_to_view, error='', username=permission.get('username'))

            return "Post not found"
    else:
        return permission.get('response')


@app.route('/addComment',
           methods=['POST'])
def comment_handler():
    permission = security.check_permission()
    if (permission and permission.get('status') == 1):
        operation_result = post.comment_post(request.form.get('post_id'),
                          permission.get('username'),
                          request.form.get('comment'))
        if operation_result == 1:
            return redirect('/post?id=%s' % request.form.get('post_id'))
        else:
            return operation_result

    else:
        return "Only logged users can perform this operation"


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.route('/worker',
           methods=['GET'])
def worker_handler():
    return Response(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'service-worker.js')).read(), mimetype='text/javascript')


@app.template_filter('ctime')
def timectime(s):
    return datetime.datetime.fromtimestamp(s / 1e3).strftime("%Y-%m-%d %H:%M")


@app.template_filter('postlimit')
def timectime(string):
    return string[:50] + '...'


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