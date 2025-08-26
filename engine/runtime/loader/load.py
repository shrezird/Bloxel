import json
from pathlib import Path

class Loader:
    def __init__(self, filename):
        base = Path(__file__).parent
        for k, v in json.loads((base / filename).read_text(encoding='utf-8')).items():
            setattr(self, k, (base / v).resolve().as_uri() if isinstance(v, str) and (base / v).exists() else v)

load = Loader('directories.json')