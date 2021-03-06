#!/usr/bin/env python
from flask import render_template
from handlers.datastore import Datastore
import uuid
import time


class Post:
    def __init__(self):
        self.post_page_path = 'post.html'
        self.edit_post_path = 'edit_post.html'
        self.login_path = 'login.html'
        self.datastore = Datastore()

    def render_edit_page(self,
                         error='', username='', post='', action='Create'):
        if post:
            action = 'Edit'
        return render_template(self.edit_post_path,
                               error=error,
                               action=action,
                               username=username,
                               post=post)

    def render_view_page(self,
                         post, post_likes=0, error='',
                         username='', comments='', user_liked=''):
        if not comments:
            comments = self.get_posts_comments(post.get('id'))
        return render_template(self.post_page_path,
                               error=error,
                               username=username,
                               post=post,
                               likes=post_likes,
                               comments=comments,
                               user_liked=user_liked)

    def query_latest_posts(self):
        return self.datastore.do_query(
            kind='Post', limit=10, order_by='-timestamp')

    def query_post_by_id(self, post_id):
        post_list = self.datastore.do_query('Post', 'id', post_id)
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

    def query_comments_by_id(self, comment_id):
        comment = self.datastore.do_query('Comments', 'id', comment_id)
        if len(comment) > 0:
            return comment[0]
        else:
            return 0

    def query_likes_by_post_id(self, post_id):
        likes = self.datastore.do_query('Like', 'post', post_id)
        return len(likes)

    def query_likes_by_post_id_and_user(self, post_id, username):
        like = self.datastore.do_query(
            'Like', 'post', post_id, 'user', username)
        if len(like) > 0:
            return like[0]
        else:
            return []

    def get_posts_comments(self, post_id):
        return self.datastore.do_query('Comments', 'post_id', post_id)

    def create_post(self,
                    post_author, post_title, post_image, post_text, post_tag):
        post_id = str(uuid.uuid4())
        post = self.datastore.create_entity('Post', post_id)
        error = ''
        post['id'] = post_id
        post['author'] = post_author
        post['title'] = post_title
        post['image'] = post_image
        post['text'] = post_text
        post['tag'] = post_tag
        post['timestamp'] = int(time.time() * 1000)
        if not post_title or not post_text or not post_tag:
            error = 'Missing parameters'
        else:
            self.datastore.save_object(post)
        if error:
            return {'response': self.render_edit_page(
                error, post_author, post)}
        else:
            return {'status': 1, 'post_id': post_id}

    def edit_post(self,
                  post_id, edit_author, post_title='',
                  post_image='', post_text='', post_tag=''):
        post = self.query_post_by_id(post_id)
        if post != 0:
            if post.get('author') != edit_author:
                return "Unauthorized operation"
            if post_title != '':
                post['title'] = post_title
            if post_image != '':
                post['image'] = post_image
            if post_text != '':
                post['text'] = post_text
            if post_tag != '':
                post['tag'] = post_tag
            self.datastore.save_object(post)
            return {'status': 1, 'post_id': post_id}

        return {'response': "Error"}

    def delete_post(self, post_id, username):
        post = self.query_post_by_id(post_id)
        if post != 0:
            if post.get('author') != username:
                return "Unauthorized operation"
            self.datastore.delete_object('Post', post_id)
            return 1
        return 'post not found'

    def like_post(self, post_id, username):
        post = self.query_post_by_id(post_id)
        if post != 0:
            if post.get('author') == username:
                return "Unauthorized operation"
            like_id = str(uuid.uuid4())
            like = self.datastore.create_entity('Like', like_id)
            error = ''
            like['id'] = like_id
            like['post'] = post_id
            like['user'] = username
            self.datastore.save_object(like)
            return {'status': 1, 'post_id': post_id}
        return 'post not found'

    def dislike_post(self, post_id, username):
        post = self.query_post_by_id(post_id)
        if post != 0:
            if post.get('author') == username:
                return "Unauthorized operation"
            like = self.query_likes_by_post_id_and_user(post_id, username)
            self.datastore.delete_object('Like', like['id'])
            return {'status': 1, 'post_id': post_id}
        return 'post not found'

    def comment_post(self, post_id, comment_author, comment_text):
        comment_id = str(uuid.uuid1())
        comment = self.datastore.create_entity('Comments', comment_id)
        error = ''
        comment['post_id'] = post_id
        comment['author'] = comment_author
        comment['id'] = comment_id
        comment['text'] = comment_text
        comment['timestamp'] = int(time.time() * 1000)
        if not post_id or not comment_author or not comment_text:
            error = 'Missing parameters'
        else:
            self.datastore.save_object(comment)
        post = self.query_post_by_id(post_id)
        if post:
            return 1
        else:
            return error

    def delete_comment(self, comment_id, username):
        comment = self.query_comments_by_id(comment_id)
        if comment != 0:
            if comment.get('author') == username:
                self.datastore.delete_object('Comments', comment_id)
                return 1
            else:
                return 'not authorized'
        else:
            return 'comment not found'

    def edit_comment(self, comment_id, edit_author, comment_text):
        comment = self.query_comments_by_id(comment_id)
        if comment != 0:
            if comment.get('author') != edit_author:
                return "Unauthorized operation"
            if comment_text != '':
                comment['text'] = comment_text
            self.datastore.save_object(comment)
            return {'status': 1, 'comment_id': comment_id}

        return {'response': "Error"}