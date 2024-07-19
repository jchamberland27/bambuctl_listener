#!/usr/bin/python3
"""Fill dev DB with some data"""
from redis import Redis
import os
import json
import argparse

print("Connecting to Redis...")
parser = argparse.ArgumentParser(description="Fill dev DB with some data")
parser.add_argument("--redis_host", type=str, default="localhost", help="Redis host")
parser.add_argument("--redis_port", type=int, default=6379, help="Redis port")
args = parser.parse_args()

redis_host = args.redis_host
redis_port = args.redis_port
db = Redis(host=redis_host, port=redis_port, decode_responses=True)

print("Loading printers JSON...")
with open("printers.json") as f:
    printers = json.load(f)

for printer in printers:
    print(f"Adding printer {printers[printer]['id']} to DB")
    db.lpush("printer_ids", printers[printer]["id"])
    db.hmset(printers[printer]["id"], printers[printer])

print("Done!")
