#!/usr/bin/python3
"""Fill dev DB with some data"""
from redis import Redis
import os
import json
import argparse

print("Connecting to Redis...")
parser = argparse.ArgumentParser(description="Fill dev DB with some data")
parser.add_argument("--redis_host", type=str, default="192.168.1.86", help="Redis host")
parser.add_argument("--redis_port", type=int, default=6381, help="Redis port")
parser.add_argument("-v", "--view", action="store_true", help="View the data in the DB")
args = parser.parse_args()


redis_host = args.redis_host
redis_port = args.redis_port
db = Redis(host=redis_host, port=redis_port, decode_responses=True)

if args.view:
    print("Viewing data in the DB...")
    keys = db.keys()
    for key in keys:
        if key == "printer_ids":
            print(f"{key}")
        else:
            print(f"{key}: {db.hgetall(key)}")
    exit()

print("Loading printers JSON...")
with open("printers.json") as f:
    printers = json.load(f)

for printer in printers:
    print(f"Adding printer {printers[printer]['id']} to DB")
    db.lpush("printer_ids", printers[printer]["id"])
    db.hmset(printers[printer]["id"], printers[printer])


print("Done!")
