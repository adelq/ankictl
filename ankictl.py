import os
import sys
import json
import sqlite3
import difflib

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
        css = model["css"]
        with open(os.path.join(dirpath, "index.css"), "w") as f:
            f.write(css)
        templates = model["tmpls"]
        for template in templates:
            tmpl_name = template["name"]
            question = template["qfmt"]
            answer = template["afmt"]
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


def push_collection_css():
    collection = mw.pm.name
    models = mw.col.models.all()
    for model in models:
        # Get directory for each model
        # Ex: output/M2/Cloze-AQ/
        name = model["name"]
        mw.col.log("Working on %s" % name)
        # Forward slashes mess up file paths
        clean_name = name.replace("/", "|")
        dirpath = os.path.join(OUTPUT_DIR, collection, clean_name)
        assert os.path.isdir(dirpath)
        # Read CSS
        with open(os.path.join(dirpath, "index.css"), "r") as f:
            css = f.read()
        # Update CSS
        model["css"] = css
        # Now same for each HTML-ish template
        templates = model["tmpls"]
        for template in templates:
            tmpl_name = template["name"]
            tmpl_path = os.path.join(dirpath, tmpl_name.replace("/", "|"))
            # Read templates
            with open(os.path.join(tmpl_path, "question.mustache"), "r") as f:
                question = f.read()
            with open(os.path.join(tmpl_path, "answer.mustache"), "r") as f:
                answer = f.read()
            template["qfmt"] = question
            template["afmt"] = answer
        # Write changes
        mw.col.models.update(model)
    tooltip("Updated {} models".format(len(models)))

if __name__ != '__main__':
    eaction = QAction("Export styles from Anki", mw)
    eaction.triggered.connect(save_collection_css)
    mw.form.menuTools.addAction(eaction)
    iaction = QAction("Import styles into Anki", mw)
    iaction.triggered.connect(push_collection_css)
    mw.form.menuTools.addAction(iaction)
