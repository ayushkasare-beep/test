# Practical 1 — Spark Optimization — Data Skew

Based on the uploaded **BD Practical Journal**. The source text below is kept for reference; the separate code files were extracted from that journal.

## Files

- `skew.py`

## Step-by-step execution (Windows PowerShell)

1. Open VS Code and create/open this folder.
2. Install PySpark if necessary: `python -m pip install pyspark`.
3. Run: `python skew.py`.
4. During its 120-second pause, open `http://localhost:4040`.
5. Inspect **Jobs** and **Stages** to understand grouping and shuffle activity.

## Expected result

A large count for key 0 and a Spark UI showing completed jobs.

## Important note

The journal code generates skew and performs GROUP BY; it does not implement the salting fix mentioned in the aim.

## Original journal text (reference)

This section preserves the text extracted from the uploaded document. Screenshots/figures are not embedded here.

```text
Practical 1

Q.1 Spark Optimization: Implement a Spark job and use the Spark UI to identify
and fix data skew and "shuffle" bottlenecks.

skew.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit


#Create a spark session
spark=(
     SparkSession.builder.appName("SparkSkewPractical")
     .master("local[4]")
     .config("spark.sql.shuffle.partitions","8")
     .getOrCreate()
)


# Reduce unnecessary messages in the terminal
spark.sparkContext.setLogLevel("WARN")
print("================================")
print("Spark application started!")
print("================================")


# Create 5 million records
number_of_records=5_000_000
df=spark.range(number_of_records)
print("Dataset created!")
# Create intentionally skewed data
# About 90% of the records get key = 0
skewed_df=df.withColumn(
    "key",
    when(
        col("id")<number_of_records * 0.90,
        lit(0)
    ).otherwise(
        (col("id")%999)+1
    )
)
print("Skewed dataset created!")


# Show the distribution of keys
print("\nKey Distributed:")
skewed_df.groupBy("key").count().orderBy(
    col("count").desc()
).show(10)


# Perform GROUP BY
# GROUP BY causes a shuffle
print("\nStarting GROUP BY...")


result=(
    skewed_df
    .groupBy("key")
    .count()
)


# collect() forces Spark to execute the operation
result.collect()


print("\nGROUP BY completed!")
print("====================================")
print("Open Spark UI:")
print("http://localhost:4040")
print("====================================")


# Keep Spark running so we can inspect Spark UI
import time
time.sleep(120)
spark.stop()



Output:
1st Output:




2nd Output:
```
