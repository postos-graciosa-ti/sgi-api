import os
import time
from datetime import datetime, timedelta

import requests


def run_daily_custom_notification_check():
    while True:
        now = datetime.now()

        next_run = now.replace(hour=6, minute=0, second=0, microsecond=0)

        if next_run <= now:
            next_run += timedelta(days=1)

        wait_seconds = (next_run - now).total_seconds()

        print(f"Next run scheduled at {next_run.strftime('%Y-%m-%d %H:%M')}")

        time.sleep(wait_seconds)

        try:
            print("Sending request to /verify-custom-notifications...")

            response = requests.get(
                os.environ.get("VERIFY_CUSTOM_NOTIFICATION_ENDPOINT")
            )

            print(f"Status: {response.status_code}, Response: {response.text}")

        except Exception as e:
            print(f"Error during request: {e}")
