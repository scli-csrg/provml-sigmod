from typing import Any, Dict
class Adapter:
    event_type: str = ""
    def emit(self, **kwargs: Any) -> Dict[str, Any]:
        raise NotImplementedError
