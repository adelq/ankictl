import os
import json
import sqlite3

COLLECTION_PATH = "~/.local/share/Anki2/{}/collection.anki2"


def save_collection_css(collection):
    db_path = os.path.expanduser(COLLECTION_PATH.format(collection))
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
