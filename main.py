import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("lift_log.json")

def load_log():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Corrupt log file—starting fresh.")
    return []

def save_log(log):
    with open(DATA_FILE, "w") as f:
        json.dump(log, f, indent=2)

def add_lift(log, exercise, weight, reps, sets, note=""):
    entry = {
        "date": str(date.today()),
        "exercise": exercise.strip(),
        "weight": int(weight),
        "reps": int(reps),
        "sets": int(sets),
        "note": note.strip(),
    }
    log.append(entry)
    save_log(log)
    print(f"✅ Added: {exercise} — {weight} lbs x {reps} reps x {sets} sets")

def list_lifts(log):
    if not log:
        print("No lifts yet. Add one!")
        return
    for i, lift in enumerate(log, 1):
        note = f" | {lift['note']}" if lift.get("note") else ""
        print(f"{i}. [{lift['date']}] {lift['exercise']} — {lift['weight']} lbs x {lift['reps']} x {lift['sets']}{note}")

def delete_lift(log, index):
    i = index - 1
    if 0 <= i < len(log):
        removed = log.pop(i)
        save_log(log)
        print(f"🗑️ Deleted: {removed['exercise']} from {removed['date']}")
    else:
        print("Invalid index.")

def prompt_int(msg):
    while True:
        val = input(msg).strip()
        if val.isdigit():
            return int(val)
        print("Enter a number.")

def main():
    log = load_log()
    while True:
        print("\n1) Add lift  2) Show log  3) Delete  4) Today  5) PR  6) Quit")
        choice = input("Choose: ").strip()
        
        if choice == "1":
            exercise = input("Exercise: ")
            weight = prompt_int("Weight (lbs): ")
            reps   = prompt_int("Reps: ")
            sets   = prompt_int("Sets: ")
            note   = input("Note (optional): ")
            add_lift(log, exercise, weight, reps, sets, note)
        elif choice == "2":
            list_lifts(log)
        elif choice == "3":
            list_lifts(log)
            if log:
                idx = prompt_int("Delete which #? ")
                delete_lift(log, idx)
        elif choice == "4":
            day = today_str()
            list_lifts_for(log, day)
            stats_for(log, day)
        elif choice == "5":
            name = input("Exercise name for PR: ")
            pr_by_exercise(log, name)
        elif choice == "6":
            print("Saved. Bye!")
            break
        else:
            print("Invalid choice.")


from datetime import date

def today_str():
    return str(date.today())

def list_lifts_for(log, day):
    items = [l for l in log if l.get("date") == day]
    if not items:
        print(f"No lifts for {day}.")
        return
    for i, lift in enumerate(items, 1):
        note = f" | {lift['note']}" if lift.get("note") else ""
        print(f"{i}. [{lift['date']}] {lift['exercise']} — {lift['weight']} lbs x {lift['reps']} x {lift['sets']}{note}")

def stats_for(log, day):
    items = [l for l in log if l.get("date") == day]
    total_sets = sum(l["sets"] for l in items)
    total_reps = sum(l["reps"] * l["sets"] for l in items)
    total_volume = sum(l["weight"] * l["reps"] * l["sets"] for l in items)
    print(f"\nStats for {day}:")
    print(f"- Total sets:   {total_sets}")
    print(f"- Total reps:   {total_reps}")
    print(f"- Total volume: {total_volume} lb-reps")

def pr_by_exercise(log, exercise_name):
    ex = exercise_name.strip().lower()
    lifts = [l for l in log if l["exercise"].strip().lower() == ex]
    if not lifts:
        print(f"No entries for '{exercise_name}'.")
        return
    # Best by weight; if tie, pick higher total reps*sets
    best = max(lifts, key=lambda l: (l["weight"], l["reps"] * l["sets"]))
    print(f"🏆 PR for {exercise_name}: {best['weight']} lbs — {best['reps']} x {best['sets']} on {best['date']}")



if __name__ == "__main__":
    main()
