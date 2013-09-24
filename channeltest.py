#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from webapp2 import Route, WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
import time

from channel import Channel

class Broadcast(webapp2.RequestHandler):
    def get(self):
        Channel.broadcast('<div class=\'row-fluid\'>THIS IS A BROADCAST ON ALL CHANNELS</div>')
        self.response.out.write('Broadcast was sent')        
    
class MainHandler(webapp2.RequestHandler):        
    def get(self, pageName):
        time.sleep(1)
        c = Channel.getChannel(pageName)
        path = os.path.join(os.path.dirname(__file__), './channeltest.html')
        self.response.out.write(template.render(path, {'title': pageName, 'token':c.token } ))

# Map URLs to handlers
routes = [
    Route('/broadcast', Broadcast),      
    Route('/<pageName>', MainHandler),  
]

# webapp2 config
app_config = {
}

app = WSGIApplication(routes=routes, config=app_config, debug=True)

if __name__ == '__main__':
    run_wsgi_app(app)
        