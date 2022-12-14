import time
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional, Union


def create_query_dict(params: Dict[str, Any]) -> Dict[str, Any]:
    query_dict = {}
    for k, v in params.items():
        if v is None:
            continue
        elif isinstance(v, list):
            query_dict[k] = str(v).replace("'", '"').replace(" ", "")
        elif isinstance(v, (int, float, Decimal)):
            query_dict[k] = number_to_string(v)
        else:
            query_dict[k] = v
    return query_dict


def millisecond_to_datetime(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000)


def get_timestamp() -> int:
    return int(time.time() * 1000)


def quantize_tick_size(
    num: Union[str, int, float, Decimal],
    tick_size: Union[str, Decimal],
    rounding: Optional[str] = None,
) -> Decimal:
    if isinstance(num, (int, float)):
        num = Decimal(str(num))
    elif isinstance(num, str):
        num = Decimal(num)

    if isinstance(tick_size, str):
        tick_size = Decimal(tick_size)

    return num.quantize(tick_size.normalize(), rounding).normalize()


def number_to_string(num: Union[int, float, Decimal]) -> str:
    formatted_num = "{:f}".format(num)
    if "." in formatted_num:
        return formatted_num.rstrip("0").rstrip(".")
    return formatted_num
