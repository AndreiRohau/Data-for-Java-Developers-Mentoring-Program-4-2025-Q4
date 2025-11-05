package com.arohau.modeul2task;

import org.apache.spark.sql.SparkSession;

/**
 * Hello world!
 */
public class App {
    public static void main(String[] args) {
        System.out.println("Hello World!");

        SparkSession spark = SparkSession.builder().master("local[*]").getOrCreate();


    }
}
