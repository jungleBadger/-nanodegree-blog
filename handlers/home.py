#!/usr/bin/env python
from flask import render_template
class Home:
    def __init__(self):
        self.page_path = 'home.html'


    def render_page(self, error='', username=''):
        return render_template(self.page_path,
                               error=error,
                               username=username)