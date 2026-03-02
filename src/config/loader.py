import yaml
from types import SimpleNamespace

def to_namespace(obj):
    if isinstance(obj, dict):
        return SimpleNamespace(
            **{k: to_namespace(v) for k, v in obj.items()}
        )
    elif isinstance(obj, list):
        return [to_namespace(i) for i in obj]
    else:
        return obj

def load_config():
    with open("configs/app.yaml") as f:
        raw = yaml.safe_load(f)
    return to_namespace(raw)

def load_class_names(path="configs/classes.yaml"):
    with open(path) as f:
        data = yaml.safe_load(f)

    # ensure int keys
    return {int(k): v for k, v in data.items()}