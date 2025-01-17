# gcp-cloud-data-security-consumer

This repository presents some best practices when processing, storing and accessing data. It does the following:

- Reads encrypted files stored in Google Cloud Storage 
- Decrypts these files with the GNUPG Python package, keys being retrieved from GCP Secret Manager
- Writes this file to a policy tag-constrained BigQuery table 

- It also separately checks if the table already exists with policy tags, and if not, recreates it and reassigns the tags 


## Getting Started

1. Create a `.env` file and fill in the following variables

```
GCP_PROJECT_ID=<YOUR_PROJECT_ID>>
```

2. Install poetry (if required) and the poetry files in your chosen virtual environment 

```
pip install poetry 
poetry install
```

3. run `main()`






*Developed in Python 3.12.0*