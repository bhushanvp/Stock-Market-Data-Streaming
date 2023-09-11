import datetime
from confluent_kafka import Producer
import pandas as pd
import time
import json

class StockDataProducer:
    _TOPIC = "stock-market-data"
    _KEY = "nifty50"
    _CSV_FILE = "./data/NIFTY 50-10-09-2022-to-10-09-2023.csv"
    _SLEEP_INTERVAL = 2

    def __init__(self, config):
        self._df = pd.read_csv(self._CSV_FILE)
        self._producer = Producer(config)

    def _producer_callback(self, err, msg):
        if err:
            print(err)
        else:
            print(msg)

    def produce_data(self):
        try:
            for i in self._df.values:
                data = {
                    "open": i[1],
                    "high": i[2],
                    "low": i[3],
                    "close": i[4],
                    "timestamp": f"{datetime.datetime.utcnow()}",
                }

                print(data)

                self._producer.produce(
                    topic=self._TOPIC,
                    key=self._KEY,
                    value=json.dumps(data),
                    callback=self._producer_callback
                )

                time.sleep(self._SLEEP_INTERVAL)

            self._producer.flush()

        except Exception as e:
            print(f"Error producing data: {e}")


def main():
    config = {
        "bootstrap.servers": "localhost:9092"
    }

    stock_producer = StockDataProducer(config)
    stock_producer.produce_data()

if __name__ == "__main__":
    main()
