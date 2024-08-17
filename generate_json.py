import hashlib
import json
import math
import os

import yaml

from values import get_all_values


def hash_name(name):
    hsh = hashlib.sha256(name.encode())
    return hsh.hexdigest()[:8]


def convert_yaml_to_json(yaml_file):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)
    return data


def process_folder():
    all_data = []
    for root, dirs, files in os.walk("catalog"):
        for file in files:
            if not file.startswith("[EXCLUDED]") and (file.endswith(".yaml") or file.endswith(".yml")):
                yaml_file = os.path.join(root, file)
                raw_data = convert_yaml_to_json(yaml_file)
                _id = hash_name(raw_data["name"])

                for key, value in raw_data.items():
                    if isinstance(value, float) and math.isnan(value):
                        raw_data[key] = ""

                data = {"id": _id, **raw_data}
                all_data.append(data)

    with open("catalog.json", "w") as file:
        json.dump(all_data, file, indent=2)


process_folder()

with open("values.json", "w") as f:
    json.dump(get_all_values(), f, indent=2)
