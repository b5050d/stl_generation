"""
This script is for the backend to communcate with the
frontend via redis. The idea is that this is where
the stl generation gets commanded.
"""

import redis
import os
import time
from modules.process_byte_streams import cookie_cutter


REDIS_HOST = os.getenv("REDIS_HOST", "custom-redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_QUEUE = os.getenv("REDIS_QUEUE", "incoming_queue")
REDIS_RESPONSE_CHANNEL = os.getenv("REDIS_RESPONSE_CHANNEL", "response_channel")


class BackendLink:
    """
    Class to handle the backend link to the frontend
    """

    def __init__(self):
        """
        Initialise the backend link
        """
        print("Setting up the Backend Link")
        self.set_up_redis()

    def set_up_redis(self):
        """
        Set up Redis
        """
        print("Setting up Redis")
        self.redis = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, decode_responses=False
        )

    def process_message(self, message):
        """
        Process an incoming message
        """
        print("Processing Message")
        key, value = message
        print(f"Got message from {key}: {value}")

        # Check if the message is valid
        data_key = value.decode()

        # Go get the data at that key
        data = self.redis.get(data_key)
        print(f"Read the data from the key: {key}")

        # Call the STL Generation
        print("calling the backend")
        response = cookie_cutter(data)
        time.sleep(1)

        # Add the processed bytes into redis
        self.redis.set(data_key, response.getvalue())

        # Publish to the sub channel to let the web app know
        # that a response is ready for it
        self.redis.publish(REDIS_RESPONSE_CHANNEL, data_key)
        print("Publsihed")

    def main(self):
        """
        Main Loop
        """
        while True:
            # Wait for a message
            message = self.redis.brpop(REDIS_QUEUE, timeout=0)  # Blocks forever
            if message:
                self.process_message(message)
            else:
                print("Timeout reached, no message")


if __name__ == "__main__":
    a = BackendLink()
    a.main()
