import logging
import requests
import urllib.parse

def get_all(url, path, headers):
    try:
        logging.info(f"Attempting to get list from: {url}")  # Debug line
        response = requests.get(urllib.parse.urljoin(url, path), headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return None