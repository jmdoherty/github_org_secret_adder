# Org Secret Adder

Scripts for generating, adding or updating GitHub Action secrets in an organization

## generate_secret_for_org.py
Encrypt and encode a string to be used as a secret. Result can be used in the [Terraform Resource](https://registry.terraform.io/providers/integrations/github/latest/docs/resources/actions_organization_secret#encrypted_value)

It requires the GITHUB_TOKEN environment to be set with a PAT that can read the organization public key (admin:org permission)

### Usage

```
python generate_secret_for_org.py -h
usage: generate_secret_for_org.py [-h] [--url URL] --org ORG --input INPUT

Encrypt and encode a string for an organization

options:
  -h, --help     show this help message and exit
  --url URL      URL of Github API endpoint (default: https://api.github.com)
  --org ORG      Organization to get the public key for and use to encrypt string (default: None)
  --input INPUT  String to encrypt and encode (default: None)
``` 

### Example
```
python generate_org_secret.py --org moneris-enterprise-migration-test --input "This is a test"
Encrypting input: "This is a test" with public_key for org moneris-enterprise-migration-test
G76WICHgR1VSptYCb1Gqtxw+JwrnekVmlYKsvlic2nzqdS+EGUACeGKH6bCnqOYUkQOkvBIXVi10dnWmlSE=
```


## add_org_secrets.py
Add or update secrets directly in a GitHub organization, using a csv file for the list of secret names and values

The secrets visibility is set to all repos in the organization.

It requires the GITHUB_TOKEN environment to be set with a PAT that can read the organization public key, and create and/or update organization secrets (admin:org permission)

### Usage

```
python add_org_secrets.py -h
usage: add_org_secrets.py [-h] [--url URL] --org ORG --csvfile CSVFILE [--overwrite]

Add or update secrets to a GitHub organization

options:
  -h, --help         show this help message and exit
  --url URL          URL of Github API endpoint (default: https://api.github.com)
  --org ORG          Org to add secret to (default: None)
  --csvfile CSVFILE  csv file with each line in the format secretname,secretvalue (default: None)
  --overwrite        Set if to allow existing secrets to be overwritten, otherwise an error is thrown (default: False)

```

### Example
```
python add_org_secrets.py --org example-org --csvfile secret.csv.sample 
INFO: Adding secrets in secret.csv.sample to GitHub orgaization example-org
INFO: Adding or updating secret notarealsecretname1
INFO: Adding or updating secret notarealsecretname2 
INFO: Adding or updating secret notarealsecretname3 
INFO: Adding or updating secret notarealsecretname4 
INFO: Adding or updating secret notarealsecretname5

```

See ```secret.csv.sample``` for an example input file
