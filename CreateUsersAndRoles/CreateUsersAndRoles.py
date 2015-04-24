# Demonstrates how to start a service by starting the geometry service
# This service is included with every ArcGIS Server and is stopped by default

# For Http calls
import json

import urllib,httplib

import sys

import getpass

import codecs

def main(argv=None):

    # Ask for admin user name and password

    username = "mcfoi" # raw_input("Enter user name: ")
    password = getpass.getpass("Enter password: ")

    # Ask for server name and the port
    serverName = "localhost" # raw_input("Enter server name: ")
    serverPort = "6080" # raw_input("Enter server port: ")

    # Get a token and connect
    token = getToken(username, password, serverName, serverPort)

    if token == "":
        sys.exit(1)

    # Input file that contains the role information
    rolesFile = "C:\Users\mfoi\Dropbox\ESRI Documents\Scripts Python\CreateUsersAndRoles_inputRoles.txt" # raw_input("Path to pipe-delimited text file containing roles: ")

    # Input file that contains the user information
    usersFile = "C:\Users\mfoi\Dropbox\ESRI Documents\Scripts Python\CreateUsersAndRoles_inputUsers.txt" # raw_input("Path to pipe-delimited text file containing users: ")

    # Dictionaries to store user and role information
    roles = {}
    rolePrivileges = {}

    users = {}
    userRoles = {}

    # Loop through the roles file and create the roles
    # Add the user information to a dictionary
    num = 0
    for roleRow in readlinesFromInputFile(rolesFile):
        roles["role" + str(num)] = {"rolename":roleRow[0],"description":roleRow[1]}
        rolePrivileges["rolePrivilege" + str(num)] = {"rolename":roleRow[0], "privilege":roleRow[2]}
        num +=1

    # Read the user's file
    num = 0
    for userRow in readlinesFromInputFile(usersFile):
        # Add the user information to a dictionary
        users["user" + str(num)] = {"username":userRow[0],"password":userRow[1],"email":userRow[2], "fullname":userRow[3],"description":userRow[4].rstrip()}
        userRoles["userRole"+str(num)] = {"username" : userRow[0],"roles":userRow[5]}
        num +=1

    # Call helper functions to add users and roles
    addRoles(roles,serverName, serverPort,token)
    assignPrivilegeToRole(rolePrivileges, serverName, serverPort, token)
    addUsers(users,serverName, serverPort,token)
    addUsersToRoles(userRoles, serverName, serverPort, token)

# A function that reads lines from the input file
def readlinesFromInputFile(filename, delim='|'):
    file = codecs.open(filename,'r','utf-8-sig')
    for line in file.readlines():
        # Remove the trailing whitespaces and the newline characters
        line = line.rstrip()

        if line.startswith('#') or len(line) == 0:
            pass # Skip the lines that contain # at the beginning or any empty lines
        else:
            # Split the current line into list
            yield line.split(delim)
    file.close()

# A function that will post HTTP POST request to the server
def postToServer(serverName, serverPort, url, params):

    httpConn = httplib.HTTPConnection(serverName, serverPort)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    # URL encode the resource URL
    url = urllib.quote(url.encode('utf-8'))

    # Build the connection to add the roles to the server
    httpConn.request("POST", url, params, headers)

    response = httpConn.getresponse()
    data = response.read()
    httpConn.close()

    return (response, data)

# Helper function that adds the roles
def addRoles(roleDict, serverName, serverPort, token):

    for roleToAdd in roleDict:

        role = roleDict[roleToAdd]
        print "Adding the role: " + role['rolename']

        # URL for adding a role
        addroleURL = "/arcgis/admin/security/roles/add"
        params = urllib.urlencode({'token':token,'f':'json','rolename':role['rolename'],'description':role['description']})
        response, data = postToServer(serverName, serverPort, addroleURL, params)

        if (response.status != 200 or not assertJsonSuccess(data)):
            print "Error adding the role: " + role['rolename']
            print str(data)
        else:
            print "Added the role '" + role['rolename'] + "' successfully"

# Helper function that assigns privileges to roles
def assignPrivilegeToRole(privileges, serverName, serverPort, token):

        for privilegeToAssign in privileges:

            privilege = privileges[privilegeToAssign]

            # URL for assigning a privilege to a role
            assignPrivilegeURL = "/arcgis/admin/security/roles/assignPrivilege"
            params = urllib.urlencode({'token':token,'f':'json','rolename':privilege['rolename'],'privilege':privilege['privilege']})

            response, data = postToServer(serverName, serverPort, assignPrivilegeURL, params)

            if (response.status != 200 or not assertJsonSuccess(data)):
                print "Could not assign the privilege '" + privilege['privilege'] + "' to the role '" + privilege['rolename'] + "'"
                print str(data)
            else:
                print "Assigned the privilege '" + privilege['privilege'] + "' to the role '" + privilege['rolename'] + "' successfully"

# Helper function that adds the users
def addUsers(userDict,serverName, serverPort, token):

    for userAdd in userDict:
        user = userDict[userAdd]

        print "Adding the user:" + user['username']

        # URL for adding a user
        addUserURL = "/arcgis/admin/security/users/add"
        params = urllib.urlencode({'token':token,'f':'json','username':user['username'],'password':user['password'],'fullname':user['fullname'],'description':user['description'],'email':user['email']})

        response, data = postToServer(serverName, serverPort, addUserURL, params)

        if (response.status != 200 or not assertJsonSuccess(data)):
            print "Error adding user: " + user['username']
            print str(data)
        else:
            print "Added the user '" + user['username'] + "' successfully"

# Helper function that adds users to roles
def addUsersToRoles(userRoleDict,serverName, serverPort, token):

    for userAdd in userRoleDict:

        userRole = userRoleDict[userAdd]
        print "Adding the user '" + userRole['username'] + "' to the role(s) '" + userRole['roles'] + "'"

        addUserToRolesURL = "/arcgis/admin/security/users/assignRoles"
        params = urllib.urlencode({'token':token,'f':'json',"userName":userRole['username'],"roles":userRole['roles']})

        response, data = postToServer(serverName, serverPort, addUserToRolesURL, params)

        if (response.status != 200 or not assertJsonSuccess(data)):
            print "Could not add user '" + userRole['username'] + "' to the role(s) '" + userRole['roles'] + "'"
            print str(data)
        else:
            print "Added the user '" + userRole['username'] + "' to the role(s) '" + userRole['roles'] + "' successfully"


def getToken(username, password, serverName, serverPort):

    httpConn = httplib.HTTPConnection(serverName, serverPort)

    tokenURL = "/arcgis/admin/generateToken"

    params = urllib.urlencode({'username': username, 'password': password,'client': 'requestip', 'f': 'json'})

    response, data = postToServer(serverName, serverPort, tokenURL, params)

    if (response.status != 200 or not assertJsonSuccess(data)):
        print "Error while fetching tokens from admin URL. Please check if the server is running and ensure that the username/password provided are correct"
        print str(data)
        return
    else:
        # Extract the token from it
        token = json.loads(data)
        return token['token']


# A function that checks that the JSON response received from the server does not contain an error
def assertJsonSuccess(data):
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        return False
    else:
        return True

# Script start
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))