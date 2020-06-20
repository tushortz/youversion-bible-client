from youversion.bible import Bible
import os
import json
import time
import random

books = []
data = []

b = Bible("kareem_taiwo", "Victoria1.")

BASE_DIR = "_notes"

if not os.path.exists(BASE_DIR):
    os.mkdir(BASE_DIR)

def _save_as_json(page):
    path = (f"{BASE_DIR}/{page}.json")
    result = b.notes(page)
    
    if type(result) == dict and result.get("error"):
        return False

    with open(path, "w") as f:
        f.write(json.dumps(result))
        print(f"page {page} complete ...")

    return len(result) > 0

def save_as_json(index=1):
    has_data = True
    BASE_DIR = "_notes"

    while has_data:
        if _save_as_json(index):
            index += 1
            time.sleep(random.randint(1, 3))
        else:
            has_data = False