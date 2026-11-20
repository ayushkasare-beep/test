# Practical 5 — Spark Structured Streaming — Socket Word Count

Based on the uploaded **BD Practical Journal**. The source text below is kept for reference; the separate code files were extracted from that journal.

## Files

- `socket_sender.py`
- `word_count_stream.py`

## Step-by-step execution (Windows PowerShell)

1. Open VS Code and install PySpark: `python -m pip install pyspark`.
2. In Terminal 1 run `python socket_sender.py` and leave it waiting.
3. In Terminal 2 run `python word_count_stream.py`.
4. Go back to Terminal 1 and type `hello spark hello python hello spark`.
5. Observe word-frequency counts in Terminal 2. Type `exit` in Terminal 1 when finished.

## Expected result

hello = 3, spark = 2, python = 1 in the streaming output.

## Important note

The files and socket port 9999 follow the journal.

## Original journal text (reference)

This section preserves the text extracted from the uploaded document. Screenshots/figures are not embedded here.

```text
Practical 5

Q.1 Structured Streaming: Build a Spark Structured Streaming app to count word
frequencies from a live socket stream.

Commands:-
  ● python --version
  ● java --version
  ● pip install pyspark
  ● pyspark --version
Above screenshot shows that PySpark is installed successfully, but the
pyspark command is not available in your Windows PATH.
So for this type the below command,
1) python -c "import pyspark; print(pyspark.__version__)"
2) To find where PySpark was installed type,
   python -m pip show pyspark
socket_sender.py
import socket


HOST = "localhost"
PORT = 9999


# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind socket to host and port
server_socket.bind((HOST, PORT))


# Listen for connection
server_socket.listen(1)


print("======================================")
print("Socket Server Started")
print("Waiting for Spark to connect...")
print("Host:", HOST)
print("Port:", PORT)
print("======================================")


# Accept connection from Spark
connection, address = server_socket.accept()


print("Spark connected!")
print("Start entering messages.")
print("Type 'exit' to stop.")
print("--------------------------------------")


while True:


    message = input("Enter message: ")


    # Stop the program
    if message.lower() == "exit":
        break


    # Send message to Spark
    connection.sendall((message + "\n").encode("utf-8"))
print("Closing connection...")


connection.close()
server_socket.close()


print("Socket server stopped.")



word_count_stream.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split


spark = SparkSession.builder \
    .master("local[2]") \
    .appName("WordCount") \
    .getOrCreate()


spark.sparkContext.setLogLevel("ERROR")


data = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()


words = data.select(
    explode(split(data.value, " ")).alias("word")
)


counts = words.groupBy("word").count()


query = counts.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()


query.awaitTermination()
Run both files in different terminals.
First run Python socket_sender.py
Then Open another terminal and run Python word_count_stream.py
Go back to the 1st terminal and enter text for word count:
        hello spark hello python hello spark
Check the 2nd terminal for Word Count Output.


Output:

1st trminal




2nd terminal
```
