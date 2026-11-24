import json
import os
import sys

MAX_CHARS = 200
LABEL = "vending-pickup"
SLUG = "u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee"


def load_line():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.txt"), "r", encoding="utf-8") as fh:
        body = fh.read().strip()
    if len(body) < 1 or len(body) > MAX_CHARS:
        sys.stderr.write("line length out of gate range\n")
        raise SystemExit(0)
    return body


def emit(body):
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body + "\n")
    with open(target, "r", encoding="utf-8") as fh:
        if fh.read().strip() != body:
            raise RuntimeError("round trip failed")
    return target


def report(target, body):
    print(json.dumps({"status": "ok", "label": LABEL, "bytes": len(body.encode("utf-8")), "wrote": target, "slug": SLUG}))


def run():
    body = load_line()
    target = emit(body)
    report(target, body)


run()
