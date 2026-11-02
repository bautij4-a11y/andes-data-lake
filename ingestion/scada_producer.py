"""Publish simulated SCADA readings (JSON Lines) to a Kafka topic.

Events are sent as-is (duplicates and bad values included). Cleaning happens downstream.
The sensor_id is used as the message key, so each sensor keeps its order within a partition.
"""
import argparse
import json
import time
from pathlib import Path

from kafka import KafkaProducer

TOPIC = "scada.readings.raw"
DEFAULT_INPUT = Path(__file__).resolve().parents[1] / "sources" / "scada" / "data" / "readings.jsonl"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--bootstrap", default="localhost:9092")
    parser.add_argument("--rate", type=float, default=0,
                        help="events per second (0 = as fast as possible)")
    args = parser.parse_args()

    producer = KafkaProducer(
        bootstrap_servers=args.bootstrap,
        key_serializer=lambda k: k.encode("utf-8"),
        value_serializer=lambda v: v,
        acks="all",
        linger_ms=20,
    )

    sent = 0
    with open(args.input) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            event = json.loads(line)
            producer.send(TOPIC, key=event["sensor_id"], value=line.encode("utf-8"))
            sent += 1
            if args.rate > 0:
                time.sleep(1 / args.rate)
    producer.flush()
    print(f"Published {sent} events to topic '{TOPIC}'.")


if __name__ == "__main__":
    main()
