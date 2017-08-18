#!/usr/bin/env python
from flask import render_template
from handlers.post import Post
class Home:
    def __init__(self):
        self.page_path = 'home.html'
        self.post = Post()


    def render_page(self, error='', username='', posts=''):
        return render_template(self.page_path,
                               posts=posts,
                               error=error,
                               username=username)