#!/usr/bin/env python

# [START app]
import logging
from flask import Flask, render_template, request, redirect
from livereload import Server
from google.cloud import datastore
import bcrypt
import sys

app = Flask(__name__)


# Instantiates a client
datastore_client = datastore.Client()

# The kind for the new entity
kind = 'Task'
# The name/ID for the new entity
name = 'sampletask1'
# The Cloud Datastore key for the new entity
task_key = datastore_client.key(kind, name)

# Prepares the new entity
task = datastore.Entity(key=task_key)
task['description'] = 'Buy milk cloud'

# Saves the entity
datastore_client.put(task)

print('Saved {}: {}'.format(task.key.name, task['description']))

def generateHash(raw):
    return bcrypt.hashpw(raw, bcrypt.gensalt())

def validatePassword(password):
    return bcrypt.checkpw(password, generateHash(password))

@app.route("/login",
           methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = self.request.get('username')
        password = self.request.get('password')
        return 1
    elif request.method == 'GET':
        return render_template("login.html")
    else:
        return 3

@app.route("/signup",
           methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        user = request.get_json()

        print(user.get('username'))
        return redirect("/", code=302)
    else:
        return 3


@app.route('/')
def home():
    """Return a friendly HTTP greeting."""
    user = "oi"
    return render_template("home.html", user=user)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

def main(*args):
    if (len(sys.argv) > 1 and sys.argv[1] == "local"):
        server = Server(app.wsgi_app)
        server.watch('main.py')
        server.serve()
    else:
        app.run(host='127.0.0.1', port=8080, debug=True)


if __name__ == '__main__':
    main()
# [END app]
