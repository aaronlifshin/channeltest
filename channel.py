import webapp2_extras.appengine.auth.models as auth_models
import datetime
from google.appengine.ext import ndb
import logging
from google.appengine.api import channel
import json


class Channel(ndb.Model):
    token = ndb.StringProperty()  
    tokenExpires = ndb.DateTimeProperty()  
    
    @classmethod
    def makeMessage(cls,html):
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = datetime.datetime.now() - epoch  
        timestamp = delta.total_seconds()
        message = {
                'notificationHTML': html,
                'timestamp': timestamp
               }
        return json.dumps(message)
               

    @classmethod
    def createChannel(cls, clientID):
        now = datetime.datetime.now()
        c = Channel()
        c.token = channel.create_channel(clientID, duration_minutes=1440)
        c.tokenExpires = now + datetime.timedelta(days=1)
        logging.info('Creating new token: %s' % c.token)        
        c.put()
        return c
        
    @classmethod
    def broadcast(cls, messageHTML):
        q = cls.query()
        channels = q.fetch(100)
        for c in channels:
            if c.tokenExpires > datetime.datetime.now():
                channel.send_message(c.token, cls.makeMessage(messageHTML))
                
    @classmethod
    def getChannel(cls, clientID):
        q = cls.query()
        channels = q.fetch(10)
        channelToReturn = None
        for c in channels:
            if c.tokenExpires > datetime.datetime.now():
                channelToReturn = c
        if channelToReturn is None:
            channelToReturn = cls.createChannel(clientID)
        return channelToReturn
        
        
         
