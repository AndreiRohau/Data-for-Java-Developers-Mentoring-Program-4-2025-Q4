-- Insert sample test data for windowed metrics
-- This represents typical metrics data from various components

INSERT INTO metrics.windowed_metrics 
(component_name, metric_name, unit, min_value, max_value, from_timestamp, to_timestamp)
VALUES
-- User Service CPU metrics
('user-service', 'cpu-usage', 'percent', 10.00, 23.00, '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
('user-service', 'cpu-usage', 'percent', 15.00, 28.00, '2021-09-09T12:20:02.001Z', '2021-09-09T12:25:02.001Z'),
('user-service', 'cpu-usage', 'percent', 12.00, 25.00, '2021-09-09T12:25:02.001Z', '2021-09-09T12:30:02.001Z'),

-- User Service Memory metrics
('user-service', 'memory-usage', 'percent', 45.00, 67.00, '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
('user-service', 'memory-usage', 'percent', 50.00, 72.00, '2021-09-09T12:20:02.001Z', '2021-09-09T12:25:02.001Z'),

-- API Gateway metrics
('api-gateway', 'cpu-usage', 'percent', 5.00, 15.00, '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
('api-gateway', 'response-time', 'milliseconds', 50.00, 120.00, '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
('api-gateway', 'request-count', 'count', 100.00, 500.00, '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),

-- Database Service metrics
('database-service', 'cpu-usage', 'percent', 20.00, 45.00, '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
('database-service', 'disk-io', 'mbps', 10.00, 35.00, '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
('database-service', 'connection-pool', 'count', 10.00, 25.00, '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),

-- Cache Service metrics
('cache-service', 'memory-usage', 'percent', 30.00, 55.00, '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
('cache-service', 'hit-rate', 'percent', 85.00, 95.00, '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z'),
('cache-service', 'eviction-rate', 'count', 5.00, 15.00, '2021-09-09T12:15:02.001Z', '2021-09-09T12:20:02.001Z');
