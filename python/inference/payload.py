"""Parse MQTT sensor payloads into numeric row batches."""

from __future__ import annotations


def parse_mqtt_payload(payload_str: str) -> list[list[float]]:
    """Convert a CSV MQTT payload into a list of sensor rows."""
    data: list[list[float]] = []
    for line in payload_str.splitlines():
        data.append([float(value) for value in line.split(",")])
    return data
