__author__ = 'Harsh Daftary'

try:
    import requests
    import json

except ImportError:
    print("requests and json libraries are required, but not found.")
    exit(1)

from functools import wraps

class ApiError(Exception):
    pass


class GoDebianApi(object):

    def __init__(self, host="http://go.debian.net/"):
        """
        :param host: by default it will use go.debian.net for generating preview and short urls
        use host = http://deb.li/ if you want in that format
        json api url is deb.li/rpc/json
        if you want to change it then subclass this class and override __init__ to make your changes.

        :return None
        """
        self.api_url = "http://deb.li/rpc/json"
        self.host = host
        self.preview = host + "p/%s"
        self.headers = {'Content-type': 'application/json'}
        self.check_ip_white_list()

    def _api_call(func):
        @wraps(func)
        def _tmp(self, *args, **kwargs):
            function_name = func.__name__

            data = {'method': function_name, 'params': args, 'id': "jsonrpc"}
            r = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))
            #print(r.status_code)

            if r.status_code == 200:
                resp = r.json()
                if resp.get('result', False):
                    return self.host + resp.get('result')
                else:
                    raise ApiError(resp.get('error', "Some error occurred"))
            else:
                raise ApiError("May be your host is not whitelisted in the api, visit https://wiki.debian.org/deb.li for more details.")
        return _tmp
            

    @_api_call
    def add_url(self, url):
        """
        :param url: Provides shortened link for given URL
                    repeated URLs don't get different Keys.
        :return str: shortened URL
        """
        pass

    def get_preview_url(self, key):
        """
        :param key: Returns preview URL for provided key
        :return str
        """
        return self.preview % key

    @_api_call
    def get_url(self, key):
        """
        :param key: Enter the key to get associated URL
        Get key from following format : http://deb.li/p/<key>
        :return str: URL associated
        """
        pass

    @_api_call
    def add_static_url(self, url, keyword):
        """
        :param url: Url to be shortened
        :param keyword: Static keyword against which url needs to be stored
        example : go.debian.net/<keyword>
        :return:
        """
        pass

    @_api_call
    def update_static_url(self, url, keyword):
        """
        :param url: new url
        :param keyword: Static keyword against which url needs to be stored
        example : go.debian.net/<keyword>
        :return:
        """

    def check_ip_white_list(self):
        try:
        _ = self.add_url("http://www.debian.org")
        except Exception as e:
            print("Exception occured")
            print(e)

