import argparse
import json
import os
import datetime

DB_PATH = os.path.join("data", "lifts.json")

def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump([], f)

def _load():
    _ensure_db()
    with open(DB_PATH, "r") as f:
        try:
            return json.load(f)
        except ValueError:
            return []

def _save(rows):
    with open(DB_PATH, "w") as f:
        json.dump(rows, f, indent=2)

def cmd_add(args):
    rows = _load()
    entry = {
        "date": args.date or datetime.date.today().isoformat(),
        "exercise": args.exercise.strip(),
        "sets": int(args.sets),
        "reps": [int(x) for x in args.reps.split(",")] if args.reps else [],
        "weight": [float(x) for x in args.weight.split(",")] if args.weight else [],
        "notes": args.notes or ""
    }
    rows.append(entry)
    _save(rows)
    print("added: {} - {}".format(entry["date"], entry["exercise"]))

def cmd_list(args):
    rows = _load()
    if not rows:
        print("no entries yet.")
        return
    for r in rows:
        print("[{}] {} sets:{} reps:{} weight:{} notes:{}".format(
            r.get("date",""), r.get("exercise",""), r.get("sets",""),
            r.get("reps",""), r.get("weight",""), r.get("notes","")
        ))

def build_parser():
    p = argparse.ArgumentParser(description="Lift Log CLI")
    sub = p.add_subparsers(dest="cmd")

    add = sub.add_parser("add", help="add a lift")
    add.add_argument("--exercise", required=True)
    add.add_argument("--sets", required=True, type=int)
    add.add_argument("--reps")
    add.add_argument("--weight")
    add.add_argument("--date")
    add.add_argument("--notes")
    add.set_defaults(func=cmd_add)

    ls = sub.add_parser("list", help="list lifts")
    ls.set_defaults(func=cmd_list)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "func", None):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
