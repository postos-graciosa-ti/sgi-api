# Why is this needed?
# because we are using a free instance of render, which kills the application after 50 seconds of inactivity

import os
import time

import requests

keep_alive_endpoint = os.environ.get("KEEP_ALIVE_ENDPOINT")


def keep_alive_function():
    while True:
        try:
            requests.get(keep_alive_endpoint)

        except Exception as e:
            print("Erro ao tentar manter o servidor ativo:", e)

        time.sleep(30)
