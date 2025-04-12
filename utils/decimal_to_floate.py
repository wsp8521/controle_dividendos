from decimal import Decimal

def decimal_para_float(data):
    if isinstance(data, dict):
        return {k: decimal_para_float(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [decimal_para_float(v) for v in data]
    elif isinstance(data, Decimal):
        return float(data)
    return data
