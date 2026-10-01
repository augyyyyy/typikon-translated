import json
import glob

vocab = {
    "vespers_type": set(),
    "matins_type": set(),
    "liturgy_type": set(),
    "has_polyeleos": set(),
    "doxology_type": set(),
}

def scan_dict(d):
    if not isinstance(d, dict):
        return
    for k, v in d.items():
        if k in vocab:
            vocab[k].add(str(v))
        if isinstance(v, dict):
            scan_dict(v)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    scan_dict(item)

for fn in glob.glob("json_db/*.json"):
    with open(fn, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            scan_dict(data)
        except Exception as e:
            pass

for k, s in vocab.items():
    print(f"{k}: {sorted(list(s))}")
