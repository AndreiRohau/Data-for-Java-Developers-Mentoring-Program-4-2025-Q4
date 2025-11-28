-- Test that max_value doesn't exceed threshold
-- Change threshold to test failure/success scenarios

SELECT
    component_name,
    metric_name,
    max_value
FROM {{ ref('metrics_view') }}
WHERE max_value < 50  -- Set to 50 to make it fail