"""
Data Quality Pipeline DAG

This DAG ingests CSV files from the dags/data folder into NeonDB,
processes them, and moves them to a processed folder.
Then triggers DBT Cloud job for data transformations and tests.
"""

from datetime import datetime
from pathlib import Path
import shutil

from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator


@dag(
    dag_id='data_quality_pipeline',
    description='Ingests windowed metrics CSV files into NeonDB',
    schedule=None,  # Manual trigger only
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["data-ingestion", "neondb", "metrics"],
)
def data_quality_pipeline():
    """Data quality pipeline for ingesting metrics CSV files."""
    
    @task
    def install_dependencies():
        """Install required Python dependencies."""
        import subprocess
        
        # psycopg2 is already included in Airflow, but ensure we have the CSV extras
        dependencies = [
            'psycopg2-binary',
        ]
        
        for dep in dependencies:
            try:
                subprocess.run(['pip', 'install', dep], check=True, capture_output=True)
                print(f"✓ Installed {dep}")
            except subprocess.CalledProcessError as e:
                print(f"Note: {dep} may already be installed or included: {e}")
        
        return "Dependencies ready"
    
    @task
    def ingest_csv_files(deps_ready: str):
        """
        Ingest CSV files from dags/data folder into NeonDB.
        Uses PostgreSQL COPY command for efficient bulk loading.
        """
        import csv
        
        # Paths
        data_dir = Path('/usr/local/airflow/dags/data')
        processed_dir = Path('/usr/local/airflow/dags/data/processed')
        processed_dir.mkdir(exist_ok=True)
        
        # Get database connection
        hook = PostgresHook(postgres_conn_id='neon_db_metrics')
        conn = hook.get_conn()
        cursor = conn.cursor()
        
        # Find all CSV files that haven't been processed yet
        # Check if file exists in processed/ OR if a marker file exists
        all_csv_files = list(data_dir.glob('*.csv'))
        csv_files = []
        for csv_file in all_csv_files:
            processed_file = processed_dir / csv_file.name
            marker_file = processed_dir / f"{csv_file.name}.processed"
            
            # Skip if already processed (file moved or marker exists)
            if processed_file.exists() or marker_file.exists():
                print(f"Skipping {csv_file.name} - already processed")
                continue
            
            csv_files.append(csv_file)
        
        if not csv_files:
            print("No CSV files found in dags/data folder")
            return "No files to process"
        
        print(f"Found {len(csv_files)} CSV file(s) to process")
        
        processed_count = 0
        total_records = 0
        
        for csv_file in csv_files:
            try:
                print(f"\n--- Processing: {csv_file.name} ---")
                
                # Count records (excluding header)
                with open(csv_file, 'r') as f:
                    record_count = sum(1 for _ in f) - 1  # -1 for header
                
                print(f"Records to insert: {record_count}")
                
                # Use COPY command for bulk insert
                # The CSV has: componentName,fromTimestamp,maxValue,metricName,minValue,toTimestamp,unit
                # Our table expects: component_name,metric_name,unit,min_value,max_value,from_timestamp,to_timestamp
                
                with open(csv_file, 'r') as f:
                    # Skip header
                    next(f)
                    
                    # Use copy_expert for better control
                    copy_sql = """
                        COPY metrics.windowed_metrics 
                        (component_name, from_timestamp, max_value, metric_name, min_value, to_timestamp, unit)
                        FROM STDIN WITH CSV
                    """
                    
                    cursor.copy_expert(sql=copy_sql, file=f)
                
                # Commit the transaction
                conn.commit()
                print(f"✓ Committed {record_count} records from {csv_file.name}")
                
                # Move file to processed folder
                processed_file = processed_dir / csv_file.name
                try:
                    shutil.move(str(csv_file), str(processed_file))
                    print(f"✓ Moved {csv_file.name} to processed/")
                except (PermissionError, OSError) as e:
                    # If we can't move, try to create a marker file instead
                    print(f"⚠ Could not move file: {e}")
                    marker_file = processed_dir / f"{csv_file.name}.processed"
                    try:
                        marker_file.touch()
                        print(f"✓ Created marker file: {marker_file.name}")
                    except Exception as marker_error:
                        print(f"⚠ Could not create marker: {marker_error}, but data was imported successfully")
                
                processed_count += 1
                total_records += record_count
                
            except Exception as e:
                print(f"✗ Error processing {csv_file.name}: {e}")
                conn.rollback()
                raise
        
        # Verify data was inserted
        cursor.execute("""
            SELECT component_name, COUNT(1) as amount 
            FROM metrics.windowed_metrics
            GROUP BY component_name
            ORDER BY component_name;
        """)
        
        results = cursor.fetchall()
        
        print("\n=== Ingestion Summary ===")
        print(f"Files processed: {processed_count}")
        print(f"Total records inserted: {total_records}")
        print("\nRecords by component:")
        for component, count in results:
            print(f"  {component}: {count}")
        
        cursor.close()
        conn.close()
        
        return f"Successfully processed {processed_count} file(s), {total_records} records"
    
    @task
    def verify_data():
        """Verify data integrity after ingestion."""
        hook = PostgresHook(postgres_conn_id='neon_db_metrics')
        conn = hook.get_conn()
        cursor = conn.cursor()
        
        # Check total count
        cursor.execute("SELECT COUNT(*) FROM metrics.windowed_metrics;")
        total = cursor.fetchone()[0]
        
        # Check by component
        cursor.execute("""
            SELECT 
                component_name, 
                COUNT(1) as record_count,
                COUNT(DISTINCT metric_name) as metric_types,
                MIN(from_timestamp) as earliest,
                MAX(to_timestamp) as latest
            FROM metrics.windowed_metrics
            GROUP BY component_name
            ORDER BY component_name;
        """)
        
        results = cursor.fetchall()
        
        print("\n=== Data Verification ===")
        print(f"Total records in database: {total}")
        print("\nDetailed breakdown:")
        for row in results:
            component, count, metrics, earliest, latest = row
            print(f"\n{component}:")
            print(f"  Records: {count}")
            print(f"  Metric types: {metrics}")
            print(f"  Time range: {earliest} to {latest}")
        
        # Data quality checks
        cursor.execute("""
            SELECT COUNT(*) 
            FROM metrics.windowed_metrics 
            WHERE min_value > max_value;
        """)
        invalid_ranges = cursor.fetchone()[0]
        
        if invalid_ranges > 0:
            print(f"\n⚠ Warning: {invalid_ranges} records have min_value > max_value")
        else:
            print("\n✓ All records have valid min/max ranges")
        
        cursor.close()
        conn.close()
        
        return f"Verification complete: {total} total records"
    
    # DBT Cloud job trigger
    trigger_dbt_cloud_job = DbtCloudRunJobOperator(
        task_id="trigger_dbt_cloud_job_run",
        dbt_cloud_conn_id="dbt_cloud_connection",  # Connection name in Airflow
        job_id=70471823534131,  # Replace with your actual DBT Cloud job ID
        check_interval=10,
        timeout=300,
    )
    
    # Define task dependencies
    deps = install_dependencies()
    ingestion_result = ingest_csv_files(deps)
    verification_result = verify_data()
    
    deps >> ingestion_result >> verification_result >> trigger_dbt_cloud_job


# Instantiate the DAG
data_quality_pipeline()
