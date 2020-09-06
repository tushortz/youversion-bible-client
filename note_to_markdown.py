from youversion.bible import Bible
import os
import json
import time
import random
import re


HEADER = """
---
title: "{0}"
date: {1}
book: {2}
draft: false
---
"""

template = """
## {0}

{1}

**Related verses**: {2}. See [notes](https://my.bible.com/notes/{3})

"""

has_data = True
index = 1

USERNAME = os.getenv("BIBLE_USERNAME")
PASSWORD = os.getenv("BIBLE_PASSWORD")

b = Bible(USERNAME, PASSWORD)

while has_data:
    notes = b.notes(index)

    if type(notes) == dict and notes.get("error"):
        has_data = False
        
    for note in notes:
        _obj = note["object"]
        text = _obj["content"]
        dt = _obj.get("updated_dt") or _obj.get("created_dt")
        dt = re.sub(r'\.\d+', " ", dt).replace("T", " ")

        id = _obj.get("id")
        
        _refs = _obj.get("references")
        locs = []

        human_references = []
        for ref in _refs:
            human_references.append(ref["human"])
            locs += ref["usfm"]

        locs = set(locs)
        human_references = ", ".join(human_references)
        # quit()
        for loc in locs:
            book, chapter, verse = loc.split(".")
            folder = f"notes/{book.lower()}"

            if not os.path.exists(folder):
                os.makedirs(folder)

            md_file = f"{folder}/{chapter}.md"
            mode = "w"
            HEAD = HEADER.format(f"{book} {chapter}", dt, book)
            
            content = ""
            if os.path.exists(md_file):
                f = open(md_file, "r")
                content = f.read()
                f.close()
                mode = "a"

                if "draft: true" in content or "draft: false" in content:
                    HEAD = ""

            with open(md_file, mode, encoding="ascii", errors='replace') as f:
                f.write(HEAD)
                
                if id in content:
                    print(f"Skipping note with id: {id} in {loc}")
                else:
                    f.write(template.format(
                        f"{book} {chapter}:{verse}", 
                        text,
                        human_references, id, 
                        dt
                    ))

    print(f"Page {index} complete")
    index += 1
