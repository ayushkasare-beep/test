# Practical 10: Kafka -> ClickHouse (Grafana visualization configured separately).
# Requires the journal's Kafka, ClickHouse and Grafana Docker Compose environment.
# Run inside its Docker network; `kafka` and `clickhouse` are container hostnames.
# Requires: pip install kafka-python clickhouse-connect
# python P10_dashboard.py consumer   (terminal 1)
# python P10_dashboard.py producer   (terminal 2)
import sys, json, random
from datetime import datetime, timezone
from kafka import KafkaProducer, KafkaConsumer

mode = sys.argv[1] if len(sys.argv) > 1 else ""
if mode == "producer":
    p = KafkaProducer(bootstrap_servers="kafka:9092",
                      value_serializer=lambda x: json.dumps(x).encode())
    for i in range(5):
        item = {"event_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "city": random.choice(["Mumbai","Pune"]),
                "pm25": round(random.uniform(10,180),2),
                "pm10": 80.0, "temperature": 30.0}
        p.send("air_quality", item)
        print("Sent:", item)
    p.flush(); p.close()
elif mode == "consumer":
    import clickhouse_connect
    db = clickhouse_connect.get_client(host="clickhouse", port=8123,
                                       username="default", password="prac123")
    db.command("""CREATE TABLE IF NOT EXISTS default.air_quality (
        event_time DateTime, city String, pm25 Float64, pm10 Float64,
        temperature Float64) ENGINE=MergeTree ORDER BY (city,event_time)""")
    c = KafkaConsumer("air_quality", bootstrap_servers="kafka:9092",
                      auto_offset_reset="earliest",
                      value_deserializer=lambda x: json.loads(x.decode()))
    for i, msg in enumerate(c):
        r = msg.value
        dt = datetime.strptime(r["event_time"], "%Y-%m-%d %H:%M:%S")
        db.insert("default.air_quality", [[dt,r["city"],r["pm25"],r["pm10"],r["temperature"]]],
                  column_names=["event_time","city","pm25","pm10","temperature"])
        print("Inserted:", r)
        if i == 4: break
    c.close(); db.close()
else:
    print("Use: python P10_dashboard.py consumer  OR  python P10_dashboard.py producer")
# Grafana: ClickHouse data source -> SQL SELECT event_time AS time, avg(pm25)
# FROM default.air_quality GROUP BY time ORDER BY time (time-series panel).
