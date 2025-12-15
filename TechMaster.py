import tkinter as tk
from tkinter import messagebox
import random
import os
import winsound
import json
from PIL import Image, ImageTk
from questions import easy_questions, medium_questions, hard_questions

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("TechMaster Challenge")
        self.bg_color = "#0f1720"
        self.card_color = "#102a34"
        self.button_color = "#1f4b50"
        self.text_color = "#d9f7ee"
        self.correct_color = "#2ecc71"
        self.wrong_color = "#e74c3c"
        self.font_main = "Segoe UI Semibold"
        self.font_body = "Segoe UI"

        self.root.geometry("1024x768")
        self.root.configure(bg=self.bg_color)
        self.root.resizable(False, False)

        # Background image
        self.bg_image_path = "bg.png"
        self.load_background_image()

        # Background music
        self.bg_music_path = "BGmusic.wav"
        self.play_bg_music()

        # State
        self.score = 0
        self.q_index = 0
        self.question_counter = 1
        self.total_questions = 20
        self.current_difficulty = "easy"
        self.username = ""
        self.questions = []

        # Milestones
        self.milestone_sounds = {
            1: "1 TO 10.wav",
            5: "5 TO 10.wav",
            10: "10 TO 15.wav",
            15: "15 TO 20.wav",
            20: "20.wav"
        }
        self.milestone_texts = {
            1: "Nice try",
            5: "Nice try",
            10: "Better luck next time",
            15: "Better luck next time",
            20: "Perfect"
        }

        # Average score sounds
        self.average_score_sounds = {
            "1-5": "1 TO 10.wav",
            "6-10": "1 TO 10.wav",
            "11-15": "10 TO 15.wav",
            "16-20": "15 TO 20.wav"
        }

        self.load_leaderboard()
        self.load_player_highscores()
        self.show_welcome_screen()

    def load_background_image(self):
        if os.path.exists(self.bg_image_path):
            try:
                self.bg_image = Image.open(self.bg_image_path)
                self.bg_image = self.bg_image.resize((1024, 768), Image.ANTIALIAS)
                self.bg_photo = ImageTk.PhotoImage(self.bg_image)
                self.bg_label = tk.Label(self.root, image=self.bg_photo)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print("Failed to load background image:", e)
                self.root.configure(bg=self.bg_color)
        else:
            self.root.configure(bg=self.bg_color)

    def play_bg_music(self):
        if os.path.exists(self.bg_music_path):
            try:
                winsound.PlaySound(self.bg_music_path, winsound.SND_ASYNC | winsound.SND_LOOP)
            except Exception as e:
                print("Failed to play background music:", e)

    def stop_bg_music(self):
        winsound.PlaySound(None, winsound.SND_PURGE)

    def clear_screen(self):
        for w in self.root.winfo_children():
            w.destroy()
        if hasattr(self, "bg_label"):
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_center_card(self, w=900, h=600):
        card = tk.Frame(self.root, bg=self.card_color, width=w, height=h)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        return card

    def sound_correct(self):
        winsound.Beep(1200, 120)

    def sound_wrong(self):
        winsound.Beep(400, 200)

    def load_leaderboard(self):
        self.leaderboard_file = "leaderboard.json"
        if os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, "r") as f:
                self.leaderboard = json.load(f)
        else:
            self.leaderboard = {"easy": [], "medium": [], "hard": []}

    def save_leaderboard(self):
        with open(self.leaderboard_file, "w") as f:
            json.dump(self.leaderboard, f, indent=4)

    def load_player_highscores(self):
        self.highscores_file = "player_highscores.json"
        if os.path.exists(self.highscores_file):
            with open(self.highscores_file, "r") as f:
                self.player_highscores = json.load(f)
        else:
            self.player_highscores = {}

    def save_player_highscores(self):
        with open(self.highscores_file, "w") as f:
            json.dump(self.player_highscores, f, indent=4)

    def draw_progress_bar(self, parent):
        canvas = tk.Canvas(parent, width=800, height=10, bg="#1b3a44", highlightthickness=0)
        canvas.pack(pady=10)
        progress = (self.question_counter - 1) / self.total_questions
        canvas.create_rectangle(0, 0, int(800 * progress), 10, fill=self.correct_color, width=0)

    # WELCOME SCREEN
    def show_welcome_screen(self):
        self.clear_screen()
        frame = self.create_center_card(700, 450)

        tk.Label(frame, text="TechMaster Challenge",
                 font=(self.font_main, 26, "bold"),
                 fg=self.text_color, bg=self.card_color).pack(pady=40)

        tk.Button(frame, text="📖 Instructions",
                  font=(self.font_body, 14),
                  bg=self.button_color, fg=self.text_color,
                  width=26, height=2, bd=0,
                  command=self.show_instructions_screen).pack(pady=8)

        tk.Button(frame, text="👤 New Player / Login",
                  font=(self.font_body, 14),
                  bg=self.button_color, fg=self.text_color,
                  width=26, height=2, bd=0,
                  command=self.username_screen).pack(pady=8)

        tk.Button(frame, text="🚪 Quit",
                  font=(self.font_body, 14),
                  bg="#a83232", fg=self.text_color,
                  width=26, height=2, bd=0,
                  command=self.quit_game).pack(pady=8)

    def show_instructions_screen(self):
        self.clear_screen()
        frame = self.create_center_card()
        text = (
            "📖 Instructions\n\n"
            "- Answer tech-related questions\n"
            "- 4 options per question\n"
            "- 1 point per correct answer\n"
            "- Skipping counts as wrong\n\n"
            "- Highscores saved per difficulty\n"
            "- Top 10 scores shown in leaderboard\n"
        )
        tk.Label(frame, text=text, font=(self.font_body, 14),
                 fg="#bff1df", bg=self.card_color, justify="left").pack(pady=40)
        tk.Button(frame, text="Back", font=(self.font_body, 12),
                  bg=self.button_color, fg=self.text_color, width=18, bd=0,
                  command=self.show_welcome_screen).pack()

    def username_screen(self):
        self.clear_screen()
        frame = self.create_center_card(600, 350)
        tk.Label(frame, text="Enter Your Name", font=(self.font_main, 22),
                 fg=self.text_color, bg=self.card_color).pack(pady=30)
        self.name_entry = tk.Entry(frame, font=(self.font_body, 16))
        self.name_entry.pack(pady=10)
        tk.Button(frame, text="Continue", font=(self.font_body, 14),
                  bg=self.button_color, fg=self.text_color, bd=0,
                  command=self.save_username).pack(pady=15)

    def save_username(self):
        name = self.name_entry.get().strip()
        if not name:
            return
        self.username = name
        if name not in self.player_highscores:
            self.player_highscores[name] = {"easy": 0, "medium": 0, "hard": 0}
            self.save_player_highscores()
            messagebox.showinfo("New Player", f"Profile created for {name}")
        else:
            messagebox.showinfo("Welcome Back", f"Welcome back, {name}")
        self.start_menu()

    def start_menu(self):
        self.clear_screen()
        frame = self.create_center_card()
        tk.Label(frame, text=f"Welcome, {self.username}",
                 font=(self.font_main, 22),
                 fg=self.text_color, bg=self.card_color).pack(pady=25)
        for d in ["easy", "medium", "hard"]:
            tk.Button(frame, text=d.upper(),
                      font=(self.font_body, 14),
                      bg=self.button_color, fg=self.text_color,
                      width=22, bd=0,
                      command=lambda x=d: self.start_game(x)).pack(pady=6)
        tk.Button(frame, text="🏆 Leaderboard", bg="#3a5f5f",
                  fg=self.text_color, width=20, bd=0,
                  command=lambda: self.show_leaderboard("easy")).pack(pady=6)
        tk.Button(frame, text="⭐ High Scores", bg="#3a5f5f",
                  fg=self.text_color, width=20, bd=0,
                  command=self.show_high_scores).pack(pady=6)
        tk.Button(frame, text="👤 New Player", font=(self.font_body, 12),
                  bg="#2b3f3f", fg=self.text_color, width=20, bd=0,
                  command=self.show_welcome_screen).pack(pady=(10, 0))

    # ---------- START GAME ----------
    def start_game(self, difficulty):
        self.stop_bg_music()  # stop background music
        self.score = 0
        self.question_counter = 1
        self.current_difficulty = difficulty
        pool = {"easy": easy_questions,
                "medium": medium_questions,
                "hard": hard_questions}.get(difficulty, []).copy()

        if not pool:
            messagebox.showerror("Error", f"No questions found for {difficulty} difficulty!")
            self.start_menu()
            return

        random.shuffle(pool)
        self.questions = pool[:self.total_questions]
        self.q_index = 0  # safe starting index
        self.show_question()

    def show_question(self):
        if not self.questions:
            self.show_result()
            return

        self.clear_screen()
        frame = self.create_center_card()

        try:
            self.current_q, options, self.correct_ans = self.questions[self.q_index]
        except Exception as e:
            print("Error loading question:", e)
            self.show_result()
            return

        top = tk.Frame(frame, bg="#0b2028", padx=15, pady=10)
        top.pack(fill="x")
        tk.Label(top, text=f"{self.username} — Score: {self.score}/{self.total_questions}", font=(self.font_main, 14),
                 fg="#bff1df", bg="#0b2028").pack(side="left")
        tk.Label(top, text=f"{self.current_difficulty.upper()}",
                 font=(self.font_body, 11, "bold"),
                 fg="#0f1720", bg="#ffe1a1", padx=10, pady=4).pack(side="right")
        tk.Label(top, text=f"{self.question_counter}/{self.total_questions}",
                 font=(self.font_body, 12, "bold"),
                 fg=self.text_color, bg="#0b2028").pack(side="right", padx=15)

        self.draw_progress_bar(frame)

        tk.Label(frame, text=self.current_q, font=(self.font_main, 17),
                 fg=self.text_color, bg=self.card_color,
                 wraplength=820, justify="center").pack(pady=30)

        self.feedback_label = tk.Label(frame, text="", font=(self.font_body, 13, "bold"),
                                       bg=self.card_color)
        self.feedback_label.pack()

        options_frame = tk.Frame(frame, bg=self.card_color)
        options_frame.pack(pady=20)

        self.buttons = []
        for i, opt in enumerate(options):
            btn = tk.Button(options_frame, text=opt,
                            font=(self.font_body, 13),
                            bg="#183b44", fg=self.text_color,
                            width=32, height=2, bd=0,
                            command=lambda o=opt, b=i: self.check_answer(o, b))
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            self.buttons.append(btn)

        tk.Button(frame, text="⏭ Skip Question",
                  bg="#4a4a2a", fg=self.text_color,
                  width=18, bd=0,
                  command=self.skip_question).pack(pady=10)

        tk.Button(frame, text="⬅ Back to Menu",
                  bg="#2b3f3f", fg=self.text_color,
                  width=18, bd=0,
                  command=self.start_menu).pack()

    def check_answer(self, selected, idx):
        for btn in self.buttons:
            btn.config(state="disabled")
        if selected == self.correct_ans:
            self.score += 1
            self.sound_correct()
            self.feedback_label.config(text="Correct!", fg=self.correct_color)
        else:
            self.sound_wrong()
            self.feedback_label.config(text=f"Wrong! Correct answer: {self.correct_ans}", fg=self.wrong_color)

        if self.questions:
            self.questions.pop(self.q_index)

        self.question_counter += 1
        self.root.after(1500, self.show_question)

    def skip_question(self):
        for btn in self.buttons:
            btn.config(state="disabled")
        self.sound_wrong()
        self.feedback_label.config(text=f"Skipped! Correct answer: {self.correct_ans}", fg=self.wrong_color)
        if self.questions:
            self.questions.pop(self.q_index)
        self.question_counter += 1
        self.root.after(1500, self.show_question)

    # ---------- SHOW RESULT ----------
    def show_result(self):
        self.clear_screen()
        frame = self.create_center_card(600, 400)

        # Determine average score range
        if 1 <= self.score <= 5:
            avg_text = "Average Score: 1-5"
            avg_sound = self.average_score_sounds.get("1-5")
        elif 6 <= self.score <= 10:
            avg_text = "Average Score: 6-10"
            avg_sound = self.average_score_sounds.get("6-10")
        elif 11 <= self.score <= 15:
            avg_text = "Average Score: 11-15"
            avg_sound = self.average_score_sounds.get("11-15")
        elif 16 <= self.score <= 20:
            avg_text = "Average Score: 16-20"
            avg_sound = self.average_score_sounds.get("16-20")
        else:
            avg_text = "No score"
            avg_sound = None

        # Play average score sound
        if avg_sound and os.path.exists(avg_sound):
            winsound.PlaySound(avg_sound, winsound.SND_ASYNC)

        # Update highscores
        if self.username not in self.player_highscores:
            self.player_highscores[self.username] = {"easy": 0, "medium": 0, "hard": 0}

        if self.score > self.player_highscores[self.username][self.current_difficulty]:
            self.player_highscores[self.username][self.current_difficulty] = self.score
            self.save_player_highscores()

        self.leaderboard[self.current_difficulty].append(
            {"name": self.username, "score": self.score})
        self.leaderboard[self.current_difficulty] = sorted(
            self.leaderboard[self.current_difficulty],
            key=lambda x: x["score"], reverse=True)[:10]
        self.save_leaderboard()

        milestone_text = self.milestone_texts.get(self.score, "Perfect")
        milestone_sound_file = self.milestone_sounds.get(self.score)
        if milestone_sound_file and os.path.exists(milestone_sound_file):
            winsound.PlaySound(milestone_sound_file, winsound.SND_ASYNC)

        tk.Label(frame, text="Quiz Complete!", font=(self.font_main, 22),
                 fg=self.text_color, bg=self.card_color).pack(pady=20)
        tk.Label(frame, text=f"Score: {self.score}/{self.total_questions}",
                 font=(self.font_main, 18),
                 fg="#ffe1a1", bg=self.card_color).pack(pady=10)
        tk.Label(frame, text=milestone_text, font=(self.font_main, 16),
                 fg="#ffe1a1", bg=self.card_color).pack(pady=10)
        tk.Label(frame, text=avg_text, font=(self.font_body, 14),
                 fg="#bff1df", bg=self.card_color).pack(pady=5)

        tk.Button(frame, text="Back to Menu", bg=self.button_color, fg=self.text_color,
                  width=18, bd=0, command=self.start_menu).pack(pady=10)

    # Leaderboard
    def show_leaderboard(self, diff):
        self.clear_screen()
        frame = self.create_center_card()
        for d in ["easy", "medium", "hard"]:
            tk.Button(frame, text=d.upper(),
                      command=lambda x=d: self.show_leaderboard(x),
                      bg=self.button_color, fg=self.text_color,
                      width=10, bd=0).pack(pady=3)
        for i, e in enumerate(self.leaderboard.get(diff, []), 1):
            tk.Label(frame, text=f"{i}. {e['name']} — {e['score']}/20",
                     font=(self.font_body, 14),
                     fg="#bff1df", bg=self.card_color).pack()
        tk.Button(frame, text="Back", bg=self.button_color, fg=self.text_color,
                  width=18, bd=0, command=self.start_menu).pack(pady=10)

    def show_high_scores(self):
        self.clear_screen()
        frame = self.create_center_card(500, 400)
        for d, s in self.player_highscores.get(self.username, {}).items():
            tk.Label(frame, text=f"{d.capitalize()}: {s}/20",
                     font=(self.font_body, 14),
                     fg="#bff1df", bg=self.card_color).pack()
        tk.Button(frame, text="Back", bg=self.button_color, fg=self.text_color,
                  width=18, bd=0, command=self.start_menu).pack(pady=20)

    def quit_game(self):
        self.root.destroy()


# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()
