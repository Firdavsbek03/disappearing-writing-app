import tkinter as tk
from tkinter import ttk

user_typed_words = []
counter=0


def selection():
    """
    checks which radio button chosen, and sets up the window accordingly.
    :return: None
    """
    global change_options
    if str(var.get()) == "1":
        number_words.config(state="disabled")
        number_minutes.config(state="readonly")
        timer_counter.config(text=f"{minute_holder.get().split()[0].zfill(2)}:00")
    else:
        number_minutes.config(state="disabled")
        number_words.config(state="readonly")
        timer_counter.config(text=f"{word_holder.get().split()[0].zfill(3)} words")
    change_options=window.after(100, selection)


def manage_user_typing():
    """
    Checks whether the user started typing or not
    :return: redirect to another function
    """
    if len(writing_field.get("1.0", "end-1c")) != 0:
        user_start_writing()
    else:
        window.after(300, manage_user_typing)


def is_user_stopped():
    """
    Checks whether the user stopped typing or not
    :return: boolean
    """
    clone = user_typed_words[:]
    repetition = 0
    for index in range(len(clone)):
        current_value = clone[index]
        try:
            next_value = clone[index + 1]
        except IndexError:
            next_value = current_value
        if next_value == current_value:
            repetition += 1
        else:
            repetition = 0
            while current_value in user_typed_words:
                user_typed_words.remove(current_value)
        if repetition == 10:
            return True
    return False


def user_start_writing():
    """
    Activates the window and starts up the process.
    :return: None
    """
    global start_writing_event
    minute_button.config(state="disabled")
    word_button.config(state="disabled")
    window.after_cancel(change_options)
    user_typed_words.append(writing_field.get("1.0", "end-1c"))
    start_writing_event = window.after(300, user_start_writing)
    if is_user_stopped():
        try:
            window.after_cancel(timer_event)
        except NameError:
            window.after_cancel(word_count_event)
        give_hint("Please, Try Again!!!","red")
    check_user_status()


def check_user_status():
    """
    According to the user choice in radio_buttons,starts timer or word count.
    :return: redirects to another function
    """
    global counter
    if counter==0:
        counter += 1
        if var.get() == "1":
            # start_timer(int(minute_holder.get().split()[0]) * 60)
            start_timer(3)
        else:
            word_count_start()


def start_timer(seconds):
    """
    Starts up the timer for chosen time period.
    :param seconds: int
    :return: None
    """
    global timer_event
    if seconds>=0:
        minute=seconds//60
        second=seconds%60
        timer_counter.config(text=f"{str(minute).zfill(2)}:{str(second).zfill(2)}")
        timer_event=window.after(1000, start_timer, seconds - 1)
    else:
        window.after_cancel(timer_event)
        give_hint("You Have Succeeded!!!","#2192FF")


def word_count_start():
    """
    Starts up word counting backwards.
    :return: None
    """
    global word_count_event
    number_of_words_left=int(word_holder.get().split()[0])-len(writing_field.get("1.0",'end-1c').split())
    if number_of_words_left<0:
        give_hint("You Have Succeeded!!!","#2192FF")
    else:
        timer_counter.config(text=f"{str(number_of_words_left).zfill(3)} words")
        word_count_event=window.after(10, word_count_start)


def give_hint(message,color):
    """
    According to the message and color, it shows the message on window by deactivating every other field.
    :param message: str
    :param color: str
    :return:
    """
    window.after_cancel(start_writing_event)
    writing_field.config(state="disabled")
    success_message = tk.Label(window, text=message, font=("Arial", 36, 'bold'), fg=color)
    success_message.grid(row=3, column=0, columnspan=3)


# Setting up tkinter Window
window = tk.Tk()
window.geometry("900x730")

# Title for the window
title = tk.Label(window, text="Disappearing Text Writing App", font=("Arial", 24, 'normal'))
title.grid(row=0, columnspan=3, column=0, pady=10)

# Variable to hold radio_button value (default value is set to 1)
var = tk.StringVar(window, "1")

# First RadioButton
minute_button = tk.Radiobutton(window, value="1", variable=var, command=selection, text="Minutes",
                               font=("Times New Roman", 16))
minute_button.grid(row=1, column=0, pady=4)

# Second RadioButton
word_button = tk.Radiobutton(window, value="2", variable=var, command=selection, text="Words",
                             font=("Times New Roman", 16))
word_button.grid(row=1, column=1)

# Label for Description for what to choose (minutes/words)
ttk.Label(window, text="Session length :", font=("Times New Roman", 16)).grid(
    column=0, row=2, padx=10, pady=25)

# Minutes Count ComboBox
minute_holder = tk.StringVar()
number_minutes = ttk.Combobox(window, width=10, textvariable=minute_holder, font=("Times New Roman", 14))
number_minutes['values'] = ('1 minute', "3 minutes", "5 minutes", "10 minutes")
number_minutes.current(1)
number_minutes.grid(column=1, row=2)

# Label for how much Time or how many Words left to finish
timer_counter = tk.Label(window, text=f"{minute_holder.get().split()[0].zfill(2)}:00", font=("Times New Roman", 18))
timer_counter.grid(column=2, row=1)

# Words Count ComboBox
word_holder = tk.StringVar()
number_words = ttk.Combobox(window, width=10, textvariable=word_holder, font=("Times New Roman", 14))
number_words['values'] = ("50 words", "75 words", "100 words", "200 words", "500 words")
number_words.grid(column=2, row=2)
number_words.current(1)

# The TextBox for writing input
writing_field = tk.Text(window, font=("Times New Roman", 14))
writing_field.grid(row=3, columnspan=3, column=0, padx=100)
writing_field.focus()

# properly set up the necessities
window.after(100,selection)

# check for user typed or not
manage_user_typing()

window.mainloop()
