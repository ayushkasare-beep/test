# Practical 5: socket sender + Spark word count in ONE file.
# First terminal: python P05_stream.py sender
# Second terminal: python P05_stream.py spark
import sys
mode = sys.argv[1] if len(sys.argv) > 1 else ""

if mode == "sender":
    import socket
    with socket.socket() as s:
        s.bind(("localhost", 9999))
        s.listen(1)
        print("Waiting for Spark...")
        c, _ = s.accept()
        with c:
            while True:
                msg = input("Enter text (exit to stop): ")
                if msg.lower() == "exit":
                    break
                c.sendall((msg + "\n").encode())
elif mode == "spark":
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import split, explode
    spark = SparkSession.builder.master("local[2]").appName("WordCount").getOrCreate()
    data = spark.readStream.format("socket").options(host="localhost", port=9999).load()
    words = data.select(explode(split("value", " ")).alias("word"))
    counts = words.groupBy("word").count()
    counts.writeStream.format("console").outputMode("complete").start().awaitTermination()
else:
    print("Use: python P05_stream.py sender  OR  python P05_stream.py spark")
