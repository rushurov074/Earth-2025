import random
import sys
import time

def type_out(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # for newline at the end

type_out("\n\nWelcome to Earth 2025\n\n")
type_out("Hello, Worker Number 472, welcome to Earth. Recently, the Earth has experienced a tragic fallout that caused millions of people to turn into radioactive 'doppelgangers' with a contagious illness that could kill the rest of the population. Our job at the US Agency of Doppelganger Containment or USDC, is to help survivors and identify doppelgangers and treat them in the containment unit. You have been given a manual that you can use to identify doppelgangers that you may access any time. You start directly after the briefing.\n\n")
type_out("Answer in lowercase only.\n")

name = input("What is your name, Worker 472?\n")
type_out(f"\nWelcome {name}, please take your USDC Manual")
type_out("You have received your USDC Manual!\n")

manual = "Normal ranges: Temperature 96–100°F, BP < 120, Heart Rate 60–100 bpm, Breathing 12–20."

# -----------------
# Names
# -----------------
first_names = ["John", "Sarah", "Alex", "Emily", "Marcus", "Lila", "Owen", "Sophia", "Daniel", "Maya"]
last_names = ["Carter", "Nguyen", "Patel", "Garcia", "Smith", "Khan", "Ivanov", "Silva", "Brown", "Lee"]

# -----------------
# Difficulty system
# -----------------
difficulty = input("Choose difficulty (easy / normal / hard): ").lower()

if difficulty == "easy":
    doppel_chance = 0.3
    temp_range = (80, 150)
    hr_low, hr_high = (40, 55), (120, 160)
    doppel_dialogue = [
        "I am normal human person. Please let me in.",
        "Greetings, worker. I am safe survivor.",
        "I am breathing correctly. Yes. Correctly.",
        "I feel fine. Blood pressure normal. Trust me.",
        "Let me inside. I am… *clearly* normal."
    ]
elif difficulty == "hard":
    doppel_chance = 0.7
    temp_range = (99, 102)
    hr_low, hr_high = (55, 59), (101, 110)
    doppel_dialogue = [
        "I haven’t eaten in days… my veins itch.",
        "I just need to rest. Don’t you ever feel… strange?",
        "Everything is normal. Perfectly normal.",
        "Sometimes my heart skips… but that’s fine, right?",
        "Please… I belong inside. Don’t look too close."
    ]
else:  # normal
    doppel_chance = 0.5
    temp_range = (97, 105)
    hr_low, hr_high = (50, 59), (105, 120)
    doppel_dialogue = [
        "The air tastes like copper today… doesn’t it?",
        "My skin feels loose, but I am fine. Normal.",
        "I had a dream my bones melted… but I woke up fine.",
        "I am healthy. Very healthy. Perfectly human.",
        "Your eyes are beautiful. I would like to wear them."
    ]

normal_dialogue = [
    "I’m so glad to be alive… thank you for keeping us safe.",
    "It’s been so hard out there. Please, let me in.",
    "I don’t feel well, but I’m human, I swear.",
    "Please, my family is inside. I need to see them.",
    "I’ve followed every rule. Don’t let me die out here."
]

# -----------------
# Expected patients generator
# -----------------
def generate_expected_list():
    new_expected = []
    for _ in range(random.randint(3, 6)):  # 3–6 survivors per day
        full_name = random.choice(first_names) + " " + random.choice(last_names)
        patient_id = f"{random.choice('ABCD')}{random.randint(100,999)}"
        new_expected.append({"name": full_name, "id": patient_id})
    return new_expected

# -----------------
# Patient generator
# -----------------
def generate_patient(expected_patients):
    # 30% chance a Doppelganger impersonates someone on the list
    impersonate = random.random() < 0.3 and expected_patients

    if impersonate:  # Doppelganger steals identity
        chosen = random.choice(expected_patients)
        full_name, patient_id = chosen["name"], chosen["id"]
        status = "Doppelganger"
        is_expected = True  # looks expected, but vitals will give them away
    else:
        full_name = random.choice(first_names) + " " + random.choice(last_names)
        patient_id = f"{random.choice('ABCD')}{random.randint(100,999)}"
        is_doppel = random.random() < doppel_chance
        status = "Doppelganger" if is_doppel else "Normal"
        is_expected = False
        if status == "Normal":
            for p in expected_patients:
                if p["name"] == full_name and p["id"] == patient_id:
                    is_expected = True
                    break

    if status == "Normal":
        vitals = {
            "Heart Rate (bpm)": random.randint(60, 100),
            "Blood Pressure": random.randint(100, 119),
            "Respiratory Rate": random.randint(12, 20),
            "Temperature (°F)": round(random.uniform(96.0, 100.0), 1),
        }
        dialogue = random.choice(normal_dialogue)
    else:  # Doppelganger
        vitals = {
            "Heart Rate (bpm)": random.choice([random.randint(*hr_low), random.randint(*hr_high)]),
            "Blood Pressure": random.choice([random.randint(70, 90), random.randint(130, 200)]),
            "Respiratory Rate": random.choice([random.randint(6, 10), random.randint(25, 40)]),
            "Temperature (°F)": round(random.uniform(*temp_range), 1),
        }
        dialogue = random.choice(doppel_dialogue)

    return full_name, patient_id, status, vitals, dialogue, is_expected

# -----------------
# Game loop
# -----------------
score = 0
strikes = 0
max_strikes = 3
day = 1
patient_number = 1

expected_patients = generate_expected_list()
type_out(f"\nExpected patients for Day {day}:")
for p in expected_patients:
    type_out(f"Name: {p['name']}, ID: {p['id']}")

new_patient_needed = True

while True:
    if new_patient_needed:
        type_out(f"\n--- Patient {patient_number} incoming (Day {day}) ---\n")
        type_out(manual + "\n")

        name, patient_id, status, vitals, dialogue, is_expected = generate_patient(expected_patients)
        type_out(f"Patient Name: {name}")
        type_out(f"Patient ID: {patient_id}")
        type_out(f"Patient says: \"{dialogue}\"")
        type_out("\n--- VITALS ---")
        for k, v in vitals.items():
            type_out(f"{k}: {v}")

        new_patient_needed = False

    action = input("\nChoose an action:\n"
                   "1. Read Manual\n"
                   "2. Send Patient to Quarantine\n"
                   "3. Send Patient to Normal Reserve\n"
                   "4. End Shift\n"
                   "5. View Expected Patients\n> ")

    if action == "1":
        type_out("\nManual: Temperature 96–100°F, BP < 120, Breathing 12–20, Heart Rate 60–100 bpm.\n")
        action = input("Now choose:\n2. Quarantine\n3. Normal Reserve\n4. End Shift\n> ")

    if action == "2":  # quarantine
        if status == "Doppelganger":
            q = input("Are you sure? (yes/no): ")
            if q == "yes":
                score += 1
            else:
                strikes += 1
        else:
            strikes += 1
        new_patient_needed = True
        patient_number += 1

    elif action == "3":  # normal reserve
        if status == "Doppelganger":
            strikes += 1
        elif status == "Normal" and is_expected:
            score += 1
            # Remove patient from expected_patients after correct identification
            for p in expected_patients:
                if p["name"] == name and p["id"] == patient_id:
                    expected_patients.remove(p)
                    break
        # Normal patient not on the list: accepted without penalty (no strike, no score)
        new_patient_needed = True
        patient_number += 1

    elif action == "4":  # end game
        type_out(f"\nShift ended. Final Score: {score}. Strikes: {strikes}/{max_strikes}")
        break

    elif action == "5":  # view expected list
        type_out(f"\nExpected patients for Day {day}:")
        for p in expected_patients:
            type_out(f"Name: {p['name']}, ID: {p['id']}")
        continue

    else:
        type_out("Invalid choice. Please try again.")

    if strikes >= max_strikes:
        type_out(f"\nYou have reached {strikes} strikes. You are fired from the USDC.\n")
        type_out(f"Final Score: {score}")
        break

    if not expected_patients:
        type_out(f"\nAll expected survivors processed for Day {day}.")
        day += 1
        expected_patients = generate_expected_list()
        type_out(f"\nExpected patients for Day {day}:")
        for p in expected_patients:
            type_out(f"Name: {p['name']}, ID: {p['id']}")
        patient_number = 1
        new_patient_needed = True