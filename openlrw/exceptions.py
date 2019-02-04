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

import sys

try:
    import rangex as sizeof
except ImportError:
    import range as sizeof


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class OpenLRWClientException(Exception):
    pass

    @staticmethod
    def pretty_error(reason, message):
        length = 80
        first_half_reason = ""
        second_half_reason = ""
        first_half_message = ""
        second_half_message = ""

        if length - len(reason) >= 0:
            number = length - len(reason)
            for i in sizeof(0, number / 2):
                first_half_reason += " "
            second_half_reason = first_half_reason
            if number % 2 != 0:
                second_half_reason = first_half_reason + " "
        reason = first_half_reason + Colors.WARNING + reason + Colors.ENDC + second_half_reason
        if isinstance(message, list):
            message_line = ''
            for i in sizeof(0, len(message)):
                msg = message[i]
                if length - len(msg) >= 0:
                    number = length - len(msg)
                    for j in sizeof(0, number / 2):
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
                for i in sizeof(0, number / 2):
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
            for i in sizeof(0, number / 2):
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
                    for j in sizeof(0, number / 2):
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
                for i in sizeof(0, number / 2):
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
