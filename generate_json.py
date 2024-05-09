import hashlib
import json
import math
import os
import yaml
import bibtexparser

def hash_name(name):
    hsh = hashlib.sha256(name.encode())
    return hsh.hexdigest()[:8]


def convert_yaml_to_json(yaml_file):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)
    return data

def convert_bibtex_to_json(bib_file):
    """Convert a bibtex file to a json object using bibtexparser."""
    with open(bib_file, "r") as file:
        bib = file.read()
    print (bib)
    bib_database = bibtexparser.loads(bib)
    # if no reference in the file, return ''
    if len(bib_database.entries) == 0:
        return ''
    else:
        return bib_database.entries[0]


def process_folder():
    """Process all yaml and bibtex files in the catalog folder and generate a single json and bibtex file with all the data."""
    all_data = []
    all_bib = []
    nb_yaml_processed = 0
    nb_bib_processed = 0
    nb_skipped = 0
    # Walk through the catalog folder and process all yaml files in alphabetical order (easier to debug)
    for root, dirs, files in os.walk("catalog"):
        files.sort()
        for file in files:
            print(f"Processing {file}", end="...")
            if file.endswith(".yaml") or file.endswith(".yml"):
                yaml_file = os.path.join(root, file)
                raw_data = convert_yaml_to_json(yaml_file)
                _id = hash_name(raw_data["name"])

                for key, value in raw_data.items():
                    if isinstance(value, float) and math.isnan(value):
                        raw_data[key] = ""

                data = {"id": _id, **raw_data}
                all_data.append(data)
                nb_yaml_processed += 1
                print("Done")
            elif file.endswith(".bib"):
                bib_file = os.path.join(root, file)
                bib_data = convert_bibtex_to_json(bib_file)
                all_bib.append(bib_data)
                nb_bib_processed += 1
                print("Done")
            else:
                nb_skipped += 1
                print("Skipped")
    print(f"Processed {nb_yaml_processed} yaml files, {nb_bib_processed} bibtex files and skipped {nb_skipped} files")    

    with open("catalog.json", "w") as file:
        json.dump(all_data, file, indent=2)
    with open("bibliography.json", "w") as file:
        json.dump(all_bib, file, indent=2)


process_folder()
