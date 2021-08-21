import json, boto3, requests, os
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
# Use to inspect RingCentral api in Insomnia or Postman
bearer_token = platform._auth_header()
res = json.loads(platform.get("/restapi/v1.0/account/~/extension/~/message-store").text())

message_uri = ""
file_name = ""

# Get latest message
for i in res["records"][0]["attachments"]:
    message_uri = i["uri"]
    file_name = f"ringcentral_voicemail_{i['id']}.mp3"

# Get audio data
voicemail = requests.get(message_uri, headers={"Authorization":bearer_token}).content

# Write audio data to .mp3 file
with open("voicemail.mp3", "wb") as f:
    f.write(voicemail)

client = boto3.client("s3", aws_access_key_id=v.aws_access_key, aws_secret_access_key=v.aws_secret_key)

aws_bucket = "gingerproject"

# Upload file to AWS S3 bucket and allow public read access
client.upload_file("./voicemail.mp3", aws_bucket, file_name, ExtraArgs={"ACL":"public-read"})

# Delete .mp3 file
os.remove("./voicemail.mp3")