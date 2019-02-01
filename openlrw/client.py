# The ECL-2.0 License (ECL-2.0)
#
# Copyright (c) 2019 Xavier Chopin Licensed under the
# Educational Community License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.osedu.org/licenses/ECL-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.

import json
import base64


try:
    from urllib import request as http
except ImportError:
    import urllib2 as http


DEFAULT_AUTH_HEADER = 'Authorization'


class OpenLRW(object):
    """
    OpenLRW API Client
    """
    def __init__(self, url, key, password, auth_header=DEFAULT_AUTH_HEADER):
        """
        Constructor

        :param url: OpenLRW URI Endpoint
        :param key: API key
        :param password: API Password
        :param auth_header: API HTTP header
        """
        self._url = url
        self._key = key
        self._password = password
        self._auth_header = auth_header

    def __getattr__(self, name):
        def function(*args, **kwargs):
            return self.execute(method=self._to_camel_case(name), **kwargs)
        return function

    @staticmethod
    def _to_camel_case(snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

