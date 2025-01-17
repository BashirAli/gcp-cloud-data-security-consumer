from dotenv import load_dotenv

# Load the .env file
load_dotenv()


def main():
    pass

if __name__ == '__main__':
    main()

# TODO
"""
1. read gnupg keys from secret manager
2. creates new table in bq and assigns policy tags if not already existing
3. reads from gcs
4. decrypts with gunpg
5. writes to bq table


"""