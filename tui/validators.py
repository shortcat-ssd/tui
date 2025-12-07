import re

def validate_dataclass(instance):
    pass

def validate(name, value, min_length=None, max_length=None, custom=None, equals=None):
    if min_length is not None and len(str(value)) < min_length:
        raise ValueError(f"{name} too short")
    if max_length is not None and len(str(value)) > max_length:
        raise ValueError(f"{name} too long")
    if custom and not custom(value):
        raise ValueError(f"Validation failed for {name}")
    if equals is not None and value != equals:
        raise ValueError(f"{name} must equal {equals}")
