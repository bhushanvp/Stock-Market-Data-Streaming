import threading
from producer.producer import StockDataProducer
from consumer.consumer import StockDataConsumer

def main():
    producer_config = {
        "bootstrap.servers": "localhost:9092"
    }

    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "console-consumer-81883",
        "auto.offset.reset": "latest"
    }

    stock_producer = StockDataProducer(producer_config)
    stock_consumer = StockDataConsumer(consumer_config)

    try:
        producer_thread = threading.Thread(target=stock_producer.produce_data)
        consumer_thread = threading.Thread(target=stock_consumer.consume_messages)

        producer_thread.start()

        consumer_thread.start()

    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    main()
