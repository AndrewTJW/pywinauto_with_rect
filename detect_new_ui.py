#script to run to take new UI snapshot
#run when want to scan new UI 
import json
from pathlib import Path
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.timings import TimeoutError
from pywinauto.application import ProcessNotFoundError
import psutil

#function to find PID from app path
def find_pid_by_path(app_path):
    for p in psutil.process_iter(["pid", "exe"]):
        if p.info["exe"] and p.info["exe"].lower() == app_path.lower():
            return p.info["pid"]
    return None


def snapshot_app(app_path: str, out_dir: str = "outputs", backend: str = "uia", timeout: int = 15,):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    app = Application(backend=backend)

    #use Path library to dynamically state app directory
    app_pid = find_pid_by_path(app_path)
    # 1) Connect if already running, else start
    try:
        app.connect(process=app_pid)
    except (ElementNotFoundError, TimeoutError, ProcessNotFoundError):
        app.start(app_path)

    # 2) Get main window (kinda hard coded)
    dlg = app.window(title = "Test Automation - Untitled")

    #wait until the app is visible, means opened 
    dlg.wait("visible", timeout=timeout)


    # 3A) Human-readable snapshot (tree)
    txt_path = out / "new_snapshot.txt"
    dlg.print_control_identifiers(filename=str(txt_path))

    # 3B) Machine-readable snapshot (JSON)
    items = []
    for c in dlg.descendants():
        ei = c.element_info
        r = ei.rectangle
        items.append({
            "control_type": ei.control_type,
            "automation_id": ei.automation_id,
            "name": ei.name,
            "class_name": ei.class_name,
            "rect": [r.left, r.top, r.right, r.bottom],
        })

    json_path = out / "new_snapshot.json"
    json_path.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")

    return str(txt_path), str(json_path), len(items)


if __name__ == "__main__":
    # Example: Notepad
    app_path = r"C:\Program Files\Keysight\Test Automation\Editor.exe"

    txt_file, json_file, count = snapshot_app(app_path, out_dir="outputs")
    print("Saved:", txt_file)
    print("Saved:", json_file)
    print("Elements:", count)