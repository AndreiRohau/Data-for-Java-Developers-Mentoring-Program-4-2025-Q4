package com.arohau.modeul2task;

import org.apache.spark.sql.*;

public class SparkBonusTest {
    private static final String CSV_URL = "bonus.csv";

    public static void main(String args[]) {
        SparkSession spark=SparkSession.builder().master("local[*]").getOrCreate();
        Dataset<Row> csv = spark.read().format("csv")
                .option("sep", ",")
                .option("inferSchema", "true")
                .option("header", "true")
                .load(CSV_URL);
        csv.show();
        csv.printSchema();
    }
}