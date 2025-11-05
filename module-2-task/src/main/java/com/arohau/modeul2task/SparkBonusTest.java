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