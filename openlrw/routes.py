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


__author__ = "Xavier Chopin"
__copyright__ = "Copyright 2019"
__license__ = "ECL-2.0"
__version__ = "1.0.0"
__email__ = "xavier.chopin@univ-lorraine.fr"
__status__ = "Production"

from openlrw.exceptions import Colors


class Routes:
    XAPI = '/xAPI/statements'
    USERS = '/api/users'
    ACADEMIC_SESSIONS = '/api/academicsessions'
    AUTH = '/api/auth/token'
    CALIPER = '/api/caliper'
    CLASSES = '/api/classes'
    COURSES = '/api/courses'
    ENROLLMENTS = '/api/enrollments'
    LINE_ITEMS = '/api/lineitems'
    RISK = '/api/risk'
    KEY_CALIPER = '/key/caliper'

    @staticmethod
    def print_get(route, response):
        print(Colors.OKGREEN+ '[GET]' + Colors.ENDC + ' ' + route + ' - Response: ' + str(response.status_code))

    @staticmethod
    def print_post(route, response):
        print(Colors.OKBLUE + '[POST]' + Colors.ENDC + ' ' + route + ' - Response: ' + str(response.status_code))

    @staticmethod
    def print_delete(route, response):
        print(Colors.FAIL + '[DELETE]' + Colors.ENDC + ' ' + route + ' - Response: ' + str(response.status_code))



