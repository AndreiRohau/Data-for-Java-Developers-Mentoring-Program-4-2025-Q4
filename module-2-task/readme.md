
Run this command before running java code:
```shell
spark-shell.cmd
```
use <code>:quit</code> to stop process

OR

```shell
pyspark.cmd
```
use <code>quit()</code> to stop process

---
Guide
---

```commandline
Used this to set up environment
https://www.youtube.com/watch?v=JjIwAMXUvYc

and code snippets from here
https://dzone.com/articles/the-magic-of-apache-spark-in-java-1

```

```commandline
Require installing tools into windows 11 x64

Download:

spark-4.0.1-bin-hadoop3.tgz
Spark: 4.0.1 (Sep 6, 2025)
Apache Hadoop 3.4 and later
https://spark.apache.org/downloads.html
https://dlcdn.apache.org/spark/spark-4.0.1/spark-4.0.1-bin-hadoop3.tgz

and

winutils.exe
https://github.com/kontext-tech/winutils/blob/master/hadoop-3.4.0-win10-x64/bin/winutils.exe
```

```commandline
Setup steps:
1) exatract spark-4.0.1-bin-hadoop3.tgz into C:\spark
2) copy winutils.exe into C:\hadoop
3) install jdk 17
4) install python 3.9+ (mine 3.11)
5) setup SPARK_HOME -> C:\spark
6) add to path variable %SPARK_HOME%\bin
7) setup HADOOP_HOME -> C:\hadoop
8) add to path variable %HADOOP_HOME%\bin
9) setup JAVA_HOME -> C:\dev\jdk17
10) add to path variable %JAVA_HOME%\bin
11) setup PYTHON_HOME -> C:\dev\python3.11
12) add to path variable %PYTHON_HOME%\bin


```

```commandline
Check:

PS C:\Users\Andrei_Rohau> java --version
openjdk 17.0.15 2025-04-15 LTS
OpenJDK Runtime Environment Corretto-17.0.15.6.1 (build 17.0.15+6-LTS)
OpenJDK 64-Bit Server VM Corretto-17.0.15.6.1 (build 17.0.15+6-LTS, mixed mode, sharing)
PS C:\Users\Andrei_Rohau> python --version
Python 3.11.0
PS C:\Users\Andrei_Rohau>
```

```commandline
      Code dependencies:
      
      <dependency>
          <groupId>org.apache.spark</groupId>
          <artifactId>spark-core_2.13</artifactId>
          <version>4.0.1</version>
      </dependency>
      <dependency>
          <groupId>org.apache.spark</groupId>
          <artifactId>spark-sql_2.13</artifactId>
          <version>4.0.1</version>
      </dependency>
```

```commandline
// Test snippet

package com.arohau.modeul2task;

import org.apache.spark.api.java.function.FilterFunction;
import org.apache.spark.sql.*;

import java.net.URISyntaxException;
import java.net.URL;
import java.nio.file.Paths;

import static org.apache.spark.sql.functions.col;

public class SparkBonusTest {
    private static final String CSV_RESOURCE = "bonus.csv"; // .src/main/resources/bonus.csv

    /*
    cmd
    spark-shell
     */
    public static void main(String args[]) throws URISyntaxException {
        // Get the resource URL
        URL resource = SparkBonusTest.class.getClassLoader().getResource(CSV_RESOURCE);
        if (resource == null) {
            throw new IllegalArgumentException("File not found! " + CSV_RESOURCE);
        }
        String csvPath = Paths.get(resource.toURI()).toString();

        SparkSession spark = SparkSession.builder().master("local[*]").getOrCreate();
        Dataset<Row> csv = spark.read().format("csv")
                .option("sep", ",")
                .option("inferSchema", "true")
                .option("header", "true")
                .load(csvPath);
        csv.show();
        csv.printSchema();


        csv.filter("name like 'reza'").show();

        csv.filter("amount >102").show();

        csv.filter(new FilterFunction<Row>() {
            @Override
            public boolean call(Row row) throws Exception {
                return row.getAs("amount").equals(102);
            }
        }).show();

        csv.groupBy(col("deposit type")).sum("amount").show();

        System.out.println("pause");
    }
}
```

```commandline
1) open cmd
2) run `spark-shell` (`:quit`) OR `pyspark` (`quit()`)
3) http://host.docker.internal:4040
4) run java code
```


