# coding=utf-8

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

from openlrw.oneroster import OneRoster
from openlrw.exceptions import *
from openlrw.routes import *

__author__ = "Xavier Chopin"
__copyright__ = "Copyright 2019"
__license__ = "ECL-2.0"
__version__ = "1.0.3"
__email__ = "xavier.chopin@univ-lorraine.fr"
__status__ = "Production"

try:
    xrange
except NameError:
    xrange = range


class OpenLRW(object):
    """
    OpenLRW API Client
    """

    URI = ""

    def __init__(self, url, username, password):
        """
        Constructor

        :param url: OpenLRW URI Endpoint
        :param key: API key
        :param password: API Password
        :param auth_header: API HTTP header
        """
        OpenLRW.URI = url
        self._username = username
        self._password = password
        self._mail = None
        self._from_mail = None
        self._to_mail = None
        self._host_mail = None

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
        self._host_mail = host
        self._from_mail = _from
        self._to_mail = to

    @staticmethod
    def _to_camel_case(snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def mail_server(self, subject, message):
        """
        Send an email
        :param subject:
        :param message:
        :return:
        """
        if self._host_mail:
            self._mail = smtplib.SMTP(str(self._host_mail))
            self._mail.sendmail(self._from_mail, self._to_mail, "Subject: " + subject + " \n\n" + message)

    ######################################################
    #                    API CALLS                       #
    ######################################################

    def http_auth_get(self, route, jwt):
        return OneRoster.http_get(route, jwt)

    def http_auth_post(self, route, data, jwt):
        return OneRoster.http_post(route, data, jwt)

    def change_indicator(self, status, jwt):
        return OneRoster.http_post(Routes.INDICATOR, {'status': status}, jwt)

    def post_user(self, data, jwt, check):
        check = 'false' if check is False else 'true'
        return OneRoster.http_post(Routes.USERS + '?check=' + check, data, jwt)

    def delete_user(self, user_id, jwt):
        return OneRoster.http_delete(Routes.USERS + '/' + user_id, jwt)

    def get_user(self, user_id, jwt):
        return OneRoster.http_get(Routes.USERS + '/' + user_id, jwt)

    def get_users(self, jwt):
        return OneRoster.http_get(Routes.USERS, jwt)

    def patch_user(self, user_id, data, jwt):
        return OneRoster.http_patch(Routes.USERS + '/' + user_id, data, jwt)

    def get_lineitem(self, id, jwt):
        return OneRoster.http_get(Routes.LINE_ITEMS + '/' + id, jwt)

    def get_lineitems(self, jwt):
        return OneRoster.http_get(Routes.LINE_ITEMS, jwt)

    def post_lineitem(self, data, jwt, check):
        check = 'false' if check is False else 'true'
        return OneRoster.http_post(Routes.LINE_ITEMS + '?check=' + check, data, jwt)

    def post_lineitem_for_a_class(self, class_id, data, jwt, check):
        check = 'false' if check is False else 'true'
        route = Routes.CLASSES + '/' + str(class_id) + '/lineitems?check=' + check
        return OneRoster.http_post(route, data, jwt)

    def post_class(self, data, jwt, check):
        check = 'false' if check is False else 'true'
        return OneRoster.http_post(Routes.CLASSES + '?check=' + check, data, jwt)

    def post_result_for_a_class(self, class_id, data, jwt, check):
        check = 'false' if check is False else 'true'
        route = Routes.CLASSES + '/' + str(class_id) + '/results?check=' + check
        return OneRoster.http_post(route, data, jwt)

    def get_results(self, jwt):
        return OneRoster.http_get(Routes.CLASSES, jwt)

    def get_results_for_a_user(self, user_id, jwt):
        return OneRoster.http_get(Routes.USERS + '/' + user_id + '/results', jwt)

    def post_enrollment(self, class_id, data, jwt, check):
        check = 'false' if check is False else 'true'
        route = Routes.CLASSES + '/' + str(class_id) + '/enrollments?check=' + check
        return OneRoster.http_post(route, data, jwt)

    # Events

    def send_xapi(self, statement):
        """
        Send xAPI statements
        :param statement: JSON Object following the xAPI format
        :return: response
        """
        route = str(OpenLRW.URI) + str(Routes.XAPI)
        credentials = base64.b64encode('{}:{}'.format(self._username, self._password).encode())
        headers = {self._auth_header: 'Basic ' + credentials.decode(), "X-Experience-API-Version": "1.0.0"}
        response = requests.post(route, headers=headers, json=statement)
        Routes.print_post(route, response)
        if response.status_code == 400:
            raise BadRequestException(response)
        elif response.status_code == 500:
            raise InternalServerErrorException(response)

        return response

    def send_caliper(self, statement):
        """
        Send Caliper statement
        :param statement: JSON Object following the IMS Caliper format
        :return: response
        """
        route = str(OpenLRW.URI) + str(Routes.KEY_CALIPER)
        response = requests.post(route, headers={"Authorization": self._username}, json=statement)
        Routes.print_post(route, response)
        if response.status_code == 400:
            raise BadRequestException(response)
        elif response.status_code == 500:
            raise InternalServerErrorException(response)
        elif response.status_code == 404:
            raise OpenLRWClientException("Invalid Key")

        return response

    # Authentication

    def generate_jwt(self):
        """
        Create a JSON Web Token
        :return: a token
        """
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        data = {"username": self._username, "password": self._password}
        print(OpenLRW.URI)
        try:
            response = requests.post(OpenLRW.URI + Routes.AUTH, headers=headers, json=data)
            Routes.print_post(self.URI + Routes.AUTH, response)
            res = response.json()
            return res['token']
        except requests.RequestException:
            self.mail_server("Unable to get the JWT Token", sys.argv[0] + " was unable to get the token.")
            sys.exit("Unable to get the JWT Token")

    ######################################

    @staticmethod
    def pretty_error(reason, message):
        length = 80
        first_half_reason = ""
        second_half_reason = ""
        first_half_message = ""
        second_half_message = ""

        if length - len(reason) >= 0:
            number = length - len(reason)
            for i in range(0, number / 2):
                first_half_reason += " "
            second_half_reason = first_half_reason
            if number % 2 != 0:
                second_half_reason = first_half_reason + " "
        reason = first_half_reason + Colors.WARNING + reason + Colors.ENDC + second_half_reason
        if isinstance(message, list):
            message_line = ''
            for i in range(0, len(message)):
                msg = message[i]
                if length - len(msg) >= 0:
                    number = length - len(msg)
                    for j in range(0, number / 2):
                        first_half_message += " "
                    second_half_message = first_half_message
                    if number % 2 != 0:
                        second_half_message = first_half_message + " "
                message_line += "│" + first_half_message + msg + second_half_message + "│"
                if i is not len(message) - 1:
                    message_line += '\n'
        else:
            if length - len(message) >= 0:
                number = length - len(message)
                for i in range(0, number / 2):
                    first_half_message += " "
                second_half_message = first_half_message
                if number % 2 != 0:
                    second_half_message = first_half_message + " "
            message_line = "│" + first_half_message + message + second_half_message + "│"

        print("""
    ╭────────────────────────────────────────────────────────────────────────────────╮ 
    │      OpenLRW client       │               \033[31mERROR MESSAGE\033[0m                  ░▒▓▓▓▓│ 
    ├────────────────────────────────────────────────────────────────────────────────│ 
    │""" + reason + """│  
    """ + message_line + """
    ╰────────────────────────────────────────────────────────────────────────────────╯
            """)
        sys.exit(1)

    @staticmethod
    def pretty_message(reason, message):
        length = 80
        first_half_reason = ""
        second_half_reason = ""
        first_half_message = ""
        second_half_message = ""

        if length - len(reason) >= 0:
            number = length - len(reason)
            for i in range(0, number / 2):
                first_half_reason += " "
            second_half_reason = first_half_reason
            if number % 2 != 0:
                second_half_reason = first_half_reason + " "
        reason = first_half_reason + Colors.WARNING + reason + Colors.ENDC + second_half_reason
        if isinstance(message, list):
            message_line = ''
            for i in range(0, len(message)):
                msg = message[i]
                if length - len(msg) >= 0:
                    number = length - len(msg)
                    for j in range(0, number / 2):
                        first_half_message += " "
                    second_half_message = first_half_message
                    if number % 2 != 0:
                        second_half_message = first_half_message + " "
                message_line += "│" + first_half_message + msg + second_half_message + '│'
                if i is not len(message) - 1:
                    message_line += '\n'
        else:
            if length - len(message) >= 0:
                number = length - len(message)
                for i in range(0, number / 2):
                    first_half_message += " "
                second_half_message = first_half_message
                if number % 2 != 0:
                    second_half_message = first_half_message + " "
            message_line = "│" + first_half_message + message + second_half_message + "│"

        print("""
    ╭────────────────────────────────────────────────────────────────────────────────╮ 
    │        OpenLRW client         │                  """ + Colors.OKBLUE + """INFO\033[0m                    ░▒▓▓▓▓│ 
    ├────────────────────────────────────────────────────────────────────────────────│ 
    │""" + reason + """│  
    """ + message_line + """
    ╰────────────────────────────────────────────────────────────────────────────────╯
            """)
