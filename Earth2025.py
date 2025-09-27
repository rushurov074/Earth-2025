import random

print("\n\nWelcome to Earth 2025\n\n")
print("Hello, Worker Number 472, welcome to Earth. Recently, the Earth has experienced a tragic fallout that caused millions of people to turn into radioactive 'doppelgangers' with a contagious illness that could kill the rest of the population. Our job at the US Agency of Doppelganger Containment or USDC, is to help survivors and identify doppelgangers and treat them in the containment unit. You have been given a manual that you can use to identify doppelgangers that you may access any time. You start directly after the breiefing.\n\n")
print("Your job at the US Agency of Doppelganger Containment (USDC) is to identify survivors and doppelgangers.\n")
print("Answer in lowercase only.\n")

name = input("What is your name, Worker 472?\n")

print(f"\nWelcome {name}, please take your USDC Manual")
print("You have recieved your USDC Manual!")
print("Your manual will be shown every time a patient enters. Oh look! One is coming now.\n")

manual = "Normal ranges: Temperature 96–100°F, BP < 120, Heart Rate 60–100 bpm, Breathing 12–20."


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
else:  # default = normal
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


# -----------------
# Patient generator
# -----------------
first_names = ["John", "Sarah", "Alex", "Emily", "Marcus", "Lila", "Owen", "Sophia", "Daniel", "Maya"]
last_names = ["Carter", "Nguyen", "Patel", "Garcia", "Smith", "Khan", "Ivanov", "Silva", "Brown", "Lee"]

normal_dialogue = [
    "I’m so glad to be alive… thank you for keeping us safe.",
    "It’s been so hard out there. Please, let me in.",
    "I don’t feel well, but I’m human, I swear.",
    "Please, my family is inside. I need to see them.",
    "I’ve followed every rule. Don’t let me die out here."
]


def generate_patient():
    full_name = random.choice(first_names) + " " + random.choice(last_names)
    is_doppel = random.random() < doppel_chance
    status = "Doppelganger" if is_doppel else "Normal"

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

    return full_name, status, vitals, dialogue


# -----------------
# Game loop
# -----------------
score = 0
strikes = 0
max_strikes = 3
patient_number = 1

while True:
    print(f"\n--- Patient {patient_number} incoming ---\n")
    print(manual + "\n")  # manual always shown for reference

    name, status, vitals, dialogue = generate_patient()
    print(f"Patient Name: {name}")
    print(f"Patient says: \"{dialogue}\"")
    print("\n--- VITALS ---")
    for k, v in vitals.items():
        print(f"{k}: {v}")

    action = input("\nChoose an action:\n"
                   "1. Read Manual\n"
                   "2. Send Patient to Quarantine\n"
                   "3. Send Patient to Normal Reserve\n"
                   "4. End Shift\n> ")

    if action == "1":
        print("\nManual: Temperature 96–100°F, BP < 120, Breathing 12–20, Heart Rate 60–100 bpm.\n")
        action = input("Now choose:\n2. Quarantine\n3. Normal Reserve\n4. End Shift\n> ")

    if action == "2":  # player chose quarantine
        if status == "Doppelganger":
            q = input("Are you sure? (yes/no): ")
            if q == "yes":
                score += 1
            else:
                strikes += 1
        else:
            strikes += 1

    elif action == "3":  # player chose normal reserve
        if status == "Normal":
            score += 1
        else:
            strikes += 1

    elif action == "4":  # quit the game
        print(f"\nShift ended. Final Score: {score} patients correctly identified. Strikes: {strikes}/{max_strikes}")
        break

    else:
        print("Invalid choice. Please try again.")

    # check if player is fired
    if strikes >= max_strikes:
        print(f"\nYou have reached {strikes} strikes. You are fired from the USDC.\n")
        print(f"Final Score: {score} patients correctly identified.")
        break

    patient_number += 1
