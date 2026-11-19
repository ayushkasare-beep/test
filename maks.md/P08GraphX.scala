// Practical 8: GraphX PageRank (data embedded, so no CSV files needed).
// Needs Spark GraphX + Scala 2.12 dependencies in build.sbt from your journal.
import org.apache.spark.sql.SparkSession
import org.apache.spark.graphx._

object P08GraphX {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().master("local[*]").appName("GraphX").getOrCreate()
    val sc = spark.sparkContext
    sc.setLogLevel("ERROR")
    val users = sc.parallelize(Seq(1L -> "Alice", 2L -> "Bob", 3L -> "Charlie",
      4L -> "David", 5L -> "Emma", 6L -> "Frank"))
    val edges = sc.parallelize(Seq(Edge(1L,2L,1), Edge(1L,3L,1),
      Edge(2L,3L,1), Edge(3L,1L,1), Edge(4L,2L,1),
      Edge(5L,4L,1), Edge(6L,2L,1)))
    val ranks = Graph(users, edges).pageRank(0.0001).vertices
    val result = users.join(ranks).map { case (_, (name, rank)) =>
      (name, rank)
    }.sortBy(_._2, ascending = false)
    result.collect().foreach(println)
    println("Most influential: " + result.first())
    spark.stop()
  }
}
