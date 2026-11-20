# Practical 10 — Kafka + ClickHouse + Grafana — Real-time Dashboard

Based on the uploaded **BD Practical Journal**. The source text below is kept for reference; the separate code files were extracted from that journal.

## Files

- `consumer.py`
- `producer.py`
- `docker-compose.yml`
- `requirements.txt`
- `Dockerfile`

## Step-by-step execution (Windows PowerShell)

1. Install/open Docker Desktop and enter this folder.
2. Run `docker compose up --build -d`.
3. Check with `docker compose ps` and `docker compose logs --tail=20 producer`.
4. Check `docker compose logs --tail=30 consumer`.
5. Read ClickHouse data: `docker compose exec clickhouse clickhouse-client --password prac123 --query "SELECT count() FROM default.air_quality"`.
6. Open `http://localhost:3000`, configure a ClickHouse data source, and create a time-series panel using the SQL in the source reference below.

## Expected result

Producer prints Sent, consumer prints Inserted, ClickHouse has records, Grafana charts display time series.

## Important note

The journal has inconsistent ClickHouse credentials in some explanatory steps; its Compose uses default user with password prac123. Use that password rather than admin/admin123.

## Original journal text (reference)

This section preserves the text extracted from the uploaded document. Screenshots/figures are not embedded here.

```text
Practical 10

Q.1 Real-time Dashboard: Integrate a Kafka stream with an OLAP engine
(ClickHouse) and visualize the data on a Grafana Dashboard.

   1. Create a project folder named prac and add docker-compose.yml,
      Dockerfile, requirements.txt, producer.py, and consumer.py.

consumer.py

import json
import time
from datetime import datetime


import clickhouse_connect
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable



def connect_clickhouse():
    while True:
        try:
              client = clickhouse_connect.get_client(
                  host="clickhouse",
                  port=8123,
                  username="default",
                  password="prac123"
              )


              client.command("""
                  CREATE TABLE IF NOT EXISTS default.air_quality
                  (
                      event_time DateTime,
                      city String,
                         pm25 Float64,
                         pm10 Float64,
                         temperature Float64
                     )
                     ENGINE = MergeTree
                     ORDER BY (city, event_time)
              """)


              print("Connected to ClickHouse.", flush=True)
              return client


       except Exception as error:
              print("Waiting for ClickHouse:", error, flush=True)
              time.sleep(3)



def connect_kafka():
   while True:
       try:
              consumer = KafkaConsumer(
                  "air_quality",
                     bootstrap_servers=["kafka:9092"],
                     auto_offset_reset="earliest",
                     enable_auto_commit=True,
                     group_id="air-quality-group",
                     value_deserializer=lambda value: json.loads(
                         value.decode("utf-8")
                     )
              )


              print("Connected to Kafka topic.", flush=True)
              return consumer


       except NoBrokersAvailable:
              print("Waiting for Kafka...", flush=True)
              time.sleep(3)



def main():
   client = connect_clickhouse()
consumer = connect_kafka()


print("Kafka Consumer Started", flush=True)


try:
    for message in consumer:
        reading = message.value


        try:
            # Convert timestamp string into a Python datetime object
               reading["event_time"] = datetime.strptime(
                   reading["event_time"],
                   "%Y-%m-%d %H:%M:%S"
               )


               client.insert(
                   "default.air_quality",
                   [[
                         reading["event_time"],
                         reading["city"],
                         reading["pm25"],
                         reading["pm10"],
                         reading["temperature"]
                   ]],
                   column_names=[
                         "event_time",
                         "city",
                         "pm25",
                         "pm10",
                         "temperature"
                   ]
               )
               print("Inserted:", reading, flush=True)


        except Exception as error:
               print("Insertion error:", error, flush=True)


except KeyboardInterrupt:
   print("Consumer stopped.", flush=True)
    finally:
        consumer.close()
        client.close()
if __name__ == "__main__":
    main()


producer.py

import json
import random
import time
from datetime import datetime, timezone


from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


TOPIC = "air_quality"



def connect_producer():
    while True:
        try:
              producer = KafkaProducer(
                  bootstrap_servers=["kafka:9092"],
                  value_serializer=lambda value:
json.dumps(value).encode("utf-8")
              )


              print("Connected to Kafka.", flush=True)
              return producer


        except NoBrokersAvailable:
              print("Waiting for Kafka...", flush=True)
              time.sleep(3)



def main():
    producer = connect_producer()
    cities = ["Mumbai", "Pune", "Nashik", "Nagpur"]
   print("Air Quality Producer Started", flush=True)


    try:
        while True:
             reading = {
                 "event_time": datetime.now(timezone.utc).strftime(
                        "%Y-%m-%d %H:%M:%S"
                   ),
                 "city": random.choice(cities),
                 "pm25": round(random.uniform(10, 180), 2),
                 "pm10": round(random.uniform(20, 250), 2),
                 "temperature": round(random.uniform(24, 38), 2)
             }


             producer.send(TOPIC, value=reading).get(timeout=10)


             print("Sent:", reading, flush=True)


             time.sleep(2)


    except KeyboardInterrupt:
       print("Producer stopped.", flush=True)


    finally:
       producer.close()



if __name__ == "__main__":
   main()




docker-compose.yml

services:
  kafka:
    image: apache/kafka:3.9.1
    ports:
     - "9092:9092"
    environment:
     KAFKA_NODE_ID: 1
     KAFKA_PROCESS_ROLES: broker,controller
     KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093
     KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
     KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
     KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
     KAFKA_LISTENER_SECURITY_PROTOCOL_MAP:
CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
     KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
     KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
     KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
     KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
     KAFKA_NUM_PARTITIONS: 1



 clickhouse:
   image: clickhouse/clickhouse-server:latest
   ports:
     - "8123:8123"
     - "9000:9000"
   environment:
     CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: 1
     CLICKHOUSE_PASSWORD: prac123



 grafana:
   image: grafana/grafana:latest
   ports:
     - "3000:3000"
   environment:
     GF_INSTALL_PLUGINS: grafana-clickhouse-datasource
   depends_on:
     - clickhouse


 producer:
   build: .
   command: python -u producer.py
   depends_on:
     - kafka
  consumer:
    build: .
    command: python -u consumer.py
    depends_on:
      - kafka
      - clickhouse



requirements.txt

kafka-python==2.0.2
clickhouse-connect



Dockerfile

FROM python:3.11-slim


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY producer.py .
COPY consumer.py .


CMD ["python", "-u", "producer.py"]




Now Run These Commands in terminal:
docker compose down
docker compose up --build -d
docker compose ps
docker compose logs --tail 10 consumer
docker compose logs --tail 20 producer
docker compose exec clickhouse clickhouse-client --user admin --password admin123
--query "SELECT * FROM default.air_quality ORDER BY event_time DESC LIMIT 10"

Grafana Usage Steps
Now after this go to http://localhost:3000
Username and password both as admin and then it will say you change the password
so keep it as admin 123 and then :

   1. Go to Connections → Data sources → Add data source.
   2. Search for ClickHouse and select it.
   3. Fill in these fields:
           ○ Server address: clickhouse
           ○ Server port: 9000 and Protocol: Native (or port 8123 with HTTP, either
               works)
           ○ Username: admin
           ○ Password: admin123
           ○ Default database: default
   4. Click Save & test. You should see a green “Data source is working” message.

Go to Dashboards → New → New dashboard → Add visualization, pick the
ClickHouse data source, and switch the query editor to SQL Editor.

Panel 1: PM2.5 over time by city (Time series)

Sql:

SELECT
 $__timeInterval(event_time) AS time,
 city,
 avg(pm25) AS pm25
FROM default.air_quality
WHERE $__timeFilter(event_time)
GROUP BY time, city
ORDER BY time

Set the format to Time series.
   2. Open Explore and execute an SQL query to view air-quality readings.
      1. Display recent air-quality readings
      SELECT
         city,
         event_time,
         pm25,
         pm10,
         temperature
      FROM default.air_quality
      ORDER BY event_time DESC
      LIMIT 20;

   3. Create a dashboard and add a Time series visualization for PM2.5 levels.
       2. Display PM2.5 levels over time (Time Series graph)
       SELECT
          event_time AS time,
          avg(pm25) AS pm25
       FROM default.air_quality
       WHERE event_time >= now() - INTERVAL 15 MINUTE
       GROUP BY time
       ORDER BY time;
Set of commands to run on terminal:

docker compose down
docker compose up --build -d




docker compose logs --tail=20 producer




docker compose logs --tail=30 consumer




docker compose exec clickhouse clickhouse-client --password prac123 --query
"SELECT count() FROM default.air_quality"

docker compose exec clickhouse clickhouse-client --password prac123 --query
"SELECT * FROM default.air_quality LIMIT 10"
```
