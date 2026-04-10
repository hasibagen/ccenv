"""
Formatters for ccenv output
"""

import json
from typing import Any, List, Dict


def format_table(data: List[Dict[str, Any]], columns: List[str]) -> str:
    """Format data as a table.

    Args:
        data: List of dictionaries
        columns: Column names to display

    Returns:
        Formatted table string
    """
    if not data:
        return "No data"

    # Calculate column widths
    widths = {col: len(col) for col in columns}
    for row in data:
        for col in columns:
            widths[col] = max(widths[col], len(str(row.get(col, ""))))

    # Build header
    header = "  ".join(col.ljust(widths[col]) for col in columns)
    separator = "  ".join("-" * widths[col] for col in columns)

    # Build rows
    rows = []
    for row in data:
        row_str = "  ".join(str(row.get(col, "")).ljust(widths[col]) for col in columns)
        rows.append(row_str)

    return "\n".join([header, separator] + rows)


def format_json(data: Any) -> str:
    """Format data as JSON.

    Args:
        data: Data to format

    Returns:
        Formatted JSON string
    """
    return json.dumps(data, indent=2, ensure_ascii=False)


def format_yaml(data: Any) -> str:
    """Format data as YAML.

    Args:
        data: Data to format

    Returns:
        Formatted YAML string
    """
    import yaml
    return yaml.dump(data, default_flow_style=False, allow_unicode=True)