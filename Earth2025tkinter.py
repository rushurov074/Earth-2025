import random
import tkinter as tk
from tkinter import messagebox

# -----------------
# Names
# -----------------
first_names = ["John", "Sarah", "Alex", "Emily", "Marcus", "Lila", "Owen", "Sophia", "Daniel", "Maya"]
last_names = ["Carter", "Nguyen", "Patel", "Garcia", "Smith", "Khan", "Ivanov", "Silva", "Brown", "Lee"]

manual = "Normal ranges: Temperature 96–100°F, BP < 120, Heart Rate 60–100 bpm, Breathing 12–20."

# -----------------
# Difficulty system variables (to be set later)
# -----------------
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
# Main Application Class
# -----------------
class Earth2025App:
    def __init__(self, root):
        self.root = root
        self.root.title("Earth 2025 - USDC")

        self.score = 0
        self.strikes = 0
        self.max_strikes = 3
        self.day = 1
        self.patient_number = 1
        self.expected_patients = []
        self.new_patient_needed = True

        self.name = ""
        self.difficulty = ""
        self.patient_data = None  # tuple: name, id, status, vitals, dialogue, is_expected

        self.create_intro_screen()

    def create_intro_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        welcome_label = tk.Label(self.root, text="Welcome to Earth 2025", font=("Arial", 16, "bold"))
        welcome_label.pack(pady=10)

        intro_text = ("Hello, Worker Number 472, welcome to Earth. Recently, the Earth has experienced a tragic fallout "
                      "that caused millions of people to turn into radioactive 'doppelgangers' with a contagious illness "
                      "that could kill the rest of the population. Our job at the US Agency of Doppelganger Containment "
                      "or USDC, is to help survivors and identify doppelgangers and treat them in the containment unit.\n\n"
                      "You have been given a manual that you can use to identify doppelgangers that you may access any time. "
                      "You start directly after the briefing.\n\n"
                      "Answer in lowercase only.")

        intro_label = tk.Label(self.root, text=intro_text, wraplength=500, justify="left")
        intro_label.pack(padx=10, pady=10)

        name_frame = tk.Frame(self.root)
        name_frame.pack(pady=5)
        name_label = tk.Label(name_frame, text="What is your name, Worker 472?")
        name_label.pack(side="left")
        self.name_entry = tk.Entry(name_frame)
        self.name_entry.pack(side="left")

        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack(pady=5)
        difficulty_label = tk.Label(difficulty_frame, text="Choose difficulty:")
        difficulty_label.pack(side="left")
        self.difficulty_var = tk.StringVar(value="normal")
        difficulties = [("Easy", "easy"), ("Normal", "normal"), ("Hard", "hard")]
        for text, mode in difficulties:
            rb = tk.Radiobutton(difficulty_frame, text=text, variable=self.difficulty_var, value=mode)
            rb.pack(side="left")

        start_button = tk.Button(self.root, text="Start", command=self.start_game)
        start_button.pack(pady=10)

    def start_game(self):
        entered_name = self.name_entry.get().strip()
        if not entered_name:
            messagebox.showwarning("Input Error", "Please enter your name.")
            return
        self.name = entered_name

        self.difficulty = self.difficulty_var.get()
        self.set_difficulty_params()

        # Show manual screen
        self.show_manual_screen()

    def set_difficulty_params(self):
        global doppel_chance, temp_range, hr_low, hr_high, doppel_dialogue
        if self.difficulty == "easy":
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
        elif self.difficulty == "hard":
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

    def show_manual_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        welcome_label = tk.Label(self.root, text=f"Welcome {self.name}, please take your USDC Manual", font=("Arial", 14))
        welcome_label.pack(pady=10)

        manual_label = tk.Label(self.root, text=manual, wraplength=500, justify="left", font=("Arial", 12, "italic"))
        manual_label.pack(padx=10, pady=10)

        proceed_button = tk.Button(self.root, text="Proceed to Duty", command=self.start_day)
        proceed_button.pack(pady=10)

    def start_day(self):
        self.score = 0
        self.strikes = 0
        self.day = 1
        self.patient_number = 1
        self.expected_patients = generate_expected_list()
        self.new_patient_needed = True

        self.create_game_screen()

    def create_game_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Status label (hide score during gameplay)
        self.score_label = tk.Label(
            self.root,
            text=f"Strikes: {self.strikes}/{self.max_strikes} | Day: {self.day}",
            font=("Arial", 12, "bold")
        )
        self.score_label.pack(pady=5)

        # Expected patients list
        expected_frame = tk.Frame(self.root)
        expected_frame.pack(padx=10, pady=5, fill="x")
        expected_label = tk.Label(expected_frame, text=f"Expected patients for Day {self.day}:", font=("Arial", 12, "underline"))
        expected_label.pack(anchor="w")
        self.expected_listbox = tk.Listbox(expected_frame, height=6, width=50)
        self.expected_listbox.pack()
        self.update_expected_listbox()

        # Patient info display
        self.info_text = tk.Text(self.root, height=12, width=60, state="disabled", wrap="word")
        self.info_text.pack(padx=10, pady=10)

        # Vitals check buttons
        vitals_check_frame = tk.Frame(self.root)
        vitals_check_frame.pack(pady=5)
        self.vitals_to_check = [
            ("Heart Rate (bpm)", "Heart Rate"),
            ("Blood Pressure", "Blood Pressure"),
            ("Respiratory Rate", "Respiratory Rate"),
            ("Temperature (°F)", "Temperature"),
        ]
        self.vitals_checked = {}
        self.vital_buttons = {}
        for vital_key, vital_label in self.vitals_to_check:
            self.vitals_checked[vital_key] = False
            btn = tk.Button(
                vitals_check_frame,
                text=f"Check {vital_label}",
                command=lambda k=vital_key: self.mark_vital_checked(k)
            )
            btn.pack(side="left", padx=5)
            self.vital_buttons[vital_key] = btn

        # Buttons frame
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=5)

        self.button_quarantine = tk.Button(buttons_frame, text="Send to Quarantine", command=self.action_quarantine, state="disabled")
        self.button_quarantine.pack(side="left", padx=5)

        self.button_normal = tk.Button(buttons_frame, text="Send to Normal Reserve", command=self.action_normal, state="disabled")
        self.button_normal.pack(side="left", padx=5)

        self.button_view_manual = tk.Button(buttons_frame, text="View Manual", command=self.show_manual_popup)
        self.button_view_manual.pack(side="left", padx=5)

        self.button_next = tk.Button(buttons_frame, text="Next Patient", command=self.next_patient)
        self.button_next.pack(side="left", padx=5)

        self.button_end_shift = tk.Button(buttons_frame, text="End Shift", command=self.end_shift)
        self.button_end_shift.pack(side="left", padx=5)

        self.next_patient()

    # --- BEGIN: Move functions into Earth2025App ---
    def mark_vital_checked(self, vital_key):
        name, patient_id, status, vitals, dialogue, is_expected = self.patient_data

        # Reveal the vital
        self.info_text.config(state="normal")
        self.info_text.insert(tk.END, f"{vital_key}: {vitals[vital_key]}\n")
        self.info_text.config(state="disabled")

        # Mark as checked
        self.vitals_checked[vital_key] = True
        self.vital_buttons[vital_key].config(state="disabled", text=f"{self.vital_buttons[vital_key]['text']} ✓")

        # Enable decision buttons if all vitals checked
        if all(self.vitals_checked.values()):
            self.button_quarantine.config(state="normal")
            self.button_normal.config(state="normal")

    def show_manual_popup(self):
        manual_window = tk.Toplevel(self.root)
        manual_window.title("USDC Manual")
        manual_window.geometry("400x200")
        manual_label = tk.Label(manual_window, text=manual, wraplength=380, justify="left", font=("Arial", 12, "italic"))
        manual_label.pack(padx=10, pady=10)
        close_button = tk.Button(manual_window, text="Close", command=manual_window.destroy)
        close_button.pack(pady=5)

    def update_expected_listbox(self):
        self.expected_listbox.delete(0, tk.END)
        for p in self.expected_patients:
            self.expected_listbox.insert(tk.END, f"Name: {p['name']}, ID: {p['id']}")

    def display_patient(self):
        name, patient_id, status, vitals, dialogue, is_expected = self.patient_data
        info = f"Patient Name: {name}\nPatient ID: {patient_id}\nPatient says: \"{dialogue}\"\n\n--- VITALS ---\n"
        # Vitals hidden initially
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)
        self.info_text.config(state="disabled")

    def update_score_label(self):
        # Only show strikes and day during gameplay
        self.score_label.config(text=f"Strikes: {self.strikes}/{self.max_strikes} | Day: {self.day}")

    def action_quarantine(self):
        if not self.patient_data:
            return
        # Only allow if all vitals checked
        if not all(self.vitals_checked.values()):
            messagebox.showwarning("Check Vitals", "Please check all vitals before making a decision.")
            return
        name, patient_id, status, vitals, dialogue, is_expected = self.patient_data
        if status == "Doppelganger":
            q = messagebox.askyesno("Confirm", "Are you sure?")
            if q:
                self.score += 1
            else:
                self.strikes += 1
        else:
            self.strikes += 1
        self.new_patient_needed = True
        self.patient_number += 1
        self.update_score_label()
        self.next_patient()

    def action_normal(self):
        if not self.patient_data:
            return
        # Only allow if all vitals checked
        if not all(self.vitals_checked.values()):
            messagebox.showwarning("Check Vitals", "Please check all vitals before making a decision.")
            return
        name, patient_id, status, vitals, dialogue, is_expected = self.patient_data
        if status == "Doppelganger":
            self.strikes += 1
        elif status == "Normal" and is_expected:
            self.score += 1
            # Remove patient from expected_patients after correct identification
            for p in self.expected_patients:
                if p["name"] == name and p["id"] == patient_id:
                    self.expected_patients.remove(p)
                    break
            self.update_expected_listbox()
        # Normal patient not on the list: accepted without penalty (no strike, no score)
        self.new_patient_needed = True
        self.patient_number += 1
        self.update_score_label()
        self.next_patient()

    def next_patient(self):
        if self.strikes >= self.max_strikes:
            self.info_text.config(state="normal")
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"You have reached {self.strikes} strikes. You are fired from the USDC.\nFinal Score: {self.score}")
            self.info_text.config(state="disabled")
            self.button_quarantine.config(state="disabled")
            self.button_normal.config(state="disabled")
            self.button_next.config(state="disabled")
            self.button_end_shift.config(state="disabled")
            # Also disable vitals check buttons
            if hasattr(self, "vital_buttons"):
                for btn in self.vital_buttons.values():
                    btn.config(state="disabled")
            return

        if not self.expected_patients:
            self.day += 1
            self.expected_patients = generate_expected_list()
            self.patient_number = 1
            self.update_expected_listbox()

        self.patient_data = generate_patient(self.expected_patients)
        self.new_patient_needed = False
        self.display_patient()
        self.update_score_label()
        # Reset vitals checked state and buttons
        for vital_key, vital_label in self.vitals_to_check:
            self.vitals_checked[vital_key] = False
            self.vital_buttons[vital_key].config(
                state="normal",
                text=f"Check {vital_label}"
            )
        # Disable Quarantine/Normal buttons until all vitals checked
        self.button_quarantine.config(state="disabled")
        self.button_normal.config(state="disabled")

    def end_shift(self):
        patients_processed = self.patient_number - 1
        # Show score in the End Shift summary popup
        summary = (f"Shift Summary:\n\n"
                   f"Day: {self.day}\n"
                   f"Score: {self.score}\n"
                   f"Strikes: {self.strikes}\n"
                   f"Patients Processed: {patients_processed}")
        messagebox.showinfo("End of Shift Summary", summary)
        # Disable all patient action buttons
        self.button_quarantine.config(state="disabled")
        self.button_normal.config(state="disabled")
        self.button_next.config(state="disabled")
        self.button_end_shift.config(state="disabled")
    # --- END: Move functions into Earth2025App ---


if __name__ == "__main__":
    root = tk.Tk()
    app = Earth2025App(root)
    root.mainloop()