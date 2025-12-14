import math
from typing import Any


def clean_float_values(obj: Any) -> Any:
    """Recursively clean NaN and Infinity values from data structures."""
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif isinstance(obj, dict):
        return {k: clean_float_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_float_values(item) for item in obj]
    return obj
