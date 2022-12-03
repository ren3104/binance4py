from typing import Any, Callable, Dict

JsonObject = Dict[str, Any]
JsonDumper = Callable[[JsonObject], str]
JsonLoader = Callable[[str], JsonObject]
