# https://developers.ringcentral.com/my-account.html#/applications
# Find your credentials at the above url, set them as environment variables, or enter them below

import json
from cred import var as v
from ringcentral import SDK


# PATH PARAMETERS
accountId = v.accountId
clientId = v.clientId
clientSecret = v.clientSecret
serverURL = v.serverURL
username = v.username
extension = v.extension
password = v.password

sdk = SDK(clientId, clientSecret, serverURL)
platform = sdk.platform()

# Be sure to reset the password in Sandbox. It's different from your dev account credentials.
platform.login(username, extension, password)
res = json.loads(platform.get("/restapi/v1.0/account/~/extension/~/message-store").text())

message_uri = ""

# Get first message from response
for i in res["records"][0]["attachments"]:
    print(i)
    message_uri = i["uri"]

bearer_token = platform._auth_header()
voicemail = platform.get(message_uri)


print(bearer_token, message_uri, voicemail)


