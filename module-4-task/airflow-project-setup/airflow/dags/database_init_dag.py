"""
Database Initialization DAG

This DAG initializes the NeonDB database with the required schema and tables
for windowed metrics. It creates the windowed_metrics table and optionally
populates it with test data.
"""

from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


@dag(
    dag_id='database_init',
    description='DAG for initializing PostgreSQL database with windowed metrics schema',
    schedule=None,  # Manual trigger only
    start_date=datetime(2024, 1, 4),
    catchup=False,
    tags=["database", "initialization", "neondb"],
)
def database_init_dag():
    """Initialize the database with windowed metrics schema."""
    
    @task
    def test_connection():
        """Test the database connection before proceeding."""
        hook = PostgresHook(postgres_conn_id='neon_db_metrics')
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL version: {version[0]}")
        cursor.close()
        conn.close()
        return "Connection successful"
    
    # Create the windowed_metrics table
    create_table = PostgresOperator(
        task_id='create_windowed_metrics_table',
        postgres_conn_id='neon_db_metrics',
        sql="""
            CREATE TABLE IF NOT EXISTS metrics.windowed_metrics (
                id SERIAL PRIMARY KEY,
                component_name VARCHAR(255) NOT NULL,
                metric_name VARCHAR(255) NOT NULL,
                unit VARCHAR(50) NOT NULL,
                min_value DECIMAL(10, 2) NOT NULL,
                max_value DECIMAL(10, 2) NOT NULL,
                from_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
                to_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                
                CONSTRAINT check_min_max CHECK (min_value <= max_value),
                CONSTRAINT check_timestamps CHECK (from_timestamp < to_timestamp)
            );
        """
    )
    
    # Create indexes
    create_indexes = PostgresOperator(
        task_id='create_indexes',
        postgres_conn_id='neon_db_metrics',
        sql="""
            CREATE INDEX IF NOT EXISTS idx_windowed_metrics_component 
                ON metrics.windowed_metrics(component_name);
            
            CREATE INDEX IF NOT EXISTS idx_windowed_metrics_metric_name 
                ON metrics.windowed_metrics(metric_name);
            
            CREATE INDEX IF NOT EXISTS idx_windowed_metrics_timestamps 
                ON metrics.windowed_metrics(from_timestamp, to_timestamp);
            
            CREATE INDEX IF NOT EXISTS idx_windowed_metrics_composite 
                ON metrics.windowed_metrics(component_name, metric_name, from_timestamp);
        """
    )
    
    # Add comments for documentation
    add_comments = PostgresOperator(
        task_id='add_table_comments',
        postgres_conn_id='neon_db_metrics',
        sql="""
            COMMENT ON TABLE metrics.windowed_metrics IS 
                'Aggregated metrics data in 5-minute windows';
            
            COMMENT ON COLUMN metrics.windowed_metrics.component_name IS 
                'The component that produced the event';
            
            COMMENT ON COLUMN metrics.windowed_metrics.metric_name IS 
                'The name of the metric (e.g., cpu-usage, memory-usage)';
            
            COMMENT ON COLUMN metrics.windowed_metrics.unit IS 
                'Measurement unit (e.g., percent, bytes, milliseconds)';
            
            COMMENT ON COLUMN metrics.windowed_metrics.min_value IS 
                'Minimum value recorded in the time window';
            
            COMMENT ON COLUMN metrics.windowed_metrics.max_value IS 
                'Maximum value recorded in the time window';
            
            COMMENT ON COLUMN metrics.windowed_metrics.from_timestamp IS 
                'Start of the time window';
            
            COMMENT ON COLUMN metrics.windowed_metrics.to_timestamp IS 
                'End of the time window';
        """
    )
    
    # Insert test data
    insert_test_data = PostgresOperator(
        task_id='insert_test_data',
        postgres_conn_id='neon_db_metrics',
        sql="""
            INSERT INTO metrics.windowed_metrics 
            (component_name, metric_name, unit, min_value, max_value, from_timestamp, to_timestamp)
            VALUES
            -- User Service CPU metrics
            ('user-service', 'cpu-usage', 'percent', 10.00, 23.00, 
                '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
            ('user-service', 'cpu-usage', 'percent', 15.00, 28.00, 
                '2021-09-09T12:20:02.001Z', '2021-09-09T12:25:02.001Z'),
            ('user-service', 'cpu-usage', 'percent', 12.00, 25.00, 
                '2021-09-09T12:25:02.001Z', '2021-09-09T12:30:02.001Z'),
            
            -- User Service Memory metrics
            ('user-service', 'memory-usage', 'percent', 45.00, 67.00, 
                '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
            ('user-service', 'memory-usage', 'percent', 50.00, 72.00, 
                '2021-09-09T12:20:02.001Z', '2021-09-09T12:25:02.001Z'),
            
            -- API Gateway metrics
            ('api-gateway', 'cpu-usage', 'percent', 5.00, 15.00, 
                '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
            ('api-gateway', 'response-time', 'milliseconds', 50.00, 120.00, 
                '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
            ('api-gateway', 'request-count', 'count', 100.00, 500.00, 
                '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
            
            -- Database Service metrics
            ('database-service', 'cpu-usage', 'percent', 20.00, 45.00, 
                '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
            ('database-service', 'disk-io', 'mbps', 10.00, 35.00, 
                '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
            ('database-service', 'connection-pool', 'count', 10.00, 25.00, 
                '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
            
            -- Cache Service metrics
            ('cache-service', 'memory-usage', 'percent', 30.00, 55.00, 
                '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
            ('cache-service', 'hit-rate', 'percent', 85.00, 95.00, 
                '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
            ('cache-service', 'eviction-rate', 'count', 5.00, 15.00, 
                '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z')
            ON CONFLICT DO NOTHING;
        """
    )
    
    @task
    def verify_data():
        """Verify that data was inserted successfully."""
        hook = PostgresHook(postgres_conn_id='neon_db_metrics')
        conn = hook.get_conn()
        cursor = conn.cursor()
        
        # Count total records
        cursor.execute("SELECT COUNT(*) FROM metrics.windowed_metrics;")
        count = cursor.fetchone()[0]
        print(f"Total records in windowed_metrics table: {count}")
        
        # Show sample data
        cursor.execute("""
            SELECT component_name, metric_name, unit, min_value, max_value 
            FROM metrics.windowed_metrics 
            LIMIT 5;
        """)
        samples = cursor.fetchall()
        print("\nSample data:")
        for row in samples:
            print(f"  {row[0]} - {row[1]} ({row[2]}): min={row[3]}, max={row[4]}")
        
        cursor.close()
        conn.close()
        return f"Verification complete: {count} records"
    
    # Define task dependencies
    connection_test = test_connection()
    verify = verify_data()
    
    connection_test >> create_table >> create_indexes >> add_comments >> insert_test_data >> verify


# Instantiate the DAG
database_init_dag()
