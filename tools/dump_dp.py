#!/usr/bin/python3
import argparse
import os
from redis import Redis


def setup_args():
    parser = argparse.ArgumentParser(description="Dump printer info from Redis")
    parser.add_argument("--key", default="all", help="Redis host")
    return parser.parse_args()


def fetch_and_print_data(redis_db, key):
    data_type = redis_db.type(key)
    print(f"Key: {key} - Type: {data_type}")

    if data_type == "string":
        print(redis_db.get(key))
    elif data_type == "hash":
        print(redis_db.hgetall(key))
    elif data_type == "list":
        print(redis_db.lrange(key, 0, -1))
    elif data_type == "set":
        print(redis_db.smembers(key))
    elif data_type == "zset":
        print(redis_db.zrange(key, 0, -1, withscores=True))
    else:
        print("Unknown data type or empty key.")


args = setup_args()

print("Connecting to Redis...")
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
db = Redis(host=redis_host, port=redis_port, decode_responses=True)

if args.key == "all":
    keys = db.keys()
    for key in keys:  # type: ignore
        fetch_and_print_data(db, key)
else:
    fetch_and_print_data(db, args.key)
