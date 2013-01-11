#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import simplejson
import twitter
import urllib2
import re

render = web.template.render('/home/production/twitworth/templates/')
urls = (
  '/', 'index',
  '/getworth', 'getworth',
)
db = web.database(dbn='postgres', user='production', pw='', db='twitworth')
#app = web.application(urls, locals())

class getworth:
    def GET(self):
       params = web.input(username=None)
       if not params.username:
           return "username not sent"
       data = db.select('final',dict(username=params.username),where="username=$username")
       if len(data)==0:
           return 'user not found in database. visit <a href ="http://twitworth.com">twitworth</a> first and esitmate you value.'
       for d in data:
           stuff=d
       return str(stuff.level1)+","+str(stuff.level2)+","+stuff.cost

class index:
    def GET(self):
       return render.index("0","","","")
    def POST(self):
       params = web.input(username=None,password=None,cost=None)
       if not (params.username and params.password):
           return ("2","","","")
       if not params.cost:
           cost=0.5
       else:
           cost=float(params.cost)
       auth_handler = urllib2.HTTPBasicAuthHandler()
       auth_handler.add_password('Twitter API', 'twitter.com',params.username, params.password)
       opener = urllib2.build_opener(auth_handler)
       level1=0
       level2=0
       try:
           theurl = "http://twitter.com/users/show/"+params.username+".json"
           follow_data = simplejson.loads(opener.open(theurl).read())
           level1 = int(follow_data['followers_count'])
           db.insert('call',call_type=0)
           pages =(level1/100) + 2
           theurl = 'http://twitter.com/statuses/followers.json?lite=true'
           fdata1 = re.sub(",Couldn't find Status with ID=([0-9]*),",",",opener.open(theurl).read())
           fdata = re.sub(",Couldn't find User with ID=([0-9]*),",",",fdata1)
           db.insert('call',call_type=1)
           followers = simplejson.loads(fdata)
           for u in followers:
               level2= level2 + u['followers_count']
           urltemp = 'http://twitter.com/statuses/followers.json?lite=true&page=%d'
           for i in range(2,pages):
               theurl = urltemp % (i,)
               data_str = opener.open(theurl).read()
               db.insert('call',call_type=1)
               pdata_str1 = re.sub(",Couldn't find Status with ID=([0-9]*),",",",data_str)
               pdata_str = re.sub(",Couldn't find User with ID=([0-9]*),",",",pdata_str1)
               data = simplejson.loads(pdata_str)
               for u in data:
                   level2 = level2 + u['followers_count']
       except urllib2.HTTPError, e:
           return render.index("2","","","")
       except urllib2.URLError, e:
           return render.index("2","","","")
       total = (cost*int(level1)) + (cost*(int(level2)/100))
       res = db.select('final',dict(username=params.username),where="username=$username")
       if len(res)==0:
           db.insert('final',username=params.username,level1=int(level1),level2=int(level2),cost=str(total))
       else:
           db.update('final',where = "username='%s'" % (params.username,),level1=int(level1),level2=int(level2),cost=str(total))
       return render.index("1",level1,level2,str(total))



#if __name__ == "__main__":
#    app.run()
application = web.application(urls, globals()).wsgifunc() 

