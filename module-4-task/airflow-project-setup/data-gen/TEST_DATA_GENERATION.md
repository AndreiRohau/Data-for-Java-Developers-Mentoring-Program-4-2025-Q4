# Test Data Generation Instructions

## Prerequisites

1. Download the test data generator JAR file from:
   https://git.epam.com/epm-cdp/global-java-foundation-program/java-courses/-/tree/main/data-training-for-devs/courses/Data_Training_for_Java_developers/aws/materials/test-data-generator-prebuilt

   Or use this direct path:
   - File: `test-data-generator-1.0.0-all.jar`

2. Make sure you have Java installed:
   ```bash
   java -version
   ```

## Generate Test Data

### Basic Usage

1. Place the `test-data-generator-1.0.0-all.jar` file in this directory

2. Run the generator with the provided configuration:
   ```bash
   java -jar test-data-generator-1.0.0-all.jar metrics-batch.json
   ```

3. The generator will create a CSV file in the `test-output` directory with 1000 windowed metrics records

### Configuration Details

The `metrics-batch.json` configuration generates CSV data with the following structure:
- **componentName**: Random service names (user-service, api-gateway, etc.)
- **metricName**: Random metric types (cpu-usage, memory-usage, etc.)
- **unit**: Measurement units (percent, milliseconds, etc.)
- **minValue**: Random value between 0-50
- **maxValue**: Random value between 50-100
- **fromTimestamp**: Sequential timestamps starting from 2024-01-01, 5-minute intervals
- **toTimestamp**: 5 minutes after fromTimestamp (300 seconds offset)

### Customization

You can customize the configuration:
- Change `recordsCount` for more/fewer records
- Modify the `values` arrays to add/remove component names or metrics
- Adjust the timestamp start time and interval
- Change min/max value ranges

## Copy Data to Airflow

After generation, copy the CSV file to the Airflow dags/data folder:

```bash
cp test-output/*.csv airflow/dags/data/
```

## Sample Output Format

The generated CSV will look like:

```csv
componentName,metricName,unit,minValue,maxValue,fromTimestamp,toTimestamp
user-service,cpu-usage,percent,15.23,78.45,2024-01-01T00:00:00.000Z,2024-01-01T00:05:00.000Z
api-gateway,response-time,milliseconds,8.12,92.34,2024-01-01T00:05:00.000Z,2024-01-01T00:10:00.000Z
database-service,disk-io,mbps,22.56,67.89,2024-01-01T00:10:00.000Z,2024-01-01T00:15:00.000Z
```

## Verify Generated Data

Check the generated file:
```bash
head -n 5 test-output/*.csv
wc -l test-output/*.csv
```
