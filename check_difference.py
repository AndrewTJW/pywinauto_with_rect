import json
from pathlib import Path

BASE_DIR = Path("outputs")

BASELINE = BASE_DIR / "snapshot.json" #the previous version UI
NEW_SNAPSHOT = BASE_DIR / "new_snapshot.json" #the new version UI
SAME_FILE = BASE_DIR / "same.json" 
NEW_ONLY_FILE = BASE_DIR / "new_only.json"


#function to load json file read the old snapshot and new_snapshot
def load(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write(path: Path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def canonical(obj): #receives an object such as {"control_type": ..., "automation_id": ..., ..}
    return json.dumps(obj, sort_keys=True)


def compute_same(baseline, new_snapshot):
    set_base = {canonical(o) for o in baseline} #for every object in baseline, apply lambda function canonical(o) then wrap it in an object
    set_new = {canonical(o) for o in new_snapshot}
    same = set_base & set_new
    return [json.loads(s) for s in same] #for each element in same load it into the json structure inside a list


#get the new list of UI by comparing the json objects inside new_snapshot.json | same.json
def compute_new_only(new_snapshot, same):
    set_new = {canonical(o) for o in new_snapshot} #convert json object into string 
    set_same = {canonical(o) for o in same}
    diff = set_new - set_same
    return [json.loads(s) for s in diff]


def main():
    baseline = load(BASELINE)
    new_snapshot = load(NEW_SNAPSHOT)

    same = compute_same(baseline, new_snapshot)
    write(SAME_FILE, same)

    # Step 2: compute new-only elements
    new_only = compute_new_only(new_snapshot, same)
    write(NEW_ONLY_FILE, new_only)

    print("Baseline elements:", len(baseline))
    print("New snapshot elements:", len(new_snapshot))
    print("Same elements:", len(same))
    print("New / changed elements:", len(new_only))
    print("Saved:", NEW_ONLY_FILE)


if __name__ == "__main__":
    main()
