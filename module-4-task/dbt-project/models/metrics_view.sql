{{
    config(
        materialized='view'
    )
}}

-- Windowed metrics view model
SELECT
    id,
    component_name,
    metric_name,
    unit,
    min_value,
    max_value,
    from_timestamp,
    to_timestamp,
    created_at
FROM metrics.windowed_metrics
ORDER BY from_timestamp DESC, component_name, metric_name