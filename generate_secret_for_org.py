import requests
from requests.exceptions import HTTPError
import json
import argparse
import os
import time
from base64 import b64encode
from nacl import encoding, public

# Process arguments
parser = argparse.ArgumentParser(
    description="Encrypt and encode a string for an organization",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--url",
    dest="url",
    default="https://api.github.com",
    help="URL of Github API endpoint",
)
parser.add_argument(
    "--org",
    dest="org",
    required=True,
    help="Organization to get the public key for and use to encrypt string",
)
parser.add_argument(
    "--input",
    dest="input",
    required=True,
    help="String to encrypt and encode",
)

args = parser.parse_args()

## Get API token from environment variable
token = os.getenv("GITHUB_TOKEN")
if token is None:
    raise SystemExit("Environment variable GITHUB_TOKEN must be set")

# Used in multiple functions
urlBase = args.url
org=args.org
input=args.input

## Headers passed to every API call
headers = {
    "Content-Type": "application/json",
    "X-GitHub-Api-Version": "2022-11-28",
    "Authorization": f"Bearer {token}",
}

# Hit the GitHub API and return the JSON response
# url: URL to hit
# method: HTTP method to use (default: GET)
# headers: HTTP headers to use
# data: Data to send in the request (default: {})
# allowRedirects: Allow redirects, otherwise return empty JSON (default: True)
#   Transferred repos return 301 redirects to their new home
# allowNotFound: Accept 404 errors silently (default: False)
#   Used to ignore 404 errors when checking if something exists
# Sleeps for 1 second after doing mutative requests (PUT, POST, DELETE) as per GitHub Rest API best practices
def getJsonResponse(url,method="GET",headers=headers,data={},allowRedirects=True, allowNotFound=False):
    jsonResponse = {}
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, allow_redirects=allowRedirects)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, data=data)
            time.sleep(1)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=data)
            time.sleep(1)
        elif method == "PUT":
            response = requests.put(url, headers=headers, data=data)
            time.sleep(1)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
            time.sleep(1)
        else:
            print(f"Unsupported method: {method}")
            exit(1)
        response.raise_for_status()

        if allowRedirects == False and response.status_code == 301:
            jsonResponse = {}
        elif response.text:
            jsonResponse = response.json()

    except HTTPError as http_err:
        # Debugging why this happens sometimes
        if http_err.response.status_code == 422:
            print(
                f"ERROR: API responds with validation failed, response was {response.content}"
            )
        if allowNotFound:
           if http_err.response.status_code != 404:
            print(f"ERROR: HTTP error occured: {http_err} while accessing {url}")
            exit(1)
        else:
            print(f"ERROR: HTTP error occured: {http_err} while accessing {url}")
            exit(1)

    except Exception as err:
        print(f"ERROR: Other error occured: {err} while accessing {url}")
        exit(1)
    return jsonResponse


# Get public key from Github Org
def get_org_public_key(org):
    url = f"{urlBase}/orgs/{org}/actions/secrets/public-key"
    response = getJsonResponse(url)
    if response['key']:
      return response['key_id'], response['key']
    else:
      print(f"ERROR: Could not get public key for {org}")
      exit(1)

# Encrypt a Unicode string using the public key
def encrypt(public_key: str, secret_value: str) -> str:
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

# Add/update secret for an organization
def generate_encrypted_string_for_org(org,input):

    # Encrypt the secret value
    key_id, public_key = get_org_public_key(org)
    return(encrypt(public_key, input))
    
def main():
    print(f'Encrypting input: "{input}" with public_key for org {org}')
    output = generate_encrypted_string_for_org(org,input)
    print(output)

if __name__ == "__main__":
    main()