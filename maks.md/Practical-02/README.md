# Practical 2 — Delta Lake — Data Lakehouse

Based on the uploaded **BD Practical Journal**. The source text below is kept for reference; the separate code files were extracted from that journal.

## Files

- `new.py`

## Step-by-step execution (Windows PowerShell)

1. Open VS Code and use a Python environment with Java.
2. Install: `python -m pip install pyspark delta-spark`.
3. Check: `python -m pip show pyspark` and `python -m pip show delta-spark`.
4. Run: `python new.py`.

## Expected result

Spark starts and a table of six students with marks is displayed.

## Important note

The provided journal code only creates and shows a DataFrame; although the aim mentions Delta Time Travel and ACID, those operations are absent from the supplied script.

## Original journal text (reference)

This section preserves the text extracted from the uploaded document. Screenshots/figures are not embedded here.

```text
Practical 2

Q.1 Data Lakehouse: Create a Delta Lake table and demonstrate "Time Travel"
and "ACID Transactions" on Spark.

1) C:\Users\Admin&gt;pip install pyspark delta-spark




2) Check with pip show pyspark




3) pip show delta-spark




Code: new.py
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


# Start Spark
builder = (
    SparkSession.builder
    .appName("DeltaLakeDemo")
    .master("local[*]")
    .config(
          "spark.sql.extensions",
          "io.delta.sql.DeltaSparkSessionExtension"
    )
    .config(
          "spark.sql.catalog.spark_catalog",
          "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )
)


spark = configure_spark_with_delta_pip(builder).getOrCreate()


print("Spark started successfully!")


# Create sample data
data = [
    (1, "Siddhant", 90),
    (2, "Shreya", 88),
    (3, "Shruti", 75),
    (4, "Chinmay", 90),
    (5, "Vishnu", 88),
    (6, "Nikita", 75)


]


df = spark.createDataFrame(
    data,
    ["id", "name", "marks"]
)


print("Student Data:")
df.show()


spark.stop()


Output:
```
