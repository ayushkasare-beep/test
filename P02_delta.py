# Practical 2: Delta Lake write, update and time travel.
# Requires: pip install pyspark delta-spark; compatible Java and Spark versions.
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip, DeltaTable
import tempfile

b = SparkSession.builder.master("local[2]").appName("DeltaDemo")
b = b.config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
b = b.config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark = configure_spark_with_delta_pip(b).getOrCreate()
path = tempfile.mkdtemp(prefix="delta_students_")  # Fresh table every run.
df = spark.createDataFrame([(1, "Amit", 90), (2, "Nikita", 75)], ["id", "name", "marks"])
df.write.format("delta").mode("overwrite").save(path)
table = DeltaTable.forPath(spark, path)
table.update("name = 'Nikita'", {"marks": "80"})
print("New data (Nikita=80):")
spark.read.format("delta").load(path).show()
print("Time travel, version 0 (Nikita=75):")
spark.read.format("delta").option("versionAsOf", 0).load(path).show()
table.history().select("version", "operation").show()
spark.stop()
