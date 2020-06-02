import os
import json
import sqlite3

ANKI_BASE_PATH = os.path.expanduser("~/.local/share/Anki2/")
COLLECTION_PATH = ANKI_BASE_PATH + "{}/collection.anki2"


def save_collection_css(collection, output="output"):
    db_path = COLLECTION_PATH.format(collection)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT models from col")

    models = json.loads(c.fetchone()[0])
    for model in models.values():
        # Create folder for model
        name = model["name"]
        # Forward slashes mess up file paths
        clean_name = name.replace("/", "|")
        # Ex: output/M2/Cloze-AQ/
        dirpath = os.path.join(output, collection, clean_name)
        os.makedirs(dirpath, exist_ok=True)
        # Save css
        css = model["css"]
        with open(os.path.join(dirpath, "index.css"), "w") as f:
            f.write(css)


def get_collections():
    collection_dirs = []
    for listing in os.listdir(ANKI_BASE_PATH):
        listing_path = os.path.join(ANKI_BASE_PATH, listing)
        # Only look at directories, not files
        if not os.path.isdir(listing_path):
            continue
        # Ignore builtin addons/addons21 folders that are reserved
        if listing == "addons" or listing == "addons21":
            continue
        # Check that folder contains a collection, then add it
        db_path = os.path.join(listing_path, "collection.anki2")
        if os.path.isfile(db_path):
            collection_dirs.append(listing)
    return collection_dirs
