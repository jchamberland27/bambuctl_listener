from dotenv import load_dotenv
import time
from threading import Thread
from typing import Dict
import os
from redis import Redis
import bambulab_common.bambu_mqtt as bambu_mqtt
from bambulab_common.printer import Printer


def build_threadpool(printers, db: Redis) -> Dict[str, Thread]:
    threads: Dict[str, Thread] = {}
    for printer_id in printers:
        printer = Printer(printer_id, db)
        client = bambu_mqtt.create_client(printer)
        printer.set_client(client)
        threads[printer_id] = Thread(
            target=bambu_mqtt.client_thread_func,
            args=(printer, bambu_mqtt.mqttMode.LISTENER, printer.client),
        )
    return threads


load_dotenv()

print("Setting up Redis and retrieving printers...")
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

db = Redis(host=redis_host, port=redis_port, decode_responses=True)
printers = db.lrange("printer_ids", 0, -1)  # Await the printers variable

print("Building threadpool...")
printer_threads = build_threadpool(printers, db)

print("Starting threads...")
for printer_id, thread in printer_threads.items():
    thread.start()

print("And we're off!")
running: bool = True
while running:
    time.sleep(5)
