import json

def is_jsonable(x):
    if x is None:
        return False
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False