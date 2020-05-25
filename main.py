import os
import json
import sqlite3

ANKI_BASE_PATH = os.path.expanduser("~/.local/share/Anki2/")
COLLECTION_PATH = ANKI_BASE_PATH + "{}/collection.anki2"


def save_collection_css(collection):
    db_path = COLLECTION_PATH.format(collection)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT models from col")

    os.makedirs(collection, exist_ok=True)
    models = json.loads(c.fetchone()[0])
    for model in models.values():
        name = model["name"]
        css = model["css"]
        # Forward slashes mess up file paths
        filename = "{}.css".format(name.replace("/", "|"))
        filepath = os.path.join(collection, filename)
        with open(filepath, "w") as f:
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
