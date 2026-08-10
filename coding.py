import os
import webbrowser
import re

# Engine State (Memory)
variables = {}

FULL_HELP_TEXT = """
==================================================
        WELCOME TO YOUR LANGUAGE HELP GUIDE        
==================================================

(Note: All commands are CASE-INSENSITIVE!)

1. VARIABLES & PRINTING:
   "Thomas" = "h"          -> Saves "Thomas" inside variable "h"
   SHOW "h"                -> Prints whatever is stored inside "h"

2. RUNNING SCRIPTS / FILES:
   RUN "test.txt"          -> Runs all code lines saved in a file

3. SYSTEM COMMANDS:
   /HELP                  -> Shows this manual
   /RESET                 -> Asks for confirmation to clear memory & screen
   /EXIT                  -> Quits the interpreter
==================================================
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def evaluate_math(expression):
    try:
        allowed_chars = "0123456789+-*/(). "
        if all(char in allowed_chars for char in expression):
            return eval(expression)
    except Exception:
        pass
    return None

def process_command(raw_input):
    global variables
    line = raw_input.strip()
    cmd = line.lower()

    if not line:
        return

    # System Commands
    if cmd == "/exit":
        print("Exiting language engine...")
        return "EXIT"

    elif cmd == "/help":
        print(FULL_HELP_TEXT)

    elif cmd == "/reset":
        confirm = input("Are you sure that you want to erase everything? (yes/no): ").lower().strip()
        if confirm in ["yes", "y"]:
            variables.clear()
            clear_screen()
            print("==================================================")
            print("     WELCOME TO YOUR PROGRAMMING LANGUAGE v1.0    ")
            print("==================================================")
            print("Type /help to get the help menu.")
            print("Type /exit to quit.")
            print("--------------------------------------------------\n")
            print(">> Memory and screen cleared!\n")
        else:
            print(">> Reset canceled. Your variables are safe.")

    # 1. RUN FILE COMMAND (Multi-Line Scripts)
    elif cmd.startswith("run"):
        filename = line[3:].strip().strip('"')
        run_file(filename)

    # 2. Web Integration
    elif cmd.startswith("insert"):
        url = line[6:].strip().strip('"')
        print(f">> [ACTION] Opening website: {url}")
        webbrowser.open(url)

    # 3. Printing & Math Evaluation
    elif cmd.startswith("show"):
        content = line[4:].strip()
        
        math_result = evaluate_math(content)
        if math_result is not None:
            print(f">> Output: {math_result}")
        elif content in variables:
            print(f">> Output: {variables[content]}")
        else:
            print(f">> Output: {content.strip('"')}")

    # 4. Variable Assignment ("Thomas" = "h")
    elif "=" in line and not cmd.startswith("when") and not "speed" in cmd and not "shape" in cmd:
        parts = line.split("=")
        val = parts[0].strip().strip('"')
        var = parts[1].strip().strip('"')
        variables[var] = val
        print(f">> [MEMORY] Saved '{val}' to variable '{var}'")

    # 5. Natural Language Intent Fallback
    else:
        print(f">> [NATURAL LANGUAGE] Processed intent for: '{line}'")

def run_file(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            print(f">> [FILE ENGINE] Running script: '{file_path}'...\n")
            for raw_line in lines:
                # Runs each line through the exact same engine!
                process_command(raw_line)
            print(f"\n>> [FILE ENGINE] Finished executing '{file_path}'.")
    except FileNotFoundError:
        print(f">> [ERROR] Could not find file named '{file_path}'. Make sure it's saved in Pydroid!")

# --- ENGINE STARTUP ---
clear_screen()
print("==================================================")
print("     WELCOME TO YOUR PROGRAMMING LANGUAGE v1.0    ")
print("==================================================")
print("Type /help to get the help menu.")
print("Type /exit to quit.")
print("--------------------------------------------------\n")

while True:
    user_input = input("Your Language > ")
    status = process_command(user_input)
    if status == "EXIT":
        break
