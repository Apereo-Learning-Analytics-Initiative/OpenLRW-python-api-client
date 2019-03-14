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
__version__ = "1"
__email__ = "xavier.chopin@univ-lorraine.fr"
__status__ = "Production"

import setuptools
from distutils.core import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='openlrw',
    version='1.0.1rc',
    description='Client library for Apereo OpenLRW API',
    long_description=readme(),
    keywords='apereo openlrw api client',
    url='https://github.com/Apereo-Learning-Analytics-Initiative/OpenLRW-python-api-client',
    author='Xavier Chopin',
    author_email='bonjour@xavierchop.in',
    license='ECL-2.0',
    packages=['openlrw'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Education',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ], requires=['requests']
)
