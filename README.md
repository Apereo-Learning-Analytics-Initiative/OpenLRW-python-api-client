# OpenLRW Python API Client
> A Python Client making your scripts for OpenLRW easier


## Getting Started
` pip install openlrw `

## Usage

#### 1. Getting a user

```python

from openlrw.client import OpenLRW

## /!\ Credentials should be in a settings file /!\ ##
URI = "http://localhost:9966"
USERNAME = "" 
PASSWORD = ""


openLRW = OpenLRW(uri, username, password) # Create an instance of the client

jwt = openLRW.generate_jwt() # Generate a JSON Web Token for using OneRoster routes

user = openLRW.get_user('john_doe', jwt) # Get the user 'John Doe'


```
