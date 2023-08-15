import urllib.request
import sys
import re
import base64
from urllib.parse import urlparse

"""
accessing a page, extracting the realm, 
then doing the authentication. We'll use 
a regular expression to pull the scheme 
and realm out of the response header.
"""

theurl = 'http://www.someserver.com/somepath/somepage.html'
"""
to run this program you need to supply
protected page with your username and password
"""

username = "Nelly"
password = "12345678"

req = urllib.request(theurl)
try:
    handle = urllib.request.urlopen(req)
except IOError as e:
    # Here we *want* to fail
    pass
else:
    # if we don't fail then the page isn't protected
    print("This page isn't protected by authentication")
    sys.exit(1)
if not hasattr(e, "code") or e.code != 401:
    # We got an error but not 401 error
    print("This page isn't protected by authentication.")
    print("But we failed for another reason.")
    sys.exit(1)

authline = e.header["www-authenticate"]
"""
gets the www-authentication line from the headers
which has the authentication scheme and realm in it
"""

authobj = re.compile(r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"]([^'"]+)['"]''', re.IGNORECASE)
# This regular expression is used to extract scheme and realm

matchobj = authobj.match(authline)

if not matchobj:
    """
    if the authline isn't matched by the regular expression
    then something is wrong
    """
    print("The authentication header is badly formed", authline)
    sys.exit(1)

scheme = matchobj.group(1)
realm = matchobj.group(2)
"""
Extracting the scheme and the realm 
from the header
"""

if scheme.lower() != "basic":
    print("This example only works with BASIC authentication")
    sys.exit(1)

base64string = base64.encode("%s:%s" % (username, password))[:-1]
authheader = "Basic %s" % base64string
req.add_header("Authorization", authheader)

try:
    handle = urllib.request(req)
except IOError as e:
    # here we shouldn't fail the username/password is right
    print("It looks like the username or password is wrong")
    sys.exit(1)
thepage = handle.read()
