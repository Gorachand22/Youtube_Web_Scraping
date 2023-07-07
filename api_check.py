from googleapiclient.discovery import build
import logging

class API:
    def __init__(self):
        self.token = ''

    def check_api(self, api_token):
        try:
            build('youtube', 'v3', developerKey=str(api_token))
        except Exception as e:
            logging.error(f"API Key Check Error: {str(e)}")
            return 0
        else:
            self.token = api_token
            return 1
