#!/usr/bin/env python
from google.cloud import datastore
class Datastore:
    datastore_client = datastore.Client()

    def __init__(self):
        self.data = []


    def do_query(self, kind, key, value):
        query = self.datastore_client.query(kind=kind)
        query.add_filter(key, '=', value)
        result = list(query.fetch())
        if len(result) > 0:
            return result
        else:
            return 0


    def create_entity(self, username):
        return datastore.Entity(key=self.datastore_client.key('email', username))


    def save_object(self, model_object):
        return self.datastore_client.put(model_object)