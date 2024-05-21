import winsound
import random
from tkinter import Canvas, PhotoImage, Button, Label, Tk, Entry, messagebox, Frame
from PIL import ImageTk, Image
import tkinter as tk
from tkinter.font import Font

class BrainTrain(Tk):
    def __init__(self):
        super().__init__()
        self.title("Brain Training")
        self.geometry("1366x768")
        self.attributes("-fullscreen", False)
        self.wm_iconbitmap("data/images/AceMath.ico")

        dataPath = "data"  # Define the data path for image files

        self.BGMusic = lambda: winsound.PlaySound(f"{dataPath}/sounds/BGMusic.wav", winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        self.gameFinishMusic = lambda: winsound.PlaySound(f"{dataPath}/sounds/GameFinish.wav", winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        self.gameStartMusic = lambda: winsound.PlaySound(f"{dataPath}/sounds/GameStart.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        self.DifficultySelectedMusic = lambda: winsound.PlaySound(f"{dataPath}/sounds/DifficultySelected.wav", winsound.SND_FILENAME)
        self.BGMusic()

        # Difficulty levels configuration
        self.difficulty_levels = {
            "Easy": {"range": (1, 10), "operations": ['+', '-', '*', '/'], "time_limit": 5},
            "Normal": {"range": (10, 99), "operations": ['+', '-', '*', '/'], "time_limit": 15},
            "Hard": {"range": (10, 100), "operations": ['+', '-', '*', '/'], "pemdas": True, "time_limit": 30}
        }

        # Background initialization
        self.bg_full_canvas = Canvas(self, width=1366, height=768)
        self.bg_full_canvas.pack()
        self.bg_full_image = ImageTk.PhotoImage(Image.open(f"{dataPath}/images/background-3.jpg"))
        self.bg_full_canvas.create_image(0, 0, anchor="nw", image=self.bg_full_image)

        # Instruction button
        instruction_image = Image.open(f"{dataPath}/images/instruction1.png").resize((250, 100), Image.LANCZOS)
        self.instruction_button_bg = ImageTk.PhotoImage(instruction_image)
        self.instruction_button = Button(self, image=self.instruction_button_bg, command=self.show_instructions)
        self.instruction_button.place(x=568, y=100)  # Place the instruction button above the play button

        # Play button
        play_image = Image.open(f"{dataPath}/images/Play.png").resize((250, 100), Image.LANCZOS)
        self.play_button_bg = ImageTk.PhotoImage(play_image)
        self.play_button = Button(self, image=self.play_button_bg, command=self.difficulty_select)
        self.play_button.place(x=568, y=280)  # Center the play button

        # Exit button
        self.ExitButtonBG = PhotoImage(file=f"{dataPath}/images/Exit.png")
        self.exit_button = Button(self, image=self.ExitButtonBG, borderwidth=0, command=self.close_confirmation)
        self.exit_button.place(x=568, y=470)  # Place below the play button

        # Back button
        self.BackButtonBG = PhotoImage(file=f"{dataPath}/images/Back.png")
        self.back_button = Button(self, image=self.BackButtonBG, borderwidth=0, command=self.to_main_menu)

        # Exit Confirmation Dialog
        self.ExitConfirmDiagBG = Image.open(f"{dataPath}/images/ExitDiag.png").resize((600, 300), Image.LANCZOS)  # Resize the image
        self.ExitConfirmBG = ImageTk.PhotoImage(self.ExitConfirmDiagBG)
        self.exit_confirm = Label(image=self.ExitConfirmBG)

        self.ExitYesButtonBG = PhotoImage(file=f"{dataPath}/images/Yes.png")
        self.exit_yes_button = Button(self, image=self.ExitYesButtonBG, borderwidth=0, command=self.close)

        self.ExitNoButtonBG = PhotoImage(file=f"{dataPath}/images/No.png")
        self.exit_no_button = Button(self, image=self.ExitNoButtonBG, borderwidth=0, command=self.cancel)

        # Load difficulty selection image
        self.select_difficulty_image = ImageTk.PhotoImage(Image.open(f"{dataPath}/images/SelectDifficulty.png"))

        # Bind the Escape key to the close confirmation
        self.bind("<Escape>", self.close_confirmation)

        # Setup difficulty selection
        self.setup_difficulty_selection()

    def show_instructions(self):
        messagebox.showinfo("Instructions", "Welcome to Brain Training!\n\nInstructions:\n1. Select a difficulty level.\n2. Answer the math questions within the time limit.\n3. Try to score as high as possible!\n\nGood luck!")

    def setup_difficulty_selection(self):
        # Load and place difficulty selection buttons
        self.easy_button_bg = PhotoImage(file="data/images/Easy.png")
        self.normal_button_bg = PhotoImage(file="data/images/Normal.png")
        self.hard_button_bg = PhotoImage(file="data/images/Hard.png")

        self.easy_button = Button(self, image=self.easy_button_bg, command=lambda: self.start_game("Easy"))
        self.normal_button = Button(self, image=self.normal_button_bg, command=lambda: self.start_game("Normal"))
        self.hard_button = Button(self, image=self.hard_button_bg, command=lambda: self.start_game("Hard"))

    def difficulty_select(self):
        # Hide the play button, instruction button, and exit button
        self.play_button.place_forget()
        self.instruction_button.place_forget()
        self.exit_button.place_forget()

        # Display the difficulty selection image without covering the full canvas
        self.difficulty_select_label = Label(self, image=self.select_difficulty_image)
        self.difficulty_select_label.place(x=533, y=150)  # Adjust x, y to place it appropriately

        # Display difficulty options
        self.easy_button.place(x=100, y=250)
        self.normal_button.place(x=550, y=250)
        self.hard_button.place(x=1000, y=250)

        # Display the back button
        self.back_button.place(x=50, y=50)  # Adjust x, y to place it appropriately

    def start_game(self, difficulty):
        print(f"Starting game with difficulty: {difficulty}")
        # Hide difficulty buttons and the select difficulty label
        self.easy_button.place_forget()
        self.normal_button.place_forget()
        self.hard_button.place_forget()
        self.difficulty_select_label.place_forget()
        self.back_button.place_forget()
        # Start the game start music
        self.gameStartMusic()
        # Start the countdown timer
        self.countdown_timer(5, difficulty)

    def countdown_timer(self, t, difficulty):
        self.pre_countdown = Label(self, text="", font=("Helvetica", 40))
        self.pre_countdown.place(x=350, y=384)
        self.update_timer(t, difficulty)

    def update_timer(self, t, difficulty):
        if t >= 0:
            self.pre_countdown.config(text=f"Game will start in {t} seconds!", fg="black")
            self.after(1000, self.update_timer, t-1, difficulty)
        else:
            self.pre_countdown.place_forget()
            self.initialize_game(difficulty)

    def initialize_game(self, difficulty):
        # Game logic based on the chosen difficulty
        print(f"Game started with {difficulty} difficulty.")
        self.current_difficulty = difficulty
        self.total_questions = 20  # Set total questions here
        self.current_question = 1
        self.score = 0
        self.timer = None
        self.generate_question()

    def generate_question(self):
        if self.current_question <= self.total_questions:
            difficulty = self.difficulty_levels[self.current_difficulty]
            range_start, range_end = difficulty['range']
            self.num1 = random.randint(range_start, range_end)
            self.num2 = random.randint(range_start, range_end)
            self.operation = random.choice(difficulty['operations'])
            if 'pemdas' in difficulty:
                self.question = f"({self.num1} {self.operation} {self.num2}) {random.choice(['+', '-', '*', '/'])} {random.randint(range_start, range_end)}"
            else:
                if self.operation == '/':
                    while self.num1 % self.num2 != 0:
                        self.num1 = random.randint(range_start, range_end)
                        self.num2 = random.randint(range_start, range_end)
                self.question = f"{self.num1} {self.operation} {self.num2} = ?"
            
            self.question_frame = Frame(self, bg='#4A6572', padx=20, pady=20, relief='ridge', borderwidth=5)
            self.question_frame.place(x=333, y=150, width=700, height=400)

            self.question_label = Label(self.question_frame, text=f"Question {self.current_question}/{self.total_questions}", font=("Helvetica", 18, 'bold'), bg='#4A6572', fg='white')
            self.question_label.pack(pady=10)

            self.question_text_label = Label(self.question_frame, text=self.question, font=("Helvetica", 24, 'bold'), bg='#4A6572', fg='#F9AA33')
            self.question_text_label.pack(pady=20)

            self.answer_entry = Entry(self.question_frame, font=("Helvetica", 18), justify='center')
            self.answer_entry.pack(pady=10)

            self.submit_button = Button(self.question_frame, text="Submit", command=self.check_answer, font=("Helvetica", 18, 'bold'), bg="#F9AA33", fg="white")
            self.submit_button.pack(pady=20)

            self.timer_label = Label(self.question_frame, text=f"Time Left: {difficulty['time_limit']} seconds", font=("Helvetica", 18, 'bold'), bg='#4A6572', fg='white')
            self.timer_label.pack(pady=10)
            self.timer_countdown(difficulty["time_limit"])

    def timer_countdown(self, seconds):
        if self.timer:
            self.after_cancel(self.timer)
        self.timer_label.config(text=f"Time Left: {seconds} seconds")
        if seconds > 0:
            self.timer = self.after(1000, self.timer_countdown, seconds - 1)
        else:
            self.check_answer()

    def check_answer(self):
        if self.timer:
            self.after_cancel(self.timer)
            self.timer = None
        user_answer = self.answer_entry.get()
        correct_answer = eval(self.question.split('=')[0])
        try:
            user_answer = float(user_answer)
        except ValueError:
            user_answer = None
        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            messagebox.showinfo("Incorrect", "Oops! Wrong answer.")
        self.current_question += 1
        self.refresh_question()

    def refresh_question(self):
        if self.current_question > self.total_questions:
            self.end_quiz()
        else:
            self.question_frame.destroy()
            self.generate_question()

    def end_quiz(self):
        for widget in self.winfo_children():
            widget.place_forget()
        
        # Use a custom font for the "Quiz ended" message
        self.custom_font = Font(family="Comic Sans MS", size=24, weight="bold")

        self.score_label = tk.Label(self, text=f"Quiz ended. Your score is {self.score}/{self.total_questions}", font=self.custom_font, bg='#344955', fg='white')
        self.score_label.place(x=450, y=300)
        self.new_game_button = tk.Button(self, text="Start a New Game", command=self.start_new_game, font=self.custom_font, bg="#4A6572", fg="white", relief='ridge')
        self.new_game_button.place(x=550, y=400)
        self.gameFinishMusic()

    def start_new_game(self):
        # Destroy the quiz end screen widgets
        self.score_label.destroy()
        self.new_game_button.destroy()
        # Reset the game by calling the difficulty selection method
        self.difficulty_select()

    def close_confirmation(self, event=None):
        self.exit_confirm.place(x=400, y=234)  # Adjust x, y to center the dialog
        self.exit_yes_button.place(x=480, y=434)
        self.exit_no_button.place(x=700, y=434)

    def close(self):
        self.destroy()

    def cancel(self):
        self.exit_confirm.place_forget()
        self.exit_yes_button.place_forget()
        self.exit_no_button.place_forget()

    def to_main_menu(self):
        # Logic to return to the main menu
        self.easy_button.place_forget()
        self.normal_button.place_forget()
        self.hard_button.place_forget()
        self.difficulty_select_label.place_forget()
        self.back_button.place_forget()
        self.instruction_button.place(x=568, y=100)  # Correct placement for the instruction button
        self.play_button.place(x=568, y=260)  # Correct placement for the play button
        self.exit_button.place(x=568, y=450)  # Correct placement for the exit button

if __name__ == "__main__":
    app = BrainTrain()
    app.mainloop()
