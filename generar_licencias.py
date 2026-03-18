import random
import string
import json
import os

def generate_key():
    parts = []
    for _ in range(4):
        parts.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=4)))
    return f"YKZ-{''.join(parts[0])}-{''.join(parts[1])}-{''.join(parts[2])}"

def main():
    keys = []
    for _ in range(300):
        keys.append(generate_key())
    
    # Save to a text file for the user to see easily
    with open("licencias_generadas.txt", "w") as f:
        for key in keys:
            f.write(f"{key}\n")
            
    # Save to a JSON for the backend/system
    with open("licencias.json", "w") as f:
        json.dump({"keys": keys, "used_keys": {}}, f, indent=4)

    print(f"Se han generado 300 licencias en licencias_generadas.txt y licencias.json")

if __name__ == "__main__":
    main()
