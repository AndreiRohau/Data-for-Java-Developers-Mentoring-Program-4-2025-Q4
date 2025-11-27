-- Create table for windowed metrics in NeonDB
-- This represents an aggregation of the metrics stream in windows of 5-minute length

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
    
    -- Add indexes for common query patterns
    CONSTRAINT check_min_max CHECK (min_value <= max_value),
    CONSTRAINT check_timestamps CHECK (from_timestamp < to_timestamp)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_windowed_metrics_component ON metrics.windowed_metrics(component_name);
CREATE INDEX IF NOT EXISTS idx_windowed_metrics_metric_name ON metrics.windowed_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_windowed_metrics_timestamps ON metrics.windowed_metrics(from_timestamp, to_timestamp);
CREATE INDEX IF NOT EXISTS idx_windowed_metrics_composite ON metrics.windowed_metrics(component_name, metric_name, from_timestamp);

-- Add comment for documentation
COMMENT ON TABLE metrics.windowed_metrics IS 'Aggregated metrics data in 5-minute windows';
COMMENT ON COLUMN metrics.windowed_metrics.component_name IS 'The component that produced the event';
COMMENT ON COLUMN metrics.windowed_metrics.metric_name IS 'The name of the metric (e.g., cpu-usage, memory-usage)';
COMMENT ON COLUMN metrics.windowed_metrics.unit IS 'Measurement unit (e.g., percent, bytes, milliseconds)';
COMMENT ON COLUMN metrics.windowed_metrics.min_value IS 'Minimum value recorded in the time window';
COMMENT ON COLUMN metrics.windowed_metrics.max_value IS 'Maximum value recorded in the time window';
COMMENT ON COLUMN metrics.windowed_metrics.from_timestamp IS 'Start of the time window';
COMMENT ON COLUMN metrics.windowed_metrics.to_timestamp IS 'End of the time window';
