package com.arohau.modeul2task;

import org.apache.spark.sql.*;
import org.apache.spark.sql.api.java.UDF1;
import org.apache.spark.sql.types.DataTypes;

import java.net.URISyntaxException;
import java.net.URL;
import java.nio.file.Paths;

import static org.apache.spark.sql.functions.callUDF;
import static org.apache.spark.sql.functions.col;

public class SparkBonusTestUdf {
    private static final String CSV_RESOURCE = "bonus.csv";

    private static final String ACTUAL_DEPOSIT_FUNCTION = "getActualDepositType";
    private static final String SHORT_TERM_DEPOSIT = "Short Term Deposit";
    private static final String LONG_TERM_DEPOSIT = "Long Term Deposit";
    private static final String CURRENT_DEPOSIT = "Current Deposit";

    /*
    cmd
    spark-shell
     */
    public static void main(String args[]) throws URISyntaxException {
        // Get the resource URL
        URL resource = SparkBonusTestUdf.class.getClassLoader().getResource(CSV_RESOURCE);
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
        spark.udf().register(ACTUAL_DEPOSIT_FUNCTION, getAccurateDepositType, DataTypes.StringType);

        csv.withColumn("deposit name", callUDF(ACTUAL_DEPOSIT_FUNCTION, col("deposit type"))).show();

        csv.withColumn("deposit name", callUDF(ACTUAL_DEPOSIT_FUNCTION, col("deposit type")))
                .groupBy("deposit name").avg("amount").show();

        System.out.println("pause");
    }

    private static final UDF1 getAccurateDepositType = new UDF1<Integer, String>() {
        public String call(final Integer i) throws Exception {
            switch (i) {
                case 1:
                    return SHORT_TERM_DEPOSIT;
                case 2:
                    return LONG_TERM_DEPOSIT;
                case 3:
                    return CURRENT_DEPOSIT;
            }
            return null;
        }
    };
}