"""
Windowed Metrics Data Model

This module defines the data model for windowed metrics that represent
an aggregation of the metrics stream in windows of 5-minute length.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import json


@dataclass
class WindowedMetric:
    """
    Represents a windowed metric aggregation.
    
    Attributes:
        component_name: The component that produced the event (e.g., 'user-service')
        metric_name: The name of the metric (e.g., 'cpu-usage', 'memory-usage')
        unit: Measurement unit (e.g., 'percent', 'milliseconds', 'count')
        min_value: Minimum value recorded in the time window
        max_value: Maximum value recorded in the time window
        from_timestamp: Start of the time window (ISO 8601 format)
        to_timestamp: End of the time window (ISO 8601 format)
        id: Optional database ID
    """
    component_name: str
    metric_name: str
    unit: str
    min_value: float
    max_value: float
    from_timestamp: str  # ISO 8601 format
    to_timestamp: str    # ISO 8601 format
    id: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convert the metric to a dictionary."""
        return {
            "componentName": self.component_name,
            "metricName": self.metric_name,
            "unit": self.unit,
            "minValue": self.min_value,
            "maxValue": self.max_value,
            "fromTimestamp": self.from_timestamp,
            "toTimestamp": self.to_timestamp
        }
    
    def to_json(self) -> str:
        """Convert the metric to a JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'WindowedMetric':
        """Create a WindowedMetric from a dictionary."""
        return cls(
            component_name=data.get("componentName", data.get("component_name")),
            metric_name=data.get("metricName", data.get("metric_name")),
            unit=data.get("unit"),
            min_value=float(data.get("minValue", data.get("min_value"))),
            max_value=float(data.get("maxValue", data.get("max_value"))),
            from_timestamp=data.get("fromTimestamp", data.get("from_timestamp")),
            to_timestamp=data.get("toTimestamp", data.get("to_timestamp")),
            id=data.get("id")
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'WindowedMetric':
        """Create a WindowedMetric from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def validate(self) -> bool:
        """
        Validate the metric data.
        
        Returns:
            True if valid, raises ValueError if invalid
        """
        if self.min_value > self.max_value:
            raise ValueError(f"min_value ({self.min_value}) cannot be greater than max_value ({self.max_value})")
        
        from_dt = datetime.fromisoformat(self.from_timestamp.replace('Z', '+00:00'))
        to_dt = datetime.fromisoformat(self.to_timestamp.replace('Z', '+00:00'))
        
        if from_dt >= to_dt:
            raise ValueError(f"from_timestamp ({self.from_timestamp}) must be before to_timestamp ({self.to_timestamp})")
        
        return True


# Example usage and test data
if __name__ == "__main__":
    # Example 1: Create from the provided JSON format
    example_json = """
    {
      "componentName": "user-service",
      "metricName": "cpu-usage",
      "unit": "percent",
      "minValue": 10,
      "maxValue": 23,
      "fromTimestamp": "2021-09-09T12:15:02.001Z",
      "toTimestamp": "2021-09-09T12:20:02.001Z"
    }
    """
    
    metric = WindowedMetric.from_json(example_json)
    print("Created metric from JSON:")
    print(metric)
    print("\nValidation result:", metric.validate())
    print("\nConverted back to JSON:")
    print(metric.to_json())
    
    # Example 2: Create programmatically
    metric2 = WindowedMetric(
        component_name="api-gateway",
        metric_name="response-time",
        unit="milliseconds",
        min_value=50.0,
        max_value=120.0,
        from_timestamp="2021-09-09T12:15:02.001Z",
        to_timestamp="2021-09-09T12:20:02.001Z"
    )
    print("\n\nCreated metric programmatically:")
    print(metric2.to_json())
