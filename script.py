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
# r = platform.get(f"/restapi/v1.0/account/{accountId}").text()
# print(json.loads(r))
res = json.loads(platform.get('/restapi/v1.0/account/~/extension/~/message-store').text())

message = ""

# Get message from response
for i in res["records"][0]["attachments"]:
    message += f"{i['uri']}"

print(message)
# print(json.loads(resp)["records"][0]["attachments"][1])
# for record in resp.text().records:
#     print(record)