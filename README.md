# Add Org Secrets
This script is used to add or update secrets to a GitHub organization, using a csv file for the list of secret names and values

The secrets visibility is set to all repos in the organization.

It requires the GITHUB_TOKEN environment to be set with a PAT that can read the organization public key, and create and/or update organization secrets, admin:org permission

## Usage

```
python add_org_secrets.py -h                                                                                                                                                                 (main|…5)
usage: add_org_secrets.py [-h] [--url URL] --org ORG --csvfile CSVFILE [--overwrite]

Add or update secrets to a GitHub organization

options:
  -h, --help         show this help message and exit
  --url URL          URL of Github API endpoint (default: https://api.github.com)
  --org ORG          Org to add secret to (default: None)
  --csvfile CSVFILE  csv file with each line in the format secretname,secretvalue (default: None)
  --overwrite        Set if to allow existing secrets to be overwritten, otherwise an error is thrown (default: False)
  ```

See ```secret.csv.sample``` for an example input file
