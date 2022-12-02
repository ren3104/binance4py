from typing import Any, Dict, Callable


JsonObject = Dict[str, Any]
JsonDumper = Callable[[JsonObject], str]
JsonLoader = Callable[[str], JsonObject]
