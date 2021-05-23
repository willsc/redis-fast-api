#!/usr/local/bin/python3


import redis
import sys

def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host="redis-18136.c1.us-east1-2.gce.cloud.redislabs.com",
            port=18136,
            password="foobar",
            db=0,
            socket_timeout=5,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)



client = redis_connect()

print(client)


