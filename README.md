# gcp-cloud-data-security-consumer

This repository presents some best practices when processing, storing and accessing data. It does the following:

- Reads encrypted files stored in Google Cloud Storage 
- Decrypts these files with the GNUPG Python package, keys being retrieved from GCP Secret Manager not from any hardcoded values
- Writes this file to a policy tag-constrained BigQuery table 

- It also separately checks if the table already exists with policy tags, and if not, recreates it and reassigns the tags 


## Getting Started
1. Install poetry (if required) and the poetry files in your chosen virtual environment 

```
pip install poetry 
poetry install
```

2. Create a `.env` file and fill in the following variables

```
GCP_PROJECT_ID=<<YOUR_PROJECT_ID>>
GCS_BUCKET=<<YOUR_GCS_BUCKET>>
PRIV_KEY_SECRET_ID=<<SECRET_MANAGER_LOCATION_FOR_PRIVATE_KEY>>
PASSPHRASE_SECRET_ID=<<SECRET_MANAGER_LOCATION_FOR_PASSPHRASE>>
```
3. Setup GPG public and private keys: 
- 
4. Upload the private key and the passphrase to Secret Manager under the following locations: `<<SECRET_MANAGER_LOCATION_FOR_PRIVATE_KEY>>` and `<<SECRET_MANAGER_LOCATION_FOR_PASSPHRASE>>`

5. Encrypt test data using the example command 

and then upload the created ___ file in to `<<YOUR_GCS_BUCKET>>`


6. run `main()`






*Developed in Python 3.12.0*