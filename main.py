from tkinter import *
import math

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
remaining_time = 0


def stop_timer():
    global timer, remaining_time
    if timer:
        window.after_cancel(timer)
        timer = None
        # remaining_time keeps its value so resume works


def reset_timer():
    global reps, timer, remaining_time  # ← add remaining_time here
    if timer:
        window.after_cancel(timer)
        timer = None
    reps = 0
    remaining_time = 0  # ← THIS was the core bug
    canvas.itemconfig(timer_text, text="00:00")
    check_label.config(text="")
    timer_label.config(text="TIMER", fg=PINK)  # ← restore colour too


def start_timer():
    global timer, reps, remaining_time
    if timer:
        return

    # Resume from where we stopped
    if remaining_time > 0:
        countdown(remaining_time)
        return

    # Fresh session — reps=0 means first session hasn't started yet
    reps += 1  # ← increment here so label logic is consistent

    if reps % 2 != 0:  # odd rep = study
        timer_label.config(text="STUDY", fg=GREEN, font=(FONT_NAME, 35, "bold"))
        countdown(WORK_MIN * 60)
    else:              # even rep = break
        timer_label.config(text="BREAK", fg=PINK, font=(FONT_NAME, 35, "bold"))
        countdown(SHORT_BREAK_MIN * 60)


def countdown(count):
    global timer, reps, remaining_time
    remaining_time = count
    countmin = math.floor(count / 60)
    countsec = count % 60
    if countsec < 10:
        countsec = f"0{countsec}"
    canvas.itemconfig(timer_text, text=f"{countmin}:{countsec}")

    if count == 0:
        remaining_time = 0
        if reps % 2 != 0:  # study session just finished
            check_label.config(text="✓" * ((reps + 1) // 2))
        timer = None
        start_timer()  # auto-start next session
    else:
        timer = window.after(1000, countdown, count - 1)


window = Tk()
window.title("Pomodoro")
window.config(padx=50, pady=100, bg=YELLOW)

canvas = Canvas(window, width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

timer_label = Label(text="TIMER", bg=YELLOW, fg=PINK, font=(FONT_NAME, 35, "bold"))
timer_label.grid(row=0, column=1)
canvas.grid(row=1, column=1)

start_button = Button(text="Start", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, "bold"), command=start_timer)
start_button.grid(row=3, column=0)
reset_button = Button(text="Reset", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, "bold"), command=reset_timer)
reset_button.grid(row=5, column=1)
stop_button = Button(text="Stop", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, "bold"), command=stop_timer)
stop_button.grid(row=3, column=3)

check_label = Label(text="", bg=YELLOW, fg=PINK, font=(FONT_NAME, 35, "bold"))
check_label.grid(row=4, column=1)

window.mainloop()