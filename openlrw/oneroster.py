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
import requests

from openlrw.exceptions import *
from openlrw.routes import Routes


__author__ = "Xavier Chopin"
__copyright__ = "Copyright 2019"
__license__ = "ECL-2.0"
__version__ = "1.0.3"
__email__ = "xavier.chopin@univ-lorraine.fr"
__status__ = "Production"


class OneRoster:

    def __init__(self):
        pass

    @staticmethod
    def http_get(route, jwt):
        """
        For OneRoster routes('/api/:route')
        :param route:
        :param jwt:
        :return:
        """
        from openlrw.client import OpenLRW
        response = requests.get(str(OpenLRW.URI + route), headers={'X-Requested-With': 'XMLHttpRequest', 'Authorization': 'Bearer ' + str(jwt)})
        Routes.print_get(route, response)

        if response.status_code == 401:
            raise ExpiredTokenException
        elif response.status_code == 404:
            return None

        return response.content

    @staticmethod
    def http_post(route, data, jwt):
        """
        For OneRoster routes('/api/:route')
        :param route:
        :param jwt:
        :param data
        :return:
        """
        from openlrw.client import OpenLRW
        response = requests.post(str(OpenLRW.URI + route), headers={'X-Requested-With': 'XMLHttpRequest', 'Authorization': 'Bearer ' + str(jwt)}, json=data)
        Routes.print_post(route, response)

        if response.status_code == 401:
            raise ExpiredTokenException
        elif response.status_code == 400:
            raise BadRequestException(response)
        elif response.status_code == 500:
            raise InternalServerErrorException(response)

        return response

    @staticmethod
    def http_delete(route, jwt):
        """
        For OneRoster routes('/api/:route')
        :param route:
        :param jwt:
        :return:
        """
        from openlrw.client import OpenLRW
        response = requests.delete(str(OpenLRW.URI + route), headers={'X-Requested-With': 'XMLHttpRequest', 'Authorization': 'Bearer ' + str(jwt)})
        Routes.print_delete(route, response)
        if response.status_code == 401:
            raise ExpiredTokenException(response)
        elif response.status_code == 500:
            raise InternalServerErrorException(response)

        return True

    @staticmethod
    def http_patch(route, data, jwt):
        """
        For OneRoster routes('/api/:route')
        :param route:
        :param jwt:
        :param data
        :return:
        """
        from openlrw.client import OpenLRW
        response = requests.patch(str(OpenLRW.URI + route), headers={'X-Requested-With': 'XMLHttpRequest', 'Authorization': 'Bearer ' + str(jwt)}, json=data)
        Routes.print_patch(route, response)
        if response.status_code == 401:
            raise ExpiredTokenException
        elif response.status_code == 400:
            raise BadRequestException(response)
        elif response.status_code == 500:
            raise InternalServerErrorException(response)

        return response
