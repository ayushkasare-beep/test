# Practical 1: create skewed data and reduce skew using salting.
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, rand, sum as total
import time

spark = (SparkSession.builder.master("local[4]").appName("SkewDemo")
         .config("spark.sql.shuffle.partitions", "8").getOrCreate())
df = spark.range(100000)
df = df.withColumn("key", when(col("id") < 90000, 0).otherwise(col("id") % 99 + 1))
print("Before salting (key 0 dominates):")
df.groupBy("key").count().orderBy(col("count").desc()).show(5)
# Split a hot key into eight salted groups, then combine their counts.
df = df.withColumn("salt", (rand() * 8).cast("int"))
part = df.groupBy("key", "salt").count()
result = part.groupBy("key").agg(total("count").alias("count"))
print("After salting (same totals):")
result.orderBy(col("count").desc()).show(5)
print("Spark UI: http://localhost:4040")
time.sleep(120)  # Inspect Jobs / Stages while the application is running.
spark.stop()
