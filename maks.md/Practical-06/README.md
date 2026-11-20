# Practical 6 — Flink Fraud Detection — KeyedProcessFunction

Based on the uploaded **BD Practical Journal**. The source text below is kept for reference; the separate code files were extracted from that journal.

## Files

- `FraudDetectionJob.java`
- `pom.xml`

## Step-by-step execution (Windows PowerShell)

1. Install Java JDK 17 and Maven; verify with `java -version` and `mvn -version`.
2. Open this folder as a Maven project in VS Code; the journal uses `FraudDetectionJob.java` and `pom.xml`.
3. Run `mvn clean compile`.
4. Run `mvn clean package`.
5. Run `java -jar target\flink-practical-1.0-SNAPSHOT.jar` if the shade packaging succeeds.

## Expected result

FRAUD ALERT for two transactions of at least ₹10,000 within 60 seconds for the same customer.

## Important note

The journal's word-wrapped Java code may need formatting correction before compilation. See full source below; Maven dependencies are specified in pom.xml.

## Original journal text (reference)

This section preserves the text extracted from the uploaded document. Screenshots/figures are not embedded here.

```text
Practical 6

Q.1 Flink State Lab: Implement a Flink application that detects "Fraudulent
Transactions" (two large transactions within 1 minute) using
KeyedProcessFunction.




Step 1: Install Java JDK 17

Step 2: Install Apache Maven

Maven downloads the Flink libraries and builds your project.

   1. Open the official page: https://maven.apache.org/download.cgi
2. Download the Binary zip archive.




3. Extract it to a folder such as C:\Tools\apache-maven.

4. Add its bin folder to the Windows PATH environment variable. For
   example, C:\Tools\apache-maven\bin.

5. Close and reopen Command Prompt.

6. Check by using command

   mvn -version




   Step 3: Install VS Code/ open VS Cdoe and Java extensions

   After installation:
1. Open VS Code.

2. Click the Extensions icon on the left sidebar.

3. Search for Extension Pack for Java.

4. Install the extension pack published by Microsoft.

   It includes Java language support, debugging, project management, and
   Maven integration.
FraudDetectionJob.java
import org.apache.flink.api.common.state.ValueState;

import org.apache.flink.api.common.state.ValueStateDescriptor;

import org.apache.flink.api.common.typeinfo.Types;

import org.apache.flink.streaming.api.datastream.DataStream;

import
org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import org.apache.flink.streaming.api.functions.KeyedProcessFunction;

import org.apache.flink.util.Collector;



import java.io.Serializable;

import java.time.Instant;



public class FraudDetectionJob {



    public static class Transaction implements Serializable {

         public String customerId;

         public double amount;

         public long timestamp;



         public Transaction() {}



         public Transaction(String customerId, double amount, long
timestamp) {

            this.customerId = customerId;

            this.amount = amount;

            this.timestamp = timestamp;
    }

}



public static class FraudAlert implements Serializable {

    public String customerId;

    public double previousAmount;

    public double currentAmount;

    public long gapMs;



    public FraudAlert() {}



    public FraudAlert(String customerId, double previousAmount,

                      double currentAmount, long gapMs) {

        this.customerId = customerId;

        this.previousAmount = previousAmount;

        this.currentAmount = currentAmount;

        this.gapMs = gapMs;

    }



    @Override

    public String toString() {

        return "FRAUD ALERT: Customer=" + customerId

                + ", Previous=₹" + previousAmount

                + ", Current=₹" + currentAmount

                + ", Gap=" + gapMs / 1000 + " seconds";

    }

}
    public static class FraudDetector

           extends KeyedProcessFunction<String, Transaction, FraudAlert>
{



       private transient ValueState<Transaction> previousTransaction;



       @Override

       public void open(

               org.apache.flink.configuration.Configuration parameters) {



           ValueStateDescriptor<Transaction> descriptor =

                   new ValueStateDescriptor<>(

                            "previous-large-transaction",

                            Types.POJO(Transaction.class));



            previousTransaction =
getRuntimeContext().getState(descriptor);

       }



       @Override

       public void processElement(

               Transaction tx,

               Context ctx,

               Collector<FraudAlert> out) throws Exception {



           // Only consider transactions of ₹10,000 or more.

           if (tx.amount < 10000) {
            return;

        }



        Transaction previous = previousTransaction.value();



        if (previous != null) {

            long gap = tx.timestamp - previous.timestamp;



            if (gap >= 0 && gap <= 60000) {

                out.collect(new FraudAlert(

                        tx.customerId,

                        previous.amount,

                        tx.amount,

                        gap));

            }

        }



        // Update the state for this customer.

        previousTransaction.update(tx);

    }

}



public static void main(String[] args) throws Exception {



    StreamExecutionEnvironment env =

            StreamExecutionEnvironment.getExecutionEnvironment();
        long base = Instant.parse("2026-10-19T10:00:00Z")

                .toEpochMilli();



        DataStream<Transaction> transactions = env.fromData(

                new Transaction("C101", 15000, base + 10000),

                new Transaction("C202", 5000, base + 20000),

                new Transaction("C101", 20000, base + 45000),

                new Transaction("C202", 12000, base + 50000),

                new Transaction("C101", 3000, base + 55000),

                new Transaction("C101", 18000, base + 90000),

                new Transaction("C202", 14000, base + 130000)

        );



        transactions

                .keyBy(tx -> tx.customerId)

                .process(new FraudDetector())

                .print();



        env.execute("Fraud Detection Job");

    }

}




pom.xml



<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
https://maven.apache.org/xsd/maven-4.0.0.xsd">



   <modelVersion>4.0.0</modelVersion>



   <groupId>com.example</groupId>

   <artifactId>flink-practical</artifactId>

   <version>1.0-SNAPSHOT</version>



   <properties>

       <maven.compiler.release>17</maven.compiler.release>

       <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>

       <flink.version>1.19.2</flink.version>

   </properties>



   <dependencies>

       <dependency>

           <groupId>org.apache.flink</groupId>

           <artifactId>flink-streaming-java</artifactId>

           <version>${flink.version}</version>

       </dependency>



       <dependency>

           <groupId>org.apache.flink</groupId>

           <artifactId>flink-clients</artifactId>

           <version>${flink.version}</version>
    </dependency>

</dependencies>



<build>

    <sourceDirectory>${project.basedir}</sourceDirectory>

    <plugins>

          <plugin>

              <groupId>org.apache.maven.plugins</groupId>

              <artifactId>maven-compiler-plugin</artifactId>

              <version>3.13.0</version>

          </plugin>



          <plugin>

              <groupId>org.codehaus.mojo</groupId>

              <artifactId>exec-maven-plugin</artifactId>

              <version>3.6.4</version>

          </plugin>



          <plugin>

              <groupId>org.apache.maven.plugins</groupId>

              <artifactId>maven-shade-plugin</artifactId>

              <version>3.6.0</version>

              <executions>

                  <execution>

                      <phase>package</phase>

                      <goals>

                          <goal>shade</goal>
                           </goals>

                           <configuration>

                               <transformers>

                                    <transformer
implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTr
ansformer">


<mainClass>FraudDetectionJob</mainClass>

                                    </transformer>

                                    <transformer
implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTr
ansformer"/>

                               </transformers>

                           </configuration>

                      </execution>

                  </executions>

              </plugin>

         </plugins>

    </build>

</project>




Step 7: Download the Flink dependencies

mvn clean compile

The successful output included:

Compiling 1 source file with javac [debug release 17] to target\classes

BUILD SUCCESS
Step 8: Run the application
We ran the following command:

mvn clean package

This compiled the program and packaged it into:

target\flink-practical-1.0-SNAPSHOT.jar


Step 8: Run the application

We executed the following command in the terminal:

java -jar target\flink-practical-1.0-SNAPSHOT.jar

The program ran successfully and displayed the following output:

7> FRAUD ALERT: Customer=C101, Previous=?15000.0, Current=?20000.0, Gap=35
seconds

7> FRAUD ALERT: Customer=C101, Previous=?20000.0, Current=?18000.0, Gap=45
seconds
```
