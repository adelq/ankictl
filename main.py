import os
import json
import sqlite3

from aqt import mw
from aqt.qt import QAction
from aqt.utils import tooltip

OUTPUT_DIR = "/home/adel/Projects/ankictl/output/"

def save_collection_css():
    collection = mw.pm.name
    models = mw.col.models.all()
    for model in models:
        metadata = {}
        # Create folder for model
        name = model["name"]
        # Forward slashes mess up file paths
        clean_name = name.replace("/", "|")
        # Ex: output/M2/Cloze-AQ/
        dirpath = os.path.join(OUTPUT_DIR, collection, clean_name)
        os.makedirs(dirpath, exist_ok=True)
        metadata["name"] = name
        # Save css
        css = model["css"] + "\n"
        with open(os.path.join(dirpath, "index.css"), "w") as f:
            f.write(css)
        templates = model["tmpls"]
        for template in templates:
            tmpl_name = template["name"]
            question = template["qfmt"] + "\n"
            answer = template["afmt"] + "\n"
            tmpl_path = os.path.join(dirpath, tmpl_name.replace("/", "|"))
            os.makedirs(tmpl_path, exist_ok=True)
            # Templates are similar enough to mustache format
            with open(os.path.join(tmpl_path, "question.mustache"), "w") as f:
                f.write(question)
            with open(os.path.join(tmpl_path, "answer.mustache"), "w") as f:
                f.write(answer)
        metadata["card_count"] = len(templates)
        # Save metadata
        with open(os.path.join(dirpath, "meta.json"), "w") as f:
            f.write(json.dumps(metadata))
    # TODO: Save Anki addon config
    tooltip("Saved {} models to {}".format(len(models), OUTPUT_DIR))


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

if __name__ != '__main__':
    eaction = QAction("Export styles from Anki", mw)
    eaction.triggered.connect(save_collection_css)
    mw.form.menuTools.addAction(eaction)
    # iaction = QAction("Import styles into Anki", mw)
    # iaction.triggered.connect(push_collection_css)
    # mw.form.menuTools.addAction(iaction)
