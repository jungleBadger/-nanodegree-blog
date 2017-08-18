#!/usr/bin/env python
from google.cloud import datastore
class Datastore:
    datastore_client = datastore.Client()

    def __init__(self):
        self.data = []


    def do_query(self, kind, key='', value='', limit=100, order_by=''):
        if not order_by:
            order_by=key
        query = self.datastore_client.query(kind=kind, order=(order_by,))
        if (key and value):
            query.add_filter(key, '=', value)
        result = list(query.fetch(limit=limit))
        if len(result) > 0:
            return result
        else:
            return []


    def create_entity(self, kind, value):
        if (kind == 'Post'):
            return datastore.Entity(self.datastore_client.key(kind, value), exclude_from_indexes = ['image', 'text'])
        else:
            return datastore.Entity(key=self.datastore_client.key(kind, value))


    def save_object(self, model_object):
        return self.datastore_client.put(model_object)