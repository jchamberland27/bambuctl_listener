#!/usr/bin/python3
"""Fill dev DB with some data"""
from redis import Redis
import os
import json

print("Connecting to Redis...")
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
db = Redis(host=redis_host, port=redis_port, decode_responses=True)

print("Loading printers JSON...")
with open("printers.json") as f:
    printers = json.load(f)

for printer in printers:
    print(f"Adding printer {printers[printer]['id']} to DB")
    db.lpush("printer_ids", printers[printer]["id"])
    db.hmset(printers[printer]["id"], printers[printer])

print("Done!")
