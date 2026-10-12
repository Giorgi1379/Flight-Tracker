from api_client import OpenSkyAPIClient
from database import DatabaseManager
from logger import logger

def run_pipeline():
    logger.info("Starting pipeline")

    api_client = OpenSkyAPIClient()
    db_manager = DatabaseManager()

    token = api_client.get_access_token()
    if not token:
        logger.error("Could not get access token")
        return

    #get data from API
    flight_data = api_client.fetch_flight_data(token)

    if flight_data == "EXPIRED":
        logger.info("retry with new token ")
        token = api_client.get_access_token()
        flight_data = api_client.fetch_flight_data(token)

    #type data in database
    if flight_data and isinstance(flight_data, list):
        db_manager.insert_flight_data(flight_data)
        logger.info("Successfully inserted flight data")
    else:
        logger.info("No flight data")


if __name__ == "__main__":
    run_pipeline()