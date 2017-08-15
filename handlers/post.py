#!/usr/bin/env python
from flask import render_template
from handlers.datastore import Datastore
import uuid
class Post:
    def __init__(self):
        self.post_page_path = 'post.html'
        self.edit_post_path = 'edit_post.html'
        self.login_path = 'login.html'
        self.datastore = Datastore()


    def render_edit_page(self, error='', username='', post='', action='Create'):
        if post:
            action = 'Edit'
        return render_template(self.edit_post_path,
                               error=error,
                               action=action,
                               username=username,
                               post=post)


    def render_view_page(self, error='', username='', post=''):
        return render_template(self.post_page_path,
                               error=error,
                               username=username,
                               post=post)


    def query_post_by_id(self, post_id):
        post_list = self.datastore.do_query('Post', 'id', post_id)
        print(post_list)
        print('AIOSDJDIOASJIDAIODJSAIODJIAOSDJSAOIJDOIAS')
        if len(post_list) > 0:
            return post_list[0]
        else:
            return 0


    def query_post_by_tag(self, post_tag):
        post_list = self.datastore.do_query('Post', 'tag', post_tag)
        if len(post_list) > 0:
            return post_list
        else:
            return 0


    def create_post(self, post_author, post_title, post_image, post_text, post_tag, post_id = ''):
        if not post_id:
            post_id = str(uuid.uuid4())

        post = self.datastore.create_entity('Post', post_id)
        error = ''
        post['id'] = post_id
        post['author'] = post_author
        post['title'] = post_title
        post['image'] = post_image
        post['text'] = post_text
        post['tag'] = post_tag

        if not post_title or not post_text or not post_tag:
            error = 'Missing parameters'
        else:
            self.datastore.save_object(post)

        if error:
            return self.render_edit_page(error, post_author, post)
        else:
            #change
            return self.render_view_page('', post_author, post)


    def edit_post(self, post_id, post_title='', post_image='', post_text='', post_tag=''):
        post = self.query_post_by_id(post_id)
        if post != 0:
            if post_title != '':
                post['title'] = post_title
            if post_image != '':
                post['image'] = post_image
            if post_text != '':
                post['text'] = post_text
            if post_tag != '':
                post['tag'] = post_tag
            self.datastore.save_object(post)
            return self.render_edit_page('', '', post)

        return 'Post not found'



    def comment_post(self, post_id, comment_author, comment_text):
        return 1


    def delete_post(self, post_id):
        return 1
