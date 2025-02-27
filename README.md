# gcp-cloud-data-security-consumer

This repository presents some best practices when processing, storing and accessing data. It does the following:

- Reads encrypted files stored in Google Cloud Storage 
- Decrypts these files with the GNUPG Python package, keys being retrieved from GCP Secret Manager not from any hardcoded values
- Writes this file to a policy tag-constrained BigQuery table 

- It also separately checks if the table already exists with policy tags, and if not, recreates it and reassigns the tags 


## Getting Started
1. Install poetry (if required) and the poetry files in your chosen virtual environment and activate it

```
pip install poetry 
poetry install
```

2. Create a `.env` file and fill in the following variables

```
GCP_PROJECT_ID=<<YOUR_PROJECT_ID>>
GCS_BUCKET=<<YOUR_GCS_BUCKET>>
DECRYPTION_KEY_SECRET_ID=<<SECRET_MANAGER_LOCATION_FOR_PRIVATE_KEY>>
DECRYPTION_PASS_SECRET_ID=<<SECRET_MANAGER_LOCATION_FOR_PASSPHRASE>>
DATASET_ID=<<YOUR_BQ_DATASET_ID>>
TABLE_ID=<<YOUR_BQ_TABLE_ID>>
GCP_PROJECT_LOCATION=<<YOUR_PROJECT_LOCATION>>
```
3. Setup your own GPG public and private keys
- CD in to the repository
- Run the following script:
```
python scripts/generate_gpg_keys.py --name "<<YOUR_NAME>>" --email "<<YOUR_EMAIL>>" --passphrase "<<YOUR_PASSPHRASE>>" --key-length <<KEY_LENGTH>> --output-dir "<<KEY_DIRECTORY>>"
```
4. Encrypt test data using the example command 

```
python scripts/encrypt_data.py --json-file "<<PATH_TO_JSON_FILE>>" --public-key "<<PATH_TO_PUBLIC_KEY>>"
```

5. Upload the private key and your passphrase to Secret Manager under the following locations: `<<SECRET_MANAGER_LOCATION_FOR_PRIVATE_KEY>>` and `<<SECRET_MANAGER_LOCATION_FOR_PASSPHRASE>>`


6. Upload the encrypted `.json.gpg` file in to `<<YOUR_GCS_BUCKET>>` with the file name `<<GCS_FILE_NAME>>`


7. run `main()`






*Developed in Python 3.12.0*