import webapp2
import urllib
import urllib2
from google.appengine.api import urlfetch
import random
import json

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class Update(webapp2.RequestHandler):
    def get(self):
        stock_response = urllib2.urlopen('http://dev.markitondemand.com/Api/v2/Quote/json?symbol=LNKD')
        stock_quote = json.load(stock_response)
        sentiment = 50
        changePercent = stock_quote['ChangePercent']
        # changePercent = 10*random.uniform(-1, 1)
        ceiling = 10
        delta = max(min(1, (abs(changePercent))/ceiling), 0)
        if changePercent > 0:
            sentiment = 55
            sentiment = sentiment + delta*30
        else:
            sentiment = 45
            sentiment = sentiment - delta*30
        url = "https://api-http.littlebitscloud.cc/devices/00e04c1f00fd/output"
        params = {
          "percent": sentiment,
          "duration_ms": -1
        }
        post_data = urllib.urlencode(params)
        result = urlfetch.fetch(url=url,
            payload=post_data,
            method=urlfetch.POST,
            headers={'Authorization': 'Bearer 8b4537d0bf61c7bf6937ad9f609d40fda9d3a6ccdd8bfebfddf504e500b3b9a0', 'Accept': 'application/vnd.littlebits.v2+json'})
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(result.content)
        self.response.write('\n')
        self.response.write(str(sentiment))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/update', Update)
], debug=True)
