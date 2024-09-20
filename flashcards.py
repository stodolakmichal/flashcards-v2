from random import random, randint
from customtkinter import *

# Create the main window
root = CTk()
root.title("DailyDictation flashcards!")
root.geometry('900x500')
set_appearance_mode('dark')

correct_answers_counter = 0
wrong_answers_counter = 0


# Get list of the words from notes.txt
def get_words():
    with open("notes.txt", "r", encoding="utf-8") as file:
        words = file.readlines()
    words = convert_to_dict(words)
    return words


def convert_to_dict(list_of_words):
    words_dict = {}
    for word in list_of_words:
        word = word.strip()
        if word:
            english, polish = word.split(" - ")
            words_dict[english] = polish
    return words_dict


def next():
    root.bind('<Return>', lambda event: answer())
    random_word = list(dict_of_words.keys())[randint(0, len(dict_of_words) - 1)]
    english_word_label.configure(text=random_word)
    answer_button.configure(state=NORMAL)
    dont_know_button.configure(state=NORMAL)
    my_entry.delete(0, END)
    answer_label.configure(text='')
    translation_label.configure(text='')


def answer():
    english_word = english_word_label.cget("text")
    polish_word = dict_of_words[english_word]
    if polish_word == my_entry.get():
        answer_label.configure(text=f"Your answer is correct!", text_color='green', font=("Helvetica", 16))
        dict_of_words.pop(english_word)
        answer_button.configure(state=DISABLED)
        dont_know_button.configure(state=DISABLED)
        global correct_answers_counter
        correct_answers_counter += 1
        correct_answers_counter_label.configure(text=f'Correct answers: {correct_answers_counter}')
        left_words_label.configure(text=f'Words left: {len(dict_of_words)}')
        translation_label.configure(text=f"{english_word} - {polish_word}")
        root.bind('<Return>', lambda event: next())
    else:
        global wrong_answers_counter
        if not answer_label.cget(
                "text") == f"Incorrect! The correct answer is: {polish_word}" and not answer_label.cget(
            "text") == f"{polish_word}":
            wrong_answers_counter += 1
        answer_label.configure(text=f"Incorrect! The correct answer is: {polish_word}", text_color='red',
                               font=("Helvetica", 16))
        wrong_answers_counter_label.configure(text=f'Wrong answers: {wrong_answers_counter}')


def show_answer():
    english_word = english_word_label.cget("text")
    polish_word = dict_of_words[english_word]
    global wrong_answers_counter
    if not answer_label.cget("text") == f"Incorrect! The correct answer is: {polish_word}" and not answer_label.cget(
            "text") == f"{polish_word}":
        wrong_answers_counter += 1
        wrong_answers_counter_label.configure(text=f'Wrong answers: {wrong_answers_counter}')
        answer_label.configure(text=f"{polish_word}")


def choose_language(choice):
    global dict_of_words, dict_english_polish, dict_polish_english, correct_answers_counter, wrong_answers_counter
    correct_answers_counter = 0
    wrong_answers_counter = 0
    correct_answers_counter_label.configure(text=f'Correct answers: {correct_answers_counter}')
    wrong_answers_counter_label.configure(text=f'Wrong answers: {wrong_answers_counter}')
    dict_of_words = get_words()
    dict_english_polish = dict_of_words
    dict_polish_english = {value: key for key, value in dict_english_polish.items()}
    if choice == "Polish - English":
        dict_of_words = dict_polish_english
        left_words_label.configure(text=f'Words left: {len(dict_of_words)}')
        next()
    else:
        dict_of_words = dict_english_polish
        left_words_label.configure(text=f'Words left: {len(dict_of_words)}')
        next()


dict_of_words = get_words()
dict_english_polish = dict_of_words
dict_polish_english = {value: key for key, value in dict_english_polish.items()}

# Frames
menu_bar_frame = CTkFrame(master=root, height=30)
menu_bar_frame.columnconfigure(0, weight=1)
menu_bar_frame.pack(side=TOP, anchor='n', fill=X, padx=10)

left_frame = CTkFrame(master=root)
left_frame.columnconfigure(0, weight=1)
left_frame.pack(side=LEFT, anchor='n', expand=True, fill=BOTH, padx=10, pady=10)

right_frame = CTkFrame(master=root)
right_frame.columnconfigure(1, weight=1)
right_frame.pack(side=LEFT, anchor='n', expand=True, fill=BOTH, padx=10, pady=10)

score_board_frame = CTkFrame(master=left_frame)
score_board_frame.pack(side=TOP, anchor='n', expand=True, padx=10, pady=10)

# ComboBox
list_of_options = ['English - Polish', 'Polish - English']
file_menu = CTkOptionMenu(menu_bar_frame, values=list_of_options, command=choose_language)
file_menu.set(list_of_options[0])
file_menu.pack(side=TOP, anchor='w', expand=True)

# Labels
english_word_label = CTkLabel(master=right_frame, text='', font=("Helvetica", 16))
english_word_label.pack(side=TOP, expand=True, padx=10)

translation_label = CTkLabel(master=right_frame, text='', font=("Helvetica", 16))
translation_label.pack(side=TOP, expand=True, padx=10)

answer_label = CTkLabel(master=right_frame, text='', font=("Helvetica", 16))
answer_label.pack(side=TOP, expand=True, padx=10)

left_words_label = CTkLabel(master=score_board_frame, text=f'Words: {len(dict_of_words)}', font=("Helvetica", 14))
left_words_label.pack(side=TOP, expand=True, padx=10, pady=5)

correct_answers_counter_label = CTkLabel(master=score_board_frame, text=f'Correct answers: {correct_answers_counter}',
                                         font=("Helvetica", 14), text_color='green')
correct_answers_counter_label.pack(side=TOP, expand=True, padx=10, pady=5)

wrong_answers_counter_label = CTkLabel(master=score_board_frame, text=f'Wrong answers: {wrong_answers_counter}',
                                       font=("Helvetica", 14), text_color='red')
wrong_answers_counter_label.pack(side=TOP, expand=True, padx=10, pady=5)

# Entry
my_entry = CTkEntry(master=right_frame, font=("Helvetica", 16), width=500, border_width=1, border_color='white',
                    justify=CENTER)
my_entry.pack(side=TOP, expand=True, padx=10)

# Buttons
answer_button = CTkButton(master=right_frame, text='Answer', corner_radius=32, command=answer, border_width=1,
                          border_color='white')
answer_button.pack(side=LEFT, expand=True, fill=BOTH, padx=10, pady=10)

dont_know_button = CTkButton(master=right_frame, text="Don't know", corner_radius=32, command=show_answer,
                             border_width=1, border_color='white')
dont_know_button.pack(side=LEFT, expand=True, fill=BOTH, padx=10, pady=10)

next_button = CTkButton(master=right_frame, text='Next', corner_radius=32, command=next, border_width=1,
                        border_color='white')
next_button.pack(side=LEFT, expand=True, fill=BOTH, padx=10, pady=10)

# Bind enter to the answer_button
root.bind('<Return>', lambda event: answer())
root.bind('<Control-n>', lambda event: next())

# Run the main window loop
next()
root.mainloop()
