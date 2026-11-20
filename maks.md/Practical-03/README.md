# Practical 3 — Three-Broker Kafka — Producer and Consumer

Based on the uploaded **BD Practical Journal**. The source text below is kept for reference; the separate code files were extracted from that journal.

## Files

- `producer.py`
- `consumer.py`

## Step-by-step execution (Windows PowerShell)

1. Install/start Docker Desktop and open VS Code.
2. Set up a three-broker `docker-compose.yml` with exposed ports 29092, 39092 and 49092 (the attached journal describes the deployment but does not provide its Compose YAML text).
3. Run `docker compose up -d` and confirm with `docker compose ps`.
4. Install: `python -m pip install kafka-python`.
5. Open Terminal 1: `python consumer.py`.
6. Open Terminal 2: `python producer.py`.
7. Observe messages and stop the consumer with Ctrl+C.

## Expected result

Ten produced student messages and corresponding received messages, including partition and offset.

## Important note

The journal references but does not include the full three-broker docker-compose.yml source. It must be provided/configured separately.

## Original journal text (reference)

This section preserves the text extracted from the uploaded document. Screenshots/figures are not embedded here.

```text
Practical 3

Q.1 Set up a 3-broker Apache Kafka cluster using Docker Compose and
implement a Python-based Kafka Producer and Consumer to send and receive
student event messages through a Kafka topic.

STEP 1 Check Docker / installation of docker for windowsStep 1

Download Docker Desktop for Windows.
https://docs.docker.com/desktop/setup/install/windows-install/




1. Download Docker Desktop for Windows.
2. Run the downloaded installer.
3. During installation, keep the WSL 2 option selected if it is offered.
4. Complete the installation and restart Windows if requested.
STEP 2 Create project in VS Code

docker --version



docker ps




STEP 3 Start Kafka using Docker

   ● Make sure you are inside the folder containing docker-compose.yml.
   ● docker compose up -d




   ● Check whether the Kafka containers are running:
   ● docker ps




   ● CONTAINER ID: A unique, system-generated alphanumeric identifier for the
     container.
   ● IMAGE: The Docker image (and version tag) used to create the container.
   ● COMMAND: The initial command or script that was executed inside the
     container when it started.
   ● CREATED: A time
   ● stamp showing exactly how long ago the container was
     built.STATUS: The current state of the container (e.g., Up 2 hours, Exited (0) 5
     minutes ago).
   ● PORTS: Any network ports forwarded from your host computer into the
     container.
   ● NAMES: The human-readable name of the container. If you didnt assign one
     using --name, Docker generates a random, whimsical name.
**If old containers cause a name conflict:**

docker rm -f kafka1 kafka2 kafka3

Then:

docker compose up -d



STEP 5 Install Python Kafka library


In your VS Code terminal:

pip install kafka-python

Check that it installed:

pip show kafka-python

You should see information about:

Name: kafka-python


STEP 6 Create Python Producer
Producer.py:
from kafka import KafkaProducer
import json
import time


producer = KafkaProducer(
     bootstrap_servers=[
          "localhost:29092",
          "localhost:39092",
          "localhost:49092"
     ],
     value_serializer=lambda v: json.dumps(v).encode("utf-8")
)
for i in range(10):
    message = {
         "student_id": i + 1,
         "name": f"Student-{i + 1}",
         "course": "Data Science",
         "message": f"Hello from student {i + 1}"
    }


    producer.send("student-events", value=message)
    print("Produced:", message)
    time.sleep(1)


producer.flush()
producer.close()



STEP 7 Create Python Consumer
Consumer.py:
from kafka import KafkaConsumer
import json


consumer = KafkaConsumer(
    "student-events",
    bootstrap_servers=[
         "localhost:29092",
         "localhost:39092",
         "localhost:49092"
    ],
    auto_offset_reset="earliest",
    group_id="student-consumer-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)


print("Consumer started...")
print("Waiting for messages...\n")


for message in consumer:
    print(
         "Received:",
         message.value,
    "| Partition:",
    message.partition,
    "| Offset:",
    message.offset
)
```
