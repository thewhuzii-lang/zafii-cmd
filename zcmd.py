#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import time

BASE = os.path.expanduser("~/.zafii_cmd")
DB = os.path.join(BASE, "commands.json")
SETTINGS = os.path.join(BASE, "settings.json")

os.makedirs(BASE, exist_ok=True)

RESET = "\033[0m"
COLORS = {
    "cyan": "\033[96m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "magenta": "\033[95m",
    "blue": "\033[94m",
    "white": "\033[97m"
}

def load():
    if not os.path.exists(DB):
        return {}
    try:
        with open(DB, "r") as f:
            return json.load(f)
    except:
        return {}

def save(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=2)

def settings():
    if not os.path.exists(SETTINGS):
        return {"theme": "cyan"}
    try:
        with open(SETTINGS, "r") as f:
            return json.load(f)
    except:
        return {"theme": "cyan"}

def save_settings(data):
    with open(SETTINGS, "w") as f:
        json.dump(data, f, indent=2)

def color():
    return COLORS.get(settings().get("theme", "cyan"), COLORS["cyan"])

def pause():
    input("\nPress Enter to continue...")

def clear():
    os.system("clear")

def banner():
    clear()
    c = color()

    print(c + """
╔══════════════════════════════════════╗
║        ⚡ ZAFII COMMAND LAB          ║
║              Version 2.0             ║
║            Created by Zafii          ║
╠══════════════════════════════════════╣
║  1.  ➕ Create Command               ║
║  2.  📦 My Commands                  ║
║  3.  🔍 Search                       ║
║  4.  ✏️  Edit Command                ║
║  5.  🗑️  Delete Command              ║
║  6.  ⭐ Favorites                    ║
║  7.  📂 Categories                   ║
║  8.  📤 Export Pack                  ║
║  9.  📥 Import Pack                  ║
║ 10.  📊 Statistics                   ║
║ 11.  🧪 Test Command                 ║
║ 12.  🎨 Theme                        ║
║ 13.  ℹ️  About Zafii-CMD             ║
║ 14.  🚪 Exit                         ║
╚══════════════════════════════════════╝
""" + RESET)

def create():
    data = load()

    name = input("Command name: ").strip()

    if not name:
        print("Name required.")
        pause()
        return

    if name in data:
        print("Command already exists.")
        pause()
        return

    command = input("Command to run: ").strip()

    if not command:
        print("Command required.")
        pause()
        return

    category = input("Category [General]: ").strip() or "General"

    data[name] = {
        "command": command,
        "category": category,
        "uses": 0,
        "favorite": False,
        "created": time.strftime("%Y-%m-%d %H:%M")
    }

    save(data)

    print(f"\n✓ {name} created!")
    pause()

def listing():
    data = load()

    print("\n📦 MY COMMANDS\n")

    if not data:
        print("No commands yet.")
    else:
        for name, info in data.items():
            star = "⭐" if info.get("favorite", False) else " "
            cat = info.get("category", "General")
            print(f"{star} {name} [{cat}] → {info['command']}")

    pause()

def search():
    data = load()
    q = input("Search: ").lower().strip()

    print()

    found = False

    for name, info in data.items():
        text = name + " " + info["command"] + " " + info.get("category", "")
        if q in text.lower():
            print(f"• {name} → {info['command']}")
            found = True

    if not found:
        print("No match found.")

    pause()

def edit():
    data = load()
    name = input("Command to edit: ").strip()

    if name not in data:
        print("Command not found.")
        pause()
        return

    print("\nCurrent command:")
    print(data[name]["command"])

    new = input("\nNew command [Enter = keep]: ").strip()
    cat = input("New category [Enter = keep]: ").strip()

    if new:
        data[name]["command"] = new

    if cat:
        data[name]["category"] = cat

    save(data)

    print("✓ Updated!")
    pause()

def delete():
    data = load()
    name = input("Command to delete: ").strip()

    if name not in data:
        print("Command not found.")
        pause()
        return

    if input(f"Delete {name}? [y/N]: ").lower() == "y":
        del data[name]
        save(data)
        print("✓ Deleted.")
    else:
        print("Cancelled.")

    pause()

def favorites():
    data = load()

    print("\n⭐ FAVORITES\n")

    for name, info in data.items():
        if info.get("favorite", False):
            print(f"⭐ {name} → {info['command']}")

    print("\nType a command name to toggle favorite.")
    name = input("Name [Enter = back]: ").strip()

    if name:
        if name in data:
            data[name]["favorite"] = not data[name].get("favorite", False)
            save(data)
            print("✓ Favorite updated.")
        else:
            print("Command not found.")

    pause()

def categories():
    data = load()
    cats = {}

    for name, info in data.items():
        cat = info.get("category", "General")
        cats.setdefault(cat, []).append(name)

    print("\n📂 CATEGORIES\n")

    if not cats:
        print("No commands yet.")
    else:
        for cat, names in cats.items():
            print(f"\n[{cat}]")
            for name in names:
                print(f"  • {name}")

    pause()

def export_pack():
    data = load()
    path = os.path.expanduser("~/zafii_commands.zpack")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print("\n✓ Export complete!")
    print(path)
    pause()

def import_pack():
    path = os.path.expanduser(input("Path to .zpack: ").strip())

    if not os.path.exists(path):
        print("File not found.")
        pause()
        return

    try:
        with open(path, "r") as f:
            incoming = json.load(f)

        data = load()
        data.update(incoming)
        save(data)

        print("✓ Import complete!")
    except:
        print("Invalid command pack.")

    pause()

def statistics():
    data = load()

    total = len(data)
    runs = sum(x.get("uses", 0) for x in data.values())
    favs = sum(1 for x in data.values() if x.get("favorite", False))

    print("\n📊 ZAFII-CMD STATISTICS\n")
    print("Commands :", total)
    print("Runs     :", runs)
    print("Favorites:", favs)

    if data:
        top = max(data.items(), key=lambda x: x[1].get("uses", 0))
        print("Most used:", top[0])

    pause()

def test():
    data = load()
    name = input("Command to test: ").strip()

    if name not in data:
        print("Command not found.")
        pause()
        return

    print("\n🧪 DRY RUN")
    print("Command:")
    print(data[name]["command"])
    print("\n✓ Nothing was executed.")

    pause()

def execute(name):
    data = load()

    if name not in data:
        print(f"❌ Command '{name}' not found.")
        return

    command = data[name]["command"]

    print(f"⚡ Running: {command}\n")

    data[name]["uses"] = data[name].get("uses", 0) + 1
    save(data)

    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        print("Error:", e)

def theme():
    s = settings()

    print("""
🎨 THEMES

1. Cyan
2. Green
3. Yellow
4. Magenta
5. Blue
6. White
""")

    choices = {
        "1": "cyan",
        "2": "green",
        "3": "yellow",
        "4": "magenta",
        "5": "blue",
        "6": "white"
    }

    choice = input("Choose: ").strip()

    if choice in choices:
        s["theme"] = choices[choice]
        save_settings(s)
        print("✓ Theme saved permanently.")
    else:
        print("Invalid choice.")

    pause()

def about():
    clear()

    print("""
╔══════════════════════════════════╗
║          ⚡ ZAFII-CMD            ║
╠══════════════════════════════════╣
║ Version : 2.0                    ║
║ Creator : Zafii                  ║
║ Platform: Termux                 ║
║                                  ║
║ Personal Command Manager         ║
║                                  ║
║        CREATED BY ZAFII ⚡        ║
╚══════════════════════════════════╝
""")

    pause()

def easter_egg():
    clear()

    print("""
╔══════════════════════════════════╗
║                                  ║
║        ⚡ Z A F I I ⚡             ║
║                                  ║
║     You found the secret! 👀     ║
║                                  ║
║       ZAFII-CMD 2.0              ║
║       Created by Zafii            ║
║                                  ║
╚══════════════════════════════════╝
""")

    time.sleep(2)

def main():
    # Direct command / Pack system
    if len(sys.argv) > 1:
        name = sys.argv[1].lower()

        # 📦 ZAFII PACK SYSTEM
        if name in ["pack", "packs", "install"]:
            pack_script = os.path.expanduser("~/zcmd_pack.py")

            if os.path.exists(pack_script):
                subprocess.run(
                    ["python", pack_script] + sys.argv[1:]
                )
            else:
                print("❌ Pack system not found.")

            return

        # 🥚 Secret Easter Egg
        if name in ["zafii", "secret", "easteregg"]:
            easter_egg()
            return

        # ⚡ Direct custom command
        execute(sys.argv[1])
        return

    while True:
        banner()

        choice = input("Select ➜ ").strip()

        if choice == "1":
            create()
        elif choice == "2":
            listing()
        elif choice == "3":
            search()
        elif choice == "4":
            edit()
        elif choice == "5":
            delete()
        elif choice == "6":
            favorites()
        elif choice == "7":
            categories()
        elif choice == "8":
            export_pack()
        elif choice == "9":
            import_pack()
        elif choice == "10":
            statistics()
        elif choice == "11":
            test()
        elif choice == "12":
            theme()
        elif choice == "13":
            about()
        elif choice == "14":
            clear()
            print("⚡ ZAFII-CMD closed.")
            print("Created by Zafii ❤️")
            break
        else:
            print("Invalid option.")
            time.sleep(1)

if __name__ == "__main__":
    main()
