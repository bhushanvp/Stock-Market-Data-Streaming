from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
import datetime
import json
import pytz

class StockDataConsumer:
    _KAFKA_TOPIC = "stock-market-data"
    _MONGODB_HOST = "localhost"
    _MONGODB_PORT = 27017
    _MONGODB_DB = "stock-market-data"
    _MONGODB_COLLECTION = "nifty50"

    def __init__(self, config):
        self._consumer = Consumer(config)
        self._client = MongoClient(self._MONGODB_HOST, self._MONGODB_PORT)
        self._db = self._client.get_database(self._MONGODB_DB)
        self._nifty50 = self._db.get_collection(self._MONGODB_COLLECTION)

    def consume_messages(self):
        self._consumer.subscribe([self._KAFKA_TOPIC])

        try:
            while True:
                msg = self._consumer.poll(1.0)

                if msg is None:
                    print("Polling....")
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print("Reached end of partition")
                    else:
                        print(msg.error())
                else:
                    try:
                        self._process_message(msg)
                    except Exception as e:
                        print(f"Error processing message: {e}")

        except KeyboardInterrupt:
            self._consumer.close()
            print("Shutting down...")

    def _process_message(self, msg):
        key = msg.key().decode('utf-8')
        value = json.loads(msg.value().decode('utf-8'), parse_float=float)

        timestamp_str = value.get("timestamp")
        date_string_with_utc = timestamp_str[:-1] + '+00:00'
        timestamp = datetime.datetime.fromisoformat(date_string_with_utc).replace(tzinfo=pytz.utc)

        try:
            insert_status = self._nifty50.insert_one({
                "timestamp": timestamp,
                "open": float(value.get("Open")),
                "high": float(value.get("High")),
                "low": float(value.get("Low")),
                "close": float(value.get("Close"))
            })

            if insert_status.acknowledged:
                print(f"{key} : {value} -> Inserted")
                pass
            else:
                print(f"{key} : {value} -> Insertion failed")

        except Exception as e:
            print(f"Error processing message: {e}")


def main():
    config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "console-consumer-81883",
        "auto.offset.reset": "earliest"
    }
    stock_consumer = StockDataConsumer(config)
    stock_consumer.consume_messages()

if __name__ == "__main__":
    main()
