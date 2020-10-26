#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 17:00:31 2017

@author: will
"""
import urllib.request
import urllib.parse
import json
import logging
import time
import csv

def _obj_hook(paris):
    'json encode'
    odict = JsonDict()
    for key, value in paris.items():
        odict[str(key)] = value
    return odict

def _encode_params(**kw):
    'Encode parameters'
    args = []
    for key, value in kw.items():
        para = value.encode('utf-8') if isinstance(value, str) else str(value)
        args.append('%s=%s' % (key, urllib.parse.quote(para)))
    return '&'.join(args)

def _encode_multipart(**kw):
    'encode mulyipart data'
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for key, value in kw.items():
        data.append('--%s' % boundary)
        if hasattr(value, 'read'):
            filename = getattr(value, 'name', '')
            name = filename.rfind('.')
            ext = filename[name:].lower() if name != (-1) else ""
            content = value.read()
            content = content.decode('ISO-8859-1')
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % key)
            data.append('Content-Length: %d' % len(content))
            data.append('Content-Type: %s\r\n' % _guess_content_type(ext))
            data.append(content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % key)
            data.append(value if isinstance(value, str) else value.decode('utf-8'))
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary

_CONTENT_TYPES = {'.png': 'image/png', '.gif': 'image/gif', '.jpg': 'image/jpeg',
                  '.jpeg': 'image/jpeg', '.jpe': 'image/jpeg'}

def _guess_content_type(ext):
    return _CONTENT_TYPES.get(ext, 'application/octet-stream')


class JsonDict(dict):
    '''
    a json class inhert dict class which can use d['key'] or d.key to get
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

_HTTP_GET = 0
_HTTP_POST = 1
_HTTP_UPLOAD = 2

def _http_get(url, authorization=None, **kw):
    logging.info('GET %s' % url)
    return _http_request(url, _HTTP_GET, authorization, **kw)

def _http_post(url, authorization=None, **kw):
    logging.info('POST %s' % url)
    return _http_request(url, _HTTP_POST, authorization, **kw)

def _http_upload(url, authorization=None, **kw):
    logging.info('UPLOAD %s' % url)
    return _http_request(url, _HTTP_UPLOAD, authorization, **kw)

def _http_request(url, method, authorization, **kw):
    'send http request and get json object'
    params = None
    boundary = None
    if method == _HTTP_UPLOAD:
        params, boundary = _encode_multipart(**kw)
    else:
        params = _encode_params(**kw)
    http_url = '%s?%s' % (url, params) if method == _HTTP_GET else url
    http_para = None if method == _HTTP_GET else params.encode(encoding='utf-8')
    #print(http_para)
    req = urllib.request.Request(http_url, data=http_para)
    if authorization:
        req.add_header('Authorization', 'OAuth2 %s' % authorization)
    if boundary:
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    resq = urllib.request.urlopen(req)
    body = resq.read().decode("utf-8")
    result = json.loads(body, object_hook=_obj_hook)
    if 'error_code' in result:
        print('error')
    return result

class HttpObject(object):
    'post get or updload object'
    def __init__(self, client, method):
        self.client = client
        self.method = method

    def __getattr__(self, attr):
        def wrap(**kw):
            'request param'
            if self.client.is_expires():
                raise AttributeError
            return _http_request('%s%s.json' % (self.client.api_url, attr.replace('__', '/')),
                                 self.method, self.client.access_token, **kw)
        return wrap

class APIClient(object):
    'APIClient class'
    def __init__(self, app_key, app_secret, redirect_uri=None,
                 response_type='code', domain='api.weibo.com', version='2'):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.auth_url = 'https://%s/oauth2/' % domain
        self.api_url = 'https://%s/%s/' % (domain, version)
        self.access_token = None
        self.expires = 0.0
        self.get = HttpObject(self, _HTTP_GET)
        self.post = HttpObject(self, _HTTP_POST)
        self.upload = HttpObject(self, _HTTP_UPLOAD)

    def get_authorize_url(self):
        'get authorize url'
        return '''https://api.weibo.com/oauth2/authorize?response_type=\
code&client_id=%s&redirect_uri=%s'''%(self.client_id, self.redirect_uri)


    def request_access_token(self, code):
        """post a request and then get a access_token"""
        result = _http_post('%s%s' % (self.auth_url, 'access_token'), \
                          client_id=self.client_id, \
                          client_secret=self.client_secret, \
                          redirect_uri=self.redirect_uri, \
                          code=code, grant_type='authorization_code')
        result.expires_in += int(time.time())
        return result


    def set_access_token(self, access_token, expires_in):
        'set access_token and expires_in'
        self.access_token = str(access_token)
        self.expires = float(expires_in)

    def is_expires(self):
        'judge'
        return not self.access_token or time.time() > self.expires

    def public_timeline(self):
        '''
        get new public weibo,the parameters followed can be used in _http_get in this method
        access_token : (string) the token you got after OAuth
        count : (int) the record items in one single page,default 50 items
        page : (int) the page number,default one page
        base_app : (int) whether get data in current app or not,
            0 is not(all data),1 is yes(current app),default 0
        '''
        result = _http_get('%s'% (self.api_url)  + 'statuses/public_timeline.json', \
                           access_token=self.access_token, \
                           count=50, \
                           page=1, \
                           base_app=0, \
                )
        return result

    def statuses_update(self):
        '''
        post a weibo with a picutre
        '''
        result = _http_upload('https://upload.api.weibo.com/2/statuses/upload.json', \
                            access_token=self.access_token, \
                            status="hanzo from api", \
                            pic=open('hanzo.jpg', 'rb'), \
                            rip='0.0.0.0', \
                             )
        return result

def uid2screen_name(uid):
    '''
    if you want to use this api,you should follow steps follows to operate.
    '''
    try:
        #step 1 : sign a app in weibo and then define const app key,app srcret,redirect_url
        APP_KEY = ["1209239226","1339230464"]
        APP_SECRET = ["b6a6708a911dee5a47aaf31e515f698d","b60b49af26c939c20fe3ff79047ad777"]
        REDIRECT_URL = 'https://api.weibo.com/oauth2/default.html'
        #step 2 : get authorize url and code
        client = APIClient(app_key=APP_KEY[0], app_secret=APP_SECRET[0], redirect_uri=REDIRECT_URL)
        #print(client.get_authorize_url())
        #step 3 : get Access Token
        #result = client.request_access_token(input("please input code : "))
        #print(result)
        #client.set_access_token(result.access_token, result.expires_in)
        #step 4 : using api by access_token
        #print(client.public_timeline())
        r = {'access_token': '2.00dvJhTGU3qp_B47c7e394a2hikTRB', 'remind_in': '157679999', 'expires_in': 1758940646, 'uid': '5935597009', 'isRealName': 'true'}
        #r = {'access_token': '2.00dvJhTG3BRd9B32496d73a9n8OiUC', 'remind_in': '157679999', 'expires_in': 1759041472, 'uid': '5935597009', 'isRealName': 'true'}
        client.set_access_token(r['access_token'], r['expires_in'])
        '''
        in this step,the api name have to turn '/' in to '__'
        for example,statuses/upload(this is a standard api name) have to turn into statuses__upload
        '''

        user = client.get.users__show(uid=uid)

        return user
        #print("uid is",client.get.account__get_uid())
        #print(client.statuses_update())
    except ValueError:
        print('pyOauth2Error')
def readData():
    line_num = 0
    f = open('weibodata.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["LineNumber", "CreatedTime", "UserID", "screen_name", "location", "gender", "content"])
    uid = 0000000000
    cnt = 0
    with open('J:/weibo.txt', 'r', encoding='utf-8') as file:
        
        while line_num < 100000:
            
            if line_num == 0:
                line = file.readline().strip()
                line_num = line_num + 1
                continue          
            # print("\nline No.:", line_num)
            line = file.readline()[64139:].strip()
            weibo = line.split("\t")

            if weibo[21] != uid:
                uid = weibo[21]
                print(cnt, uid)
                cnt += 1
                name = uid2screen_name(uid)
                screen_name = name['screen_name']
                location = name['location']
                gender = name['gender']
            csv_writer.writerow([line_num, weibo[4], weibo[21], screen_name, location, gender, weibo[18]])
            

            line_num = line_num + 1

def main():
    uid = 5935597009
    readData()
    #uid2screen_name(uid)
    #1660544250
    '''
    user = uid2screen_name(uid)
    screen_name = user["screen_name"]
    location = user["location"]
    print("昵称:",screen_name)
    print("位置:",location)
    '''

if __name__ == '__main__':
    main()

