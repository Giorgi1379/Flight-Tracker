import requests
import pandas as pd
from src.settings import CLIENT_ID, CLIENT_SECRET, TOKEN_URL, API_URL, PARAMS
from src.logger import logger

class OpenSkyAPIClient:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.token_url = TOKEN_URL
        self.api_url = API_URL
        self.params = PARAMS
        self.access_token = None

    def get_access_token(self):
        try:
            payload = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }

            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            # waits 10 seconds if internet has problem or website
            response = requests.post(self.token_url, data=payload, headers=headers, timeout=10)
            response.raise_for_status()

            logger.info("new token generated successfully")
            self.access_token = response.json().get("access_token")
            return self.access_token
        except Exception as e:
            logger.error("token get error, " + str(e))
            self.access_token = None
            return None

    def fetch_flight_data(self, token=None):
        """it gets flight data and stores it in any file it wants from API"""
        current_token = token or self.access_token
        if not current_token:
            current_token = self.get_access_token()
            if not current_token:
                return None

        headers = {"Authorization": "Bearer " + str(current_token)}

        try:
            response = requests.get(self.api_url, params=self.params, headers=headers, timeout=10)

            #invalid token
            if response.status_code == 401:
                logger.warning("invalid token(401). needs upgrade.")
                return "EXPIRED"

            #API limit run out
            if response.status_code == 429:
                logger.warning("rate limit exceeded(429)")
                return None

            response.raise_for_status()
            data = response.json()

            #did data came and, and it is clear or not
            if data and "states" in data and data["states"] is not None:
                df = pd.DataFrame(data["states"])

                if df.empty:
                    logger.info("there is no flights at this time in that region")
                    return []

                df = df[[0, 1, 3, 5, 6, 7, 9, 10, 8]]
                df[1] = df[1].fillna("").astype(str).str.strip()
                df = df.dropna(subset=[3])
                return list(df.itertuples(index=False, name=None))
            else:
                logger.info("there is no flights at this time in that region")
                return []

        except requests.exceptions.RequestException as e:
            # catches internet disconnection or server inaccessibility
            logger.error("API connection error" + str(e))
            return None
