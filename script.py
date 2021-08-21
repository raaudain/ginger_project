import json, boto3
from cred import var as v
from ringcentral import SDK


# RingCentral credentials
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
# Use when you want to test RingCentral api
bearer_token = platform._auth_header()
res = json.loads(platform.get("/restapi/v1.0/account/~/extension/~/message-store").text())

message_uri = ""

# Get latest message
for i in res["records"][0]["attachments"]:
    message_uri = i["uri"]

voicemail = platform.get(message_uri)


# print(bearer_token, message_uri, voicemail)


client = boto3.client("s3", aws_access_key_id=v.aws_access_key, aws_secret_access_key=v.aws_secret_key)

aws_bucket = "gingerproject"
aws_file_name = "ringcentral_voicemail"

client.upload_file("./README.md", aws_bucket, aws_file_name)