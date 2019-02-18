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


class OneRoster:

    def http_get(self, route, jwt):
        """
        For OneRoster routes('/api/:route')
        :param route:
        :param jwt:
        :return:
        """
        response = requests.get(self._url + route, headers={'Authorization': 'Bearer ' + jwt})
        Routes.print_get(route, response)
        return False if response.status_code == 401 else response.content  # if token expired

    def http_post(self, route, jwt, data):
        """
        For OneRoster routes('/api/:route')
        :param route:
        :param jwt:
        :return:
        """
        response = requests.post(self._url + route, headers={'Authorization': 'Bearer ' + jwt}, json=data)
        Routes.print_post(route, response)
        return response.status_code != 401  # if token expired

    def http_delete(self, route, jwt):
        """
        For OneRoster routes('/api/:route')
        :param route:
        :param jwt:
        :return:
        """
        response = requests.delete(self._url + route, headers={'Authorization': 'Bearer ' + jwt})
        Routes.print_delete(route, response)
        return response.status_code != 401  # if token expired