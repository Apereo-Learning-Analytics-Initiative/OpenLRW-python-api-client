# OpenLRW Python API Client


> A Python Client making your scripts for OpenLRW easier

<p align="center">
  <a href='https://www.python.org/dev/peps/pep-0008/'><img src="https://img.shields.io/badge/code%20style-pep8-orange.svg" alt="code style pep 8"></a>
  <a href="https://badge.fury.io/py/openlrw"><img src="https://badge.fury.io/py/openlrw.svg" alt="PyPI version"></a>
</p>

## Getting Started
` pip install openlrw `

## Usage

#### 1. Interacting with the User collection

```python

from openlrw.client import OpenLRW
from openlrw.exceptions import ExpiredTokenException

OpenLrw = OpenLRW(uri, username, password) # Create an instance of the client
jwt = OpenLrw.generate_jwt() # Generate a JSON Web Token for using OneRoster routes

# 1. Get the user john_doe
try: 
  user = OpenLrw.get_user('john_doe', jwt)
except ExpiredTokenException:
  OpenLRW.pretty_error("Error, "JWT Expired")

# 2. Get all the users
try: 
  users = OpenLrw.get_users(jwt)
except ExpiredTokenException:
  OpenLRW.pretty_error("Error, "JWT Expired")
  
  
  

```
