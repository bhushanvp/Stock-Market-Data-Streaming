# Realtime Stock Market Data Warehousing and Visualization

## Project Structure

The project is organized into two main directories: `client` and `server`, each serving distinct purposes and containing specific files related to their functionalities.

* /Project
    - /client
        - /producer
            + \___init\___.py
            + producer.py
            + requirements.txt
        - /consumer
            + \___init\___.py
            + consumer.py
            + requirements.txt
    - /server
        - /data
            - /nse
                + nifty.csv
                + banknifty.csv
                + Other files ....
            - /bse
                + sensex.csv
                + Other files ....
        - index.js
        - package.json
        - package-lock.json
    - StockMarketData1.twb
    - README.md

<hr>

## Project Workflow

1. Server streams real-time stock market data.
2. Producer fetches and publishes data to Kafka.
3. Consumer subscribes, processes, and stores data in MongoDB.
4. Tableau connects to MongoDB in real-time to visualize the data.

<hr>

## Server

The Server consists of the following files:

- `index.js`: This is the main server script responsible for handling HTTP requests and serving data.
- `data/`: This directory contains CSV files with stock market data, organized by stock exchange and symbol.

### Dependencies

- `express`: To set up HTTP endpoints and handling requests.
- `fs`: Built-in Node.js module for working with the file system, used to read CSV files.
- `csv-parser`: A Node.js library for parsing CSV data, used to transform CSV data into JSON format.

### Setup

To setup the server, run the following command.

```bash
npm i
```

### Server Workflow

1. The server initializes an Express.js application and listens on a specified port (default: 3000).

2. It defines a single route (`/data/:stock_exchange/:symbol`) for handling HTTP GET requests. The route accepts two parameters: `stock_exchange` and `symbol`, which are used to determine the CSV file to read.

3. Inside the route handler, the server constructs the path to the CSV file based on the provided `stock_exchange` and `symbol`.

4. It sets the response header to indicate that JSON data will be sent in the response.

5. The server initializes an empty array `data` to store the JSON-converted CSV rows.

6. It defines a function `getCurrentTimeISO` to get the current time in ISO format.

7. The server reads the CSV file using `fs.createReadStream` and pipes it through `csv-parser` to parse the CSV data.

8. As each row is parsed, it is pushed into the `data` array, and the `timestamp` field is added to each row with the current time in ISO format.

9. The server sends JSON data for each row in the response, adding a 2-second delay between each row using `await new Promise((resolve) => setTimeout(resolve, 2000));`.

10. After all rows have been sent, the response is ended.

### Running the Server

To run the server, execute the `index.js` script. It will start the server on port 3000 by default.

```bash
node index.js
```
<hr>

## Client

The `client` directory is responsible for interacting with and processing financial market data. It is further divided into two subdirectories: `producer` and `consumer`.

### Consumer

The Consumer consists of the following files:

- `consumer.py`: This is the main consumer script responsible for consuming data from Kafka and inserting it into MongoDB.
- Other files: The project has other files like \___init\___.py, requirements.txt

#### Dependencies

- `confluent_kafka`: This library is used to interact with Kafka and consume messages from the Kafka topic.
- `pymongo`: It provides Pythonic access to MongoDB and is used to insert data into the database.
- `datetime`: Used for working with date and time information.
- `json`: Required for parsing JSON data received from Kafka messages.
- `pytz`: Used for handling time zones.

#### Setup
**_NOTE:_** : Make sure you are in the correct directory (client/)

```bash
pip install -r requirements.txt
```

#### Consumer Workflow

1. The consumer initializes by creating a Kafka consumer instance and a connection to the MongoDB database.

2. It subscribes to the Kafka topic "stock-market-data" using the `self._consumer.subscribe()` method.

3. The consumer enters a continuous polling loop, waiting for incoming messages.

4. When a message is received, it checks for errors. If there are no errors, it processes the message using the `_process_message` method.

5. Inside `_process_message`, the key and value of the Kafka message are extracted. The value is expected to be in JSON format.

6. The timestamp from the message is converted to a `datetime` object with UTC timezone information.

7. The consumer then attempts to insert the received data (timestamp, open, high, low, close) into the MongoDB collection "nifty50."

8. If the insertion is successful, it prints a confirmation message. Otherwise, it logs an insertion failure message.

9. The process continues until the consumer is interrupted (e.g., by a keyboard interrupt).

#### Configuration

- Kafka Broker: The consumer is configured to connect to a Kafka broker running locally on "localhost:9092."
- Consumer Group: It belongs to the consumer group "console-consumer-81883."
- Offset Reset: It starts consuming messages from the earliest available offset.

#### Running the Consumer

To run the consumer, execute the `consumer.py` script. It will start consuming messages from the Kafka topic and insert them into the MongoDB database.

**_NOTE:_** : Make sure you are in the correct directory (client/)

```bash
python ./consumer/consumer.py
```

### Producer

The project consists of the following files:

- `producer.py`: This is the main producer script responsible for fetching data and publishing it to Kafka.
- Other files: The project also has other files like node_modules.json, etc.

#### Dependencies

- `confluent_kafka`: This library is used to interact with Kafka and produce messages to the Kafka topic.
- `requests`: Used for making HTTP requests to the external data source.

#### Setup
**_NOTE:_** : Make sure you are in the correct directory (client/)

```bash
pip install -r requirements.txt
```

#### Producer Workflow

1. The producer initializes by creating a Kafka producer instance.

2. It defines a callback function `_producer_callback` to handle delivery reports for produced messages. If an error occurs during message delivery, it is printed to the console.

3. The `produce_data` method is responsible for fetching stock market data from an external source using the `requests` library. In this case, it fetches data from 'http://localhost:3000/data/nse/nifty'.

4. If the HTTP request to the data source is successful (HTTP status code 200), the producer iterates over the response content in chunks.

5. Each chunk of data is decoded from bytes to a UTF-8 string.

6. The producer publishes the data to the Kafka topic "stock-market-data" with the key "nifty50." This data is sent as the message value.

7. The `_producer_callback` function handles delivery reports for each message, printing any errors encountered during message delivery.

8. Any exceptions that occur during the data fetching or publishing process are caught and logged.

9. The producer continues to fetch and publish data at regular intervals defined by `_SLEEP_INTERVAL`.

10. The process can be terminated by interrupting the script (e.g., with a keyboard interrupt).

#### Configuration

- Kafka Broker: The producer is configured to connect to a Kafka broker running locally on "localhost:9092."

#### Running the Producer

To run the producer, execute the `producer.py` script. It will continuously fetch stock market data and publish it to the Kafka topic.

**_NOTE:_** : Make sure you are in the correct directory (client/)

```bash
python ./producer/producer.py
```
<hr>

## Tableau Visualization

The Tableau dashboard is connected to the MongoDB using ODBC drivers. It fetches real-time data and visualizes in the form of candle-sticks.

<hr>