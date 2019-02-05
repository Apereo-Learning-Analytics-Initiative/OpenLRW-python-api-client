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
import smtplib
import requests
import json
import sys
import base64

from openlrw.routes import Routes
from openlrw import exceptions

__author__ = "Xavier Chopin"
__copyright__ = "Copyright 2019"
__license__ = "ECL-2.0"
__version__ = "1.0.0"
__email__ = "xavier.chopin@univ-lorraine.fr"
__status__ = "Production"


try:
    from urllib import request as http
except ImportError:
    import urllib2 as http

DEFAULT_AUTH_HEADER = 'Authorization'


class OpenLRW(object):
    """
    OpenLRW API Client
    """

    def __init__(self, url, username, password, auth_header=DEFAULT_AUTH_HEADER):
        """
        Constructor

        :param url: OpenLRW URI Endpoint
        :param key: API key
        :param password: API Password
        :param auth_header: API HTTP header
        """
        self._url = url
        self._username = username
        self._password = password
        self._auth_header = auth_header
        self._mail = None
        self._from_mail = None
        self._to_mail = None

    def __getattr__(self, name):
        def function(*args, **kwargs):
            return self.execute(method=self._to_camel_case(name), **kwargs)

        return function

    def setup_email(self, host, _from, to):
        """
        Set up the email configuration
        :param host: host server (eg: localhost)
        :param _from: email address
        :param to: email address
        """
        self._mail = smtplib.SMTP(str(host))
        self._from_mail = _from
        self._to_mail = to

    @staticmethod
    def _to_camel_case(snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    @staticmethod
    def _parse_response(response):
        try:
            body = json.loads(response.decode(errors='ignore'))

            if 'error' in body:
                message = body.get('error').get('message')
                raise exceptions.OpenLRWClientException(message)

            return body.get('result')
        except ValueError:
            return None

    def _http_get(self, route, jwt):
        """
        For OneRoster routes('/api/:route')
        :param route:
        :param jwt:
        :return:
        """
        response = requests.get(self._url + route, headers={'Authorization': 'Bearer ' + jwt})
        Routes.print_get(route, response)
        return False if response.status_code == 401 else response.content  # if token expired

    def _http_post(self, route, jwt, data):
        """
        For OneRoster routes('/api/:route')
        :param route:
        :param jwt:
        :return:
        """
        response = requests.post(self._url + route, headers={'Authorization': 'Bearer ' + jwt}, json=data)
        Routes.print_post(route, response)
        return response.status_code != 401  # if token expired

    def _http_delete(self, route, jwt):
        """
        For OneRoster routes('/api/:route')
        :param route:
        :param jwt:
        :return:
        """
        response = requests.delete(self._url + route, headers={'Authorization': 'Bearer ' + jwt})
        Routes.print_delete(route, response)
        return response.status_code != 401  # if token expired

    def mail_server(self, subject, message):
        """
        Send an email
        :param subject:
        :param message:
        :return:
        """
        if self._mail:
            self._mail.sendmail(self._from_mail, self._to_mail, "Subject: " + subject + " \n\n" + message)



    ######################################################
    #                    API CALLS                       #
    ######################################################

    # Users

    def post_user(self, data, jwt, check):
        check = 'false' if check is False else 'true'
        return self._http_post(Routes.USERS + '?check=' + check, jwt, data)

    def delete_user(self, user_id, jwt):
        return self._http_delete(self._url + Routes.USERS + '/' + user_id, jwt)

    def get_user(self, user_id, jwt):
        return self._http_get(Routes.USERS + '/' + user_id, jwt)

    def get_users(self, jwt):
        return self._http_get(Routes.USERS, jwt)

    # Events

    def send_xapi(self, statement):
        """
        Send xAPI statements
        :param statement: JSON Object following the xAPI format
        :return: response
        """
        credentials = base64.b64encode('{}:{}'.format(self._username, self._password).encode())
        headers = {self._auth_header: 'Basic ' + credentials.decode(), "X-Experience-API-Version": "1.0.0"}
        response = requests.post(self._url + Routes.XAPI, headers=headers, json=statement)
        Routes.print_post(Routes.XAPI, response)
        return response

    def send_caliper(self, statement):
        """
        Send Caliper statement
        :param statement: JSON Object following the IMS Caliper format
        :return: response
        """
        response = requests.post(self._url + Routes.CALIPER, headers={"Authorization": self._username}, json=statement)
        Routes.print_post(Routes.CALIPER, response)
        return response

    # Authentication

    def generate_jwt(self):
        """
        Create a JSON Web Token
        :return: a token
        """
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        data = {"username": self._username, "password": self._password}
        try:
            response = requests.post(self._url + Routes.AUTH, headers=headers, json=data)
            Routes.print_post(self._url + Routes.AUTH, response)
            res = response.json()
            return res['token']
        except requests.RequestException:
            self.mail_server("Unable to get the JWT Token", sys.argv[0] + " was unable to get the token.")
            sys.exit("Unable to get the JWT Token")

