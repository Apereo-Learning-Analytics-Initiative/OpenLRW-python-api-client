# OpenLRW Python API Client
<p align="center">
  <a href="https://badge.fury.io/py/openlrw"><img src="https://badge.fury.io/py/openlrw.svg" alt="PyPI version" height="18"></a>
</p>

> A Python Client making your scripts for OpenLRW easier



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
  # Do something...

# 2. Get all the users
try: 
  users = OpenLrw.get_users(jwt)
except ExpiredTokenException:
  print("JWT Expired")
  # Do something...
  
  
  

```
