# OpenLRW Python API Client


> A Python Client making your scripts for OpenLRW easier

<p align="center">
  <a href='https://www.python.org/dev/peps/pep-0008/'><img src="https://img.shields.io/badge/code%20style-pep8-orange.svg" alt="code style pep 8"></a>
  <a href="https://badge.fury.io/py/openlrw"><img src="https://badge.fury.io/py/openlrw.svg" alt="PyPI version"></a>
</p>

## Getting Started
` pip install openlrw `

## Usage

### Import the library
Add this import before using the next examples
```python
from openlrw.client import OpenLRW
from openlrw.exceptions import *
```

### Setup the client
```python
openlrw = OpenLRW(uri, username, password) # Create an instance of the client
openlrw.setup_email('localhost', 'script@openlrw.dev', 'your_email@domain.com')  # Optional: Allows you to send emails
```
### Create JSON Web Token
```python
jwt = openlrw.generate_jwt()
```
### Use OneRoster Routes
There are two ways to call OneRoster routes: by using a generic call or use implemented methods

#### Generic methods
```python
# GET
try: 
  classes = openlrw.oneroster_get('/api/classes', jwt)
except ExpiredTokenException:
  print("Error: JWT Expired)
  
# POST
try: 
  openlrw.oneroster_post('/api/classes', data, jwt)
except ExpiredTokenException:
  print("Error: JWT Expired)
except BadRequestException as e:
  print("Error: " + str(e.message.content))
except InternalServerErrorException as e:
  print("Error: " + str(e.message.content))
  
  
# PATCH
try: 
  openlrw.oneroster_patch('/api/ROUTE', data, jwt)
except ExpiredTokenException:
  print("Error: JWT Expired)
except BadRequestException as e:
  print("Error: " + str(e.message.content))
except InternalServerErrorException as e:
  print("Error: " + str(e.message.content))  
  
# DELETE
try: 
  openlrw.oneroster_delete('/api/ROUTE', jwt)
except ExpiredTokenException:
  print("Error: JWT Expired)
 
```

   #### Users
   Get a user
```python
try: 
  user = openlrw.get_user(user_id, jwt) # One user
  users = openlrw.get_users(jwt) # All the users
  new_user_res = openlrw.post_user(json, jwt, True) # Creates a user
  patch_user_res = openlrw.patch_user(user_id, json, jwt)
  delete_user_res = openlrw.delete_user(user_id, jwt)
except ExpiredTokenException:
  OpenLRW.pretty_error("Error", "JWT Expired")
```

   #### Line items
```python
try: 
    line_item = openlrw.get_lineitem("lineItemId", jwt)
    line_items = openlrw.get_lineitems(jwt)
    openlrw.post_lineitem_for_a_class("classId", json, jwt, True)
    openlrw.post_lineitem(json, jwt, True)
except ExpiredTokenException:
  OpenLRW.pretty_error("Error", "JWT Expired")
except InternalServerErrorException as e:
    script_name = str(sys.argv[0])
    openlrw.mail_server(script_name + " error", str(e.message)) # Send an email with the details
    exit()
except BadRequestException:
    OpenLRW.pretty_error("Bad Request", "Lorem ipsum")
```
  #### Class

```python
try:
    openlrw.post_class(json, jwt, True)
except InternalServerErrorException as e:
    script_name = str(sys.argv[0])
    openlrw.mail_server(script_name + " error", str(e.message)) # Send an email with the details
    exit()
except BadRequestException:
    OpenLRW.pretty_error("Bad Request", "Lorem ipsum")
```

  #### Result

```python
try: 
    result = openlrw.post_result_for_a_class("classId", json, jwt, True)
except ExpiredTokenException:
  OpenLRW.pretty_error("Error", "JWT Expired")
except InternalServerErrorException as e:
    script_name = str(sys.argv[0])
    openlrw.mail_server(script_name + " error", str(e.message)) # Send an email with the details
    exit()
except BadRequestException:
    OpenLRW.pretty_error("Bad Request", "Lorem ipsum")
```
  
  #### Send a Caliper statement
```python
try:
   response_code = openlrw.send_caliper(statement)
except BadRequestException as e:
   print(str(e.message))
   OpenLRW.pretty_error("Bad Request", "An error happened.")
except InternalServerErrorException as e:
   print(str(e.message))
   OpenLRW.pretty_error("Internal Server Error", "An error happened.")
   

OpenLRW.pretty_message("Script finished", "Ask the features you want in the pull requests!")     
   
  
```
