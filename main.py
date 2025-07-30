import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox

# Create window
root = tk.Tk()
root.title("🌟 Dreamy To-Do Dashboard")
root.geometry("800x600")

# Fonts
title_font = Font(family="Comic Sans MS", size=22, weight="bold")
label_font = Font(family="Comic Sans MS", size=12)
quote_font = Font(family="Comic Sans MS", size=10, slant="italic")

# --- Theme Setup ---
themes = [
    {
        "name": "Peachy Pink 🍑",
        "bg": "#FFF0F5",
        "task_bg": "#FFCCE5",
        "text_bg": "#FFF5F7",
        "button_bg": "#FF99CC",
        "button_fg": "#4B2C39",
        "highlight": "#FF66A3",
        "quote_fg": "#C71585"
    },
    {
        "name": "Cozy Night 🌙",
        "bg": "#1A1A2E",
        "task_bg": "#16213E",
        "text_bg": "#0F3460",
        "button_bg": "#53354A",
        "button_fg": "white",
        "highlight": "#E94560",
        "quote_fg": "#DDDDDD"
    },
    {
        "name": "Sky Blue ☁️",
        "bg": "#E0F7FA",
        "task_bg": "#B2EBF2",
        "text_bg": "#B3E5FC",
        "button_bg": "#4FC3F7",
        "button_fg": "#003f5c",
        "highlight": "#29B6F6",
        "quote_fg": "#0277BD"
    }
]
current_theme = [0]

# Title Frame
title_frame = tk.Frame(root)
title_frame.pack(pady=10)
title_label = tk.Label(title_frame, text="🌸 My Dreamy To-Do List", font=title_font)
title_label.pack(side="left")
star_label = tk.Label(title_frame, text="✨", font=title_font)
star_label.pack(side="left")

def animate_star(symbols=["✨", "🌟", "💫", "⭐"]):
    def cycle_symbols(index=0):
        star_label.config(text=symbols[index % len(symbols)])
        root.after(500, lambda: cycle_symbols(index + 1))
    cycle_symbols()
animate_star()

# Quote of the Day
quote = tk.Label(root, text="“Believe you can and you're halfway there.” – T. Roosevelt", font=quote_font)
quote.pack()

# Left Frame (Tasks)
left_frame = tk.Frame(root)
left_frame.place(x=30, y=100, width=350, height=400)
tasks_frame = tk.LabelFrame(left_frame, text="To-Do Tasks 📝", font=label_font, padx=10, pady=10)
tasks_frame.pack(fill="both", expand=True)
task_vars = []
task_checkbuttons = []

def add_task():
    task_text = task_entry.get()
    if task_text:
        var = tk.BooleanVar()
        cb = tk.Checkbutton(tasks_frame, text=task_text, variable=var, font=label_font)
        cb.pack(anchor="w")
        task_vars.append((var, task_text))
        task_checkbuttons.append(cb)
        task_entry.delete(0, tk.END)
        apply_theme(themes[current_theme[0]])

task_entry = tk.Entry(root, font=label_font, width=28)
task_entry.place(x=50, y=520)
add_btn = tk.Button(root, text="Add Task 🌱", font=label_font, command=add_task)
add_btn.place(x=290, y=515)

# Right Frame (Notes / Focus / Remember)
right_frame = tk.Frame(root)
right_frame.place(x=410, y=100, width=360, height=400)

notes_frame = tk.LabelFrame(right_frame, text="🌼 Notes", font=label_font, padx=5, pady=5)
notes_frame.pack(fill="x", padx=5, pady=5)
notes_text = tk.Text(notes_frame, height=4, font=("Comic Sans MS", 10))
notes_text.pack()

focus_frame = tk.LabelFrame(right_frame, text="🔍 Focus", font=label_font, padx=5, pady=5)
focus_frame.pack(fill="x", padx=5, pady=5)
focus_text = tk.Text(focus_frame, height=3, font=("Comic Sans MS", 10))
focus_text.pack()

remember_frame = tk.LabelFrame(right_frame, text="📌 Remember", font=label_font, padx=5, pady=5)
remember_frame.pack(fill="x", padx=5, pady=5)
remember_text = tk.Text(remember_frame, height=3, font=("Comic Sans MS", 10))
remember_text.pack()

# Save Button
def save_all():
    with open("my_dreamy_dashboard.txt", "w", encoding="utf-8") as file:
        file.write("🌸 My Dreamy To-Do List\n")
        file.write("=" * 30 + "\n\n")
        file.write("📝 Tasks:\n")
        for var, task_text in task_vars:
            status = "[✅]" if var.get() else "[❎]"
            file.write(f"{status} {task_text}\n")
        file.write("\n🌼 Notes:\n" + notes_text.get("1.0", tk.END).strip() + "\n\n")
        file.write("🔍 Focus:\n" + focus_text.get("1.0", tk.END).strip() + "\n\n")
        file.write("📌 Remember:\n" + remember_text.get("1.0", tk.END).strip() + "\n\n")
        file.write("💡 Quote of the Day:\n" + quote["text"] + "\n")
    messagebox.showinfo("Saved!", "🌷 Your tasks & notes have been saved to 'my_dreamy_dashboard.txt'!")

save_btn = tk.Button(root, text="💾 Save Everything", font=label_font, command=save_all)
save_btn.place(x=340, y=560)

# Pomodoro Timer in Popup Window
def open_pomodoro():
    pomodoro_win = tk.Toplevel(root)
    pomodoro_win.title("🍅 Pomodoro Timer")
    pomodoro_win.geometry("300x200")
    
    timer_label = tk.Label(pomodoro_win, text="25:00", font=("Comic Sans MS", 22))
    timer_label.pack(pady=10)

    seconds = [25 * 60]
    running = [False]
    after_id = [None]

    def update_timer():
        if running[0] and seconds[0] > 0:
            mins, secs = divmod(seconds[0], 60)
            timer_label.config(text=f"{mins:02d}:{secs:02d}")
            seconds[0] -= 1
            after_id[0] = pomodoro_win.after(1000, update_timer)
        elif seconds[0] == 0:
            timer_label.config(text="Time's Up!")
            messagebox.showinfo("Pomodoro Done!", "Time to take a break! 🌸")
            running[0] = False

    def start():
        if not running[0]:
            running[0] = True
            update_timer()

    def pause():
        running[0] = False
        if after_id[0]:
            pomodoro_win.after_cancel(after_id[0])

    def restart():
        pause()
        seconds[0] = 25 * 60
        timer_label.config(text="25:00")

    btns = tk.Frame(pomodoro_win)
    btns.pack(pady=5)
    tk.Button(btns, text="Start ⏱️", command=start, font=label_font).pack(side="left", padx=5)
    tk.Button(btns, text="Pause ⏸️", command=pause, font=label_font).pack(side="left", padx=5)
    tk.Button(btns, text="Restart 🔄", command=restart, font=label_font).pack(side="left", padx=5)

# Pomodoro Button (bottom right)
pomodoro_btn = tk.Button(root, text="🍅 Pomodoro Timer", font=label_font, command=open_pomodoro)
pomodoro_btn.place(x=620, y=560)

# Theme Application
def apply_theme(theme):
    root.config(bg=theme["bg"])
    title_frame.config(bg=theme["bg"])
    title_label.config(bg=theme["bg"], fg=theme["highlight"])
    star_label.config(bg=theme["bg"], fg=theme["highlight"])
    quote.config(bg=theme["bg"], fg=theme["quote_fg"])

    left_frame.config(bg=theme["bg"])
    tasks_frame.config(bg=theme["task_bg"], fg=theme["button_fg"])
    for cb in task_checkbuttons:
        cb.config(bg=theme["task_bg"], fg=theme["button_fg"], activebackground=theme["highlight"])

    right_frame.config(bg=theme["bg"])
    notes_frame.config(bg=theme["text_bg"])
    focus_frame.config(bg=theme["text_bg"])
    remember_frame.config(bg=theme["text_bg"])

    notes_text.config(bg="white", fg="black")
    focus_text.config(bg="white", fg="black")
    remember_text.config(bg="white", fg="black")

    add_btn.config(bg=theme["button_bg"], fg=theme["button_fg"], activebackground=theme["highlight"])
    save_btn.config(bg=theme["button_bg"], fg=theme["button_fg"], activebackground=theme["highlight"])
    theme_btn.config(bg=theme["button_bg"], fg=theme["button_fg"], activebackground=theme["highlight"])
    task_entry.config(bg="white", fg="black")
    pomodoro_btn.config(bg=theme["button_bg"], fg=theme["button_fg"], activebackground=theme["highlight"])

# Theme Changer
def change_theme():
    current_theme[0] = (current_theme[0] + 1) % len(themes)
    apply_theme(themes[current_theme[0]])
    theme_btn.config(text=f"🎨 Theme: {themes[current_theme[0]]['name']}")

theme_btn = tk.Button(root, text="🎨 Theme: Peachy Pink 🍑", font=label_font, command=change_theme)
theme_btn.place(x=50, y=560)

# Apply first theme
apply_theme(themes[0])
root.mainloop()
