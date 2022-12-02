import time
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Union


def create_query_dict(params: Dict[str, Any]) -> Dict[str, str]:
    query_dict = {}
    for k, v in params.items():
        if v is None:
            continue
        elif isinstance(v, list):
            query_dict[k] = str(v).replace("'", "\"").replace(" ", "")
        elif isinstance(v, (int, float, Decimal)):
            query_dict[k] = number_to_string(v)
        else:
            query_dict[k] = v
    return query_dict


def millisecond_to_datetime(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000)


def get_timestamp() -> int:
    return int(time.time() * 1000)


def quantize_tick_size(num: Union[str, int, float, Decimal], tick_size: str) -> Decimal:
    if isinstance(num, (int, float)):
        num = str(num)
    if isinstance(num, str):
        num = Decimal(num)
    return num.quantize(Decimal(tick_size).normalize()).normalize()


def number_to_string(num: Union[int, float, Decimal]) -> str:
    return "{:f}".format(num).rstrip("0").rstrip(".")
