#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import requests
import hashlib
import jwt

import base64



class Maltiverse(object):

    def __init__(self, auth_token=None, endpoint='https://api.maltiverse.com'):
        self.endpoint = endpoint
        self.auth_token = auth_token
        self.sub = None
        self.team_name = None
        self.team_researcher = None
        self.admin = None
        self.session = requests.Session()
        self.session.headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
        }
        if auth_token:
            self.session.headers.update({'Authorization': 'Bearer ' + self.auth_token})



    def get(self, method, params=None):
        '''Auxiliar method to perform GET requests to the platform'''

        #Removing content-type JSON for get requests to be valid
        self.session.headers = {
            'accept': 'application/json',
        }

        #Perform get request
        r = self.session.get(self.endpoint + method, params=params, timeout=180)

        #Restoring content-type JSON
        self.session.headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
        }
        return r

    def put(self, method, params):
        '''Auxiliar method to perform PUT requests to the platform'''
        if self.team_researcher and not self.admin:
            # Adding required information to push info being a researcher.
            if 'blacklist' in params:
                # Is not allowed to specify dates
                if 'creation_time' in params:
                    params.pop('creation_time', None)
                if 'modification_time' in params:
                    params.pop('modification_time', None)

                if 'domain' in params:
                    params.pop('domain', None)

                if 'urlchecksum' in params:
                    params.pop('urlchecksum', None)

                if 'tld' in params:
                    params.pop('tld', None)

                if 'type' in params:
                    params.pop('type', None)

                for i, bl in enumerate(params['blacklist']):
                    # Must set the ref
                    params['blacklist'][i]['ref'] = self.sub

                    # Must set the team name as the Blacklist source
                    params['blacklist'][i]['source'] = self.team_name

                    # Is not allowed to specify dates
                    if 'first_seen' in params['blacklist'][i]:
                        params['blacklist'][i].pop('first_seen', None)
                    if 'last_seen' in params['blacklist'][i]:
                        params['blacklist'][i].pop('last_seen', None)


        r = self.session.put(self.endpoint + method, data=json.dumps(params))


        return r

    def post(self, method, params):
        '''Auxiliar method to perform POST requests to the platform'''
        r = self.session.post(self.endpoint + method, data=json.dumps(params))
        return r

    def delete(self, method):
        '''Auxiliar method to perform DELETE requests to the platform'''
        r = self.session.delete(self.endpoint + method)
        return r

    def login(self, email, password):
        r = self.post('/auth/login',{'email': email, 'password': password})
        r_json = json.loads(r.text)

        if 'status' in r_json and r_json['status'] == 'success':
            if r_json['auth_token']:

                self.auth_token = r_json['auth_token']
                decoded_payload = jwt.decode(self.auth_token, verify=False)
                self.sub = decoded_payload['sub']
                self.team_name = decoded_payload['team_name']
                self.team_researcher = decoded_payload['team_researcher']
                self.admin = decoded_payload['admin']
                self.session.headers.update({'Authorization': 'Bearer ' + self.auth_token})
                return True
        return False

    def ip_get(self, ip_addr):
        ''' Requests an IP address '''
        r = self.get('/ip/' + ip_addr)
        return json.loads(r.text)

    def ip_put(self, ip_dict):
        ''' Inserts a new Ip address observable. If it exists, the document is merged and stored. Requires authentication as admin'''
        r = self.put('/ip/' + ip_dict['ip_addr'], params=ip_dict)
        return json.loads(r.text)

    def ip_delete(self, ip_addr):
        ''' Deletes Ip address observable. Requires authentication as admin'''
        r = self.delete('/ip/' + ip_addr)
        return json.loads(r.text)

    def hostname_get(self, hostname):
        ''' Requests a hostname '''
        r = self.get('/hostname/' + hostname)
        return json.loads(r.text)

    def hostname_put(self, hostname_dict):
        ''' Inserts a new hostname observable. If it exists, the document is merged and stored. Requires authentication as admin'''
        r = self.put('/hostname/' + hostname_dict['hostname'], params=hostname_dict)
        return json.loads(r.text)

    def hostname_delete(self, hostname):
        ''' Deletes hostname observable. Requires authentication as admin'''
        r = self.delete('/hostname/' + hostname)
        return json.loads(r.text)

    def url_get(self, url):
        ''' Requests a url '''
        urlchecksum = hashlib.sha256(url.encode('utf-8')).hexdigest()
        r = self.get('/url/' + urlchecksum)
        return json.loads(r.text)

    def url_put(self, url_dict):
        ''' Inserts a new url observable. If it exists, the document is merged and stored. Requires authentication as admin'''
        urlchecksum = hashlib.sha256(url_dict['url'].encode('utf-8')).hexdigest()
        r = self.put('/url/' + urlchecksum, params=url_dict)
        return json.loads(r.text)

    def url_delete(self, url):
        ''' Deletes url observable. Requires authentication as admin'''
        urlchecksum = hashlib.sha256(url.encode('utf-8')).hexdigest()
        r = self.delete('/url/' + urlchecksum)
        return json.loads(r.text)

    def sample_get(self, sha256):
        ''' Requests a sample '''
        r = self.get('/sample/' + sha256)
        return json.loads(r.text)

    def sample_put(self, sample_dict):
        ''' Inserts a new sample observable. If it exists, the document is merged and stored. Requires authentication as admin'''
        r = self.put('/sample/' + sample_dict['sha256'], params=sample_dict)
        return json.loads(r.text)

    def sample_delete(self, sha256):
        ''' Deletes sample observable. Requires authentication as admin'''
        r = self.delete('/sample/' + sha256)
        return json.loads(r.text)

    def sample_get_by_md5(self, md5):
        ''' Requests a sample by MD5 '''
        r = self.get('/search?query=md5:"' + md5 + '"')
        return json.loads(r.text)


    def search(self, query, fr=None, size=None, sort=None, range=None, range_field=None, format=None):
        ''' Performs a search into the Maltiverse platform. https://whatis.maltiverse.com/knowledge-base/search-basics/'''
        params = dict()

        params['query'] = query

        if fr is not None:
            params['from'] = fr

        if size is not None:
            params['size'] = size

        if sort:
            params['sort'] = sort

        if range:
            params['range'] = range

        if range_field:
            params['range_field'] = range_field

        if format:
            params['format'] = format

        r = self.get('/search', params=params)

        return json.loads(r.text)
