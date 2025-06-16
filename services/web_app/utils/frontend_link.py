"""
This script is for the frontend link that is responsible for
connecting the to redis and communicating with the backend process
"""

import redis
import os
import time

REDIS_HOST = os.getenv("REDIS_HOST", "custom-redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_QUEUE = os.getenv("REDIS_QUEUE", "incoming_queue")
REDIS_DATA_COUNTER_KEY = os.getenv("REDIS_DATA_COUNTER_KEY", "data_counter_key")
REDIS_RESPONSE_CHANNEL = os.getenv("REDIS_RESPONSE_CHANNEL", "response_channel")


class FrontendLink:
    """
    Class to handle connection to the backend processing scripts
    """
    def __init__(self):
        print("Initializing the front end link")
        self.set_up_redis()

    def set_up_redis(self):
        print("Setting up Redis")
        self.redis = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, decode_responses=False
        )

        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(REDIS_RESPONSE_CHANNEL)

    def get_a_new_key(self):
        print("Getting a new key")
        ans = self.redis.get(REDIS_DATA_COUNTER_KEY)
        if ans:  # not None
            num = int(ans)
            if num == 20:
                num = 0
                self.redis.set(REDIS_DATA_COUNTER_KEY, 0)
            else:
                self.redis.incr(REDIS_DATA_COUNTER_KEY)

        else:  # was None
            self.redis.set(REDIS_DATA_COUNTER_KEY, 0)
            num = 0

        key = f"data:{num}"

        # Clear the key
        self.redis.delete(key)

        return key

    def publish_message(self, data):
        print("\nPublishing Message")

        # Get a key
        key = self.get_a_new_key()
        print(f"Got a new key: {key}")

        # Add the data to the key
        print("Adding the data to the key")
        self.redis.set(key, data)

        # Write the Key to the queue
        print("Writing the key to the queue")
        self.redis.lpush(REDIS_QUEUE, key)

        # Subscribe to the channel and wait for the key to come back
        print("Subscribed for responses")
        for message in self.pubsub.listen():
            if message["type"] == "message":
                print(f"Received message: {message['data']}")
                response_key = message["data"].decode()
                if key == response_key:
                    print("We have our response!")
                    break
                else:
                    print("Unrecognized key")
            else:
                print("Not a relevant message")

        # Read the data in from the key
        print("Reading in the data coming back from the backend")
        data = self.redis.get(key)
        assert data is not None

        # Clear the Key
        self.redis.delete(key)

        print("Completed the Communication with the backend")
        return data

    def main(self):
        while True:
            self.publish_message("test")
            time.sleep(1)


if __name__ == "__main__":
    a = FrontendLink()
    a.main()
