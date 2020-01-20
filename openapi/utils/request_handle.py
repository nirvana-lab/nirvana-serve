# -*- coding: utf-8 -*-
import requests

class RequestSession(requests.Session):

    def __init__(self):
        super(RequestSession, self).__init__()
        self.init_meta_data()

    def init_meta_data(self):
        self.meta_data = {
            'url': 'www.baidu.com'
        }

    # def request(self, method, url,
    #         params=None, data=None, headers=None, cookies=None, files=None,
    #         auth=None, timeout=None, allow_redirects=True, proxies=None,
    #         hooks=None, stream=None, verify=None, cert=None, json=None):

    def http_request(self, method, url, name=None, **kwargs):
        print(method, url)
        print(self.meta_data)

a = RequestSession()

a.http_request("1", "2")