import json, requests, boto3, os, sys
from ringcentral import SDK
from cred.var import client_id, client_secret, server_url, username, extension, password, aws_access_key, aws_secret_key, s3_bucket, s3_object_url


# Comment line 3 and uncomment below if you want to input credentials directly into script
# # RingCentral credentials
# client_id = ""
# client_secret = ""
# server_url = ""
# username = ""
# extension = ""
# password = ""

# # AWS Credentials
# aws_access_key = ""
# aws_secret_key = ""
# s3_bucket = ""
# s3_object_url = ""

sdk = SDK(client_id, client_secret, server_url)
platform = sdk.platform()
platform.login(username, extension, password)
res = json.loads(platform.get("/restapi/v1.0/account/~/extension/~/message-store").text())

# Checks if there are messages
if len(res["records"]):
    message_uri = ""
    file_name = ""

    # Get latest message
    for i in res["records"][0]["attachments"]:
        message_uri = i["uri"]
        file_name = f"ringcentral_voicemail_{i['id']}.mp3"

    # Get audio data
    bearer_token = platform._auth_header()
    voicemail = requests.get(message_uri, headers={"Authorization":bearer_token}).content

    mp3_file = "./" + file_name

    # Write audio data to .mp3 file
    with open(mp3_file, "wb") as f:
        f.write(voicemail)
        f.close()

    # Upload file to AWS S3 bucket and allow public read access
    client = boto3.client("s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    client.upload_file(mp3_file, s3_bucket, file_name, ExtraArgs={"ACL":"public-read"})

    print("Object URL: " + s3_object_url + file_name)
    os.remove(mp3_file)
else:
    print("No messages")

sys.exit(0)