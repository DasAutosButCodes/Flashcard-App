import customtkinter as ctk
import random, json
from tkinter import filedialog

class FlashCard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Flashcards!")
        self.geometry("700x500")
        self.current_index = 0
        self.current_question = ""
        self.current_answer = ""
        self.cards = [
            {"question": "первый вопрос", "answer": "первый ответ"},
            {"question": "второй вопрос", "answer": "второй ответ"},
            {"question": "третий вопрос", "answer": "третий ответ"}
        ]
        self.filepath = ""

        self.flashcard = ctk.CTkLabel(master=self, text="", wraplength=480, justify="left", width=500, height=250, font=("Arial", 24),
                                  fg_color="gray25", corner_radius=20)
        self.flashcard.bind("<Button-1>", self.flip_card)
        self.flashcard.pack(padx=50, pady=(45, 0))

        self.buttons_frame = ctk.CTkFrame(master=self, width=500, height=100)
        self.buttons_frame.pack(padx=50, pady=20)
        self.next_btn = ctk.CTkButton(master=self.buttons_frame, text="▶", command=lambda: self.change_card(1), width=50, height=50, font=("Arial", 40))
        self.next_btn.place(x=300, y=25)
        self.random_btn = ctk.CTkButton(master=self.buttons_frame, text="🎲", command=lambda: self.change_card(0), width=50, height=50, font=("Arial", 35))
        self.random_btn.place(x=225, y=25)
        self.previous_btn = ctk.CTkButton(master=self.buttons_frame, text="◀", command=lambda: self.change_card(-1), width=50, height=50, font=("Arial", 40))
        self.previous_btn.place(x=150, y=25)
        self.editor_btn = ctk.CTkButton(master=self.buttons_frame, text="✏", command=self.editor, width=50, height=50, font=("Arial", 40))
        self.editor_btn.place(x=375, y=25)
        self.import_btn = ctk.CTkButton(master=self.buttons_frame, text="📥", command=self.import_flashcards,
                                      width=50, height=50, font=("Arial", 35))
        self.import_btn.place(x=75, y=25)

        self.question_count = ctk.CTkLabel(master=self, text="", font=("Arial", 25))
        self.question_count.pack(padx=50)
        self.show_question()

    def import_flashcards(self):
        self.filepath = filedialog.askopenfilename(title="Выберите JSON-файл", filetypes=[("JSON files", "*.json")])
        if self.filepath:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.cards = json.load(f)
                self.show_question()

    def flip_card(self, event):
        self.flashcard.configure(text=self.current_answer,  fg_color="gray35" if self.flashcard.cget("fg_color") == "gray25" else "gray25")
        self.current_question, self.current_answer = self.current_answer, self.current_question

    def change_card(self, step):
        if step == 0:
            self.current_index = random.randint(0, len(self.cards)-1)
        else:
            self.current_index = (self.current_index + step) % len(self.cards)
        self.show_question()

    def show_question(self):
        if not self.cards:
            self.flashcard.configure(text="Нет карточек", fg_color="gray25")
            self.question_count.configure(text="0/0")
            return
        data = list(self.cards[self.current_index].values())
        self.current_question, self.current_answer = data[0], data[1]
        self.flashcard.configure(text=self.current_question, fg_color="gray25")
        self.question_count.configure(text=f"{self.current_index + 1}/{len(self.cards)}")

    def editor(self):
        editor_root = ctk.CTkToplevel(self)
        editor_root.geometry("450x650")
        editor_root.title("Эдитор")
        editor_root.attributes("-topmost", True)
        def on_close():
            editor_root.destroy()
            print("Закрыт!")
        editor_root.protocol("WM_DELETE_WINDOW", on_close)

        def shuffle_cards():
            random.shuffle(self.cards)
            for flashcard in flashcards_frame.winfo_children():
                flashcard.destroy()
            for flashcard_data in self.cards:
                add_flashcard(flashcard_data)
            self.show_question()

        def save_cards():
            if self.filepath:
                with open(self.filepath, "w", encoding="utf-8") as f:
                    json.dump(get_clean_cards(), f, ensure_ascii=False, indent=4)
            else:
                save_as_cards()

        def save_as_cards():
            self.filepath = filedialog.asksaveasfilename(title="Создать новые флешкарточки",defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if self.filepath:
                with open(self.filepath, "w", encoding="utf-8") as f:
                    json.dump(get_clean_cards(), f, ensure_ascii=False, indent=4)

        def get_clean_cards():
            clean_cards = []
            for card in self.cards:
                clean_cards.append({
                    "question": card["question"],
                    "answer": card["answer"]
                })
            return clean_cards

        def create_flashcard():
            data = {"question": "", "answer": ""}
            self.cards.append(data)
            add_flashcard(data)
            open_flashcard(data)

        search = ctk.CTkEntry(editor_root, width=300, placeholder_text="Поиск по вопросам...")
        search.pack(pady=10, padx=20)
        search.bind("<KeyRelease>", lambda e: search_flashcards(search.get()))
        flashcards_frame = ctk.CTkScrollableFrame(editor_root, width=450)
        flashcards_frame.pack(pady=(0, 50), padx=20, fill="both", expand=True)
        flashcards_frame.bind("<Button-1>", lambda e: editor_root.focus())

        options = ctk.CTkFrame(editor_root, width=450, height=65,fg_color="gray20")
        options.place(x=0, y=590)
        create_flashcard_btn = ctk.CTkButton(options, text="+", command=create_flashcard, width=75, height=50, font=("Arial", 40))
        create_flashcard_btn.place(x=335, y=5)
        shuffle_flashcard_btn = ctk.CTkButton(options, text="🔀", command=shuffle_cards, width=75, height=50, font=("Arial", 32))
        shuffle_flashcard_btn.place(x=235, y=5)
        save_flashcard_btn = ctk.CTkButton(options, text="💾", command=save_cards, width=75, height=50,
                                              font=("Arial", 32))
        save_flashcard_btn.place(x=135, y=5)
        save_as_flashcard_btn = ctk.CTkButton(options, text="🗂", command=save_as_cards, width=75, height=50,
                                           font=("Arial", 32))
        save_as_flashcard_btn.place(x=35, y=5)

        def shorten_question(question):
            return question if len(question) <= 65 else question[:65] + "..."

        def add_flashcard(flashcard_data):
            flashcard = ctk.CTkFrame(flashcards_frame)
            flashcard.pack(pady=(10, 5), padx=25, fill="x")
            header = ctk.CTkLabel(flashcard, text=shorten_question(flashcard_data["question"]), font=("Arial", 16), wraplength=275, justify="left")
            flashcard_data["header"] = header
            header.pack(side="left", fill="x", expand=True)
            delete_btn = ctk.CTkButton(flashcard, text="🗑", command=lambda: delete_flashcard(flashcard, flashcard_data), width=40, height=40, font=("Arial", 18))
            delete_btn.pack(side="right")

            for clickable in flashcard, header:
                clickable.bind("<Button-1>", lambda e: open_flashcard(flashcard_data))
                clickable.bind("<Enter>", lambda e: flashcard.configure(cursor="hand2"))  # "hand2" = палец (как в браузере)
                clickable.bind("<Leave>", lambda e: flashcard.configure(cursor=""))

        for flashcard_data in self.cards:
            add_flashcard(flashcard_data)

        def search_flashcards(text):
            search = text.lower().strip()
            headers_match = []
            for data in self.cards:
                header = data["question"].lower()
                match = 0
                if search in header:
                    match = len(search)
                else:
                    for size in range(len(search), 0, -1):
                        if any(search[i:i + size] in header for i in range(len(search) - size + 1)):
                            match = size
                            break
                headers_match.append((match, data))
            headers_match.sort(key=lambda x: x[0], reverse=True)
            for _, data in headers_match:
                data["header"].master.pack_forget()
            for _, data in headers_match:
                data["header"].master.pack(pady=(10,5), padx=25, fill="x")

        def delete_flashcard(flashcard, flashcard_data):
            flashcard.destroy()
            self.cards.remove(flashcard_data)

        def open_flashcard(flashcard_data):
            flashcard_window = ctk.CTkToplevel(self)
            flashcard_window.geometry("450x425")
            flashcard_window.title(flashcard_data["question"])
            flashcard_window.attributes("-topmost", True)

            question_txt = ctk.CTkLabel(flashcard_window, text="Вопрос", text_color="gray55", font=("Arial", 12))
            question_txt.place(x=30, y=5)
            question = ctk.CTkTextbox(flashcard_window, width=400, height=150, font=("Arial", 24))
            question.insert(0.0, flashcard_data["question"])
            question.pack(pady=(35,15), padx=25)

            answer_txt = ctk.CTkLabel(flashcard_window, text="Ответ", text_color="gray55", font=("Arial", 12))
            answer_txt.place(x=30, y=186)
            answer = ctk.CTkTextbox(flashcard_window, width=400, height=150, font=("Arial", 24))
            answer.insert(0.0, flashcard_data["answer"])
            answer.pack(pady=15, padx=25)

            save_btn = ctk.CTkButton(flashcard_window, text="Сохранить", width=120, height=40, font=("Arial", 24),
                                     command=lambda: save_flashcard(flashcard_data, question.get("0.0", "end-1c"), answer.get("0.0", "end-1c")))
            save_btn.pack(pady=(0, 10))

        def save_flashcard(flashcard_data, question, answer):
            question = "Безымянная карточка" if not question.strip() else shorten_question(question)
            flashcard_data["question"], flashcard_data["answer"] = question, answer
            flashcard_data["header"].configure(text=question)

if __name__ == "__main__":
    app = FlashCard()
    app.mainloop()