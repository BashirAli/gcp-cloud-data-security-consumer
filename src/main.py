from dotenv import load_dotenv
from core.consumer import DataConsumer


# Load the .env file
load_dotenv()


def main():
    data_consumer = DataConsumer()
    data_consumer.decrypt_and_ingest_data()

if __name__ == '__main__':
    main()