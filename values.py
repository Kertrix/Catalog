# Get all possible language values from the catalog
import os

import yaml


def get_all_values():
    value_list = {"language": [], "task": [], "mode": [], "format": []}

    for root, dirs, files in os.walk("catalog"):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                with open(os.path.join(root, file), "r") as file:
                    data = yaml.safe_load(file)
                    for prop in ["language", "task", "mode", "format"]:
                        values = data[prop]
                        for value in values:
                            if value not in value_list[prop]:
                                value_list[prop].append(value)

    return value_list
