# Practical 3: Producer and consumer in ONE file.
# Needs the journal's 3-broker Kafka cluster on ports 29092/39092/49092.
# Run in two terminals: python P03_kafka.py consumer / python P03_kafka.py producer
import sys, json
from kafka import KafkaProducer, KafkaConsumer

brokers = ["localhost:29092", "localhost:39092", "localhost:49092"]
topic = "student-events"
mode = sys.argv[1] if len(sys.argv) > 1 else ""
if mode == "producer":
    p = KafkaProducer(bootstrap_servers=brokers,
                      value_serializer=lambda x: json.dumps(x).encode())
    for i in range(3):
        msg = {"id": i + 1, "name": "Student"}
        p.send(topic, msg)
        print("Sent:", msg)
    p.flush()
    p.close()
elif mode == "consumer":
    c = KafkaConsumer(topic, bootstrap_servers=brokers,
                      auto_offset_reset="earliest",
                      value_deserializer=lambda x: json.loads(x.decode()))
    for i, msg in enumerate(c):
        print("Received:", msg.value)
        if i == 2:  # Stop after three received records.
            break
    c.close()
else:
    print("Use: python P03_kafka.py consumer  OR  python P03_kafka.py producer")
