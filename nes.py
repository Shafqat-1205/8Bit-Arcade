import os
import subprocess
import tkinter as tk
from tkinter import PhotoImage
import pygame
import random
import sys
import ctypes

# Initialize pygame mixer for sound effects
pygame.mixer.init()

"""
def resource_path(relative_path):
    # Nuitka executables run from the folder of the .exe
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

"""

def resource_path(relative_path):
    # Nuitka executables run from the folder of the .exe
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def safe_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return None

ctypes.windll.gdi32.AddFontResourceExW(resource_path("PressStart2P.ttf"), 0x10, 0)

# Load sound effects
side_sound = safe_sound(resource_path("move.mp3"))
move_sound = safe_sound(resource_path("select.wav"))
select_sound = safe_sound(resource_path("move.wav"))

last_move_time = 0
arrow_ready = False

PAGE_SIZE = 20
current_page = 0
current_index = 0
filtered_roms = []

def on_escape(event=None):
    pygame.mixer.quit()
    root.destroy()


def launch_emulator(rom_path):
    emulator_path = resource_path("NES Games/fceux.exe")

    pygame.mixer.Sound.play(select_sound)

    # Hide menu
    root.withdraw()

    # Launch emulator (non-blocking)
    process = subprocess.Popen([emulator_path, rom_path], shell=True)

    # Poll the process without blocking Tk
    def check_process():
        if process.poll() is None:
            root.after(100, check_process)  # check again in 100ms
        else:
            # Emulator closed
            root.deiconify()
            root.focus_force()
            rom_listbox.focus_set()
            update_pointer()

    root.after(100, check_process)


def force_focus():
    root.deiconify()
    root.focus_force()
    rom_listbox.focus_force()

def on_select(event=None):
    global current_page, current_index
    idx = current_page * PAGE_SIZE + current_index
    if idx < len(filtered_roms):
        rom_file = filtered_roms[idx][0]
        rom_path = resource_path(os.path.join("NES Games", "Games", rom_file))
        launch_emulator(rom_path)

def update_pointer():
    if not arrow_ready:
        return
    
    selection = rom_listbox.curselection()
    if not selection:
        return

    index = selection[0]

    # Get bounding box of the selected item
    bbox = rom_listbox.bbox(index)
    if bbox:
        x, y, width, height = bbox

        # Place arrow to the LEFT of the text, vertically centered
        pointer_label.place(
            x=rom_listbox.winfo_x() - 40,   # adjust left spacing here
            y=rom_listbox.winfo_y() + y + (height // 2) - (arrow_image.height() // 2)
        )

        rom_listbox.see(index)
        
        
def blink_arrow():
    if not arrow_ready:
        root.after(100, blink_arrow)
        return

    pointer_label.place_forget()

    root.after(250, update_pointer)
    root.after(500, blink_arrow)
        
def setup_arrow():
    root.update_idletasks()

    bbox = rom_listbox.bbox(0)
    if not bbox:
        root.after(50, setup_arrow)
        return

    row_height = bbox[3]

    global arrow_image, arrow_ready, pointer_label
    arrow_raw = PhotoImage(file=resource_path("new_arrow.png"))

    scale = max(1, arrow_raw.height() // int(row_height))
    arrow_image = arrow_raw.subsample(scale, scale)

    pointer_label = tk.Label(root, image=arrow_image, bg="black")
    pointer_label.image = arrow_image

    arrow_ready = True
    update_pointer()

    root.after(500, blink_arrow)
    

def start_ui():
    setup_arrow()
    root.after(1000, blink_arrow)
    
    
def on_search(*args):
    global filtered_roms, current_page, current_index
    query = search_var.get().lower()

    # Ignore placeholder
    if query == "search..." or query.strip() == "":
        filtered_roms = all_roms.copy()
    else:
        filtered_roms = [
            rom for rom in all_roms
            if query in rom[1].lower()
        ]

    current_page = 0
    current_index = 0
    update_listbox()
    
def clear_placeholder(event):
    if search_entry.get() == "Search...":
        search_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
available_fonts = root.tk.call("font", "families")
RETRO_FONT = "Press Start 2P" if "Press Start 2P" in available_fonts else "Courier New"
root.title("ROM Selector")
root.geometry("800x600")
root.configure(bg="black")

# Make the window fullscreen
root.attributes('-fullscreen', True)

scanline_canvas = tk.Canvas(root, bg="black", highlightthickness=0)
scanline_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)


def draw_scanlines():
    scanline_canvas.delete("all")
    h = root.winfo_height()
    w = root.winfo_width()

    for y in range(0, h, 4):
        scanline_canvas.create_line(0, y, w, y, fill="#111")

    root.after(500, draw_scanlines)

root.after(500, draw_scanlines)

def tv_noise():
    scanline_canvas.delete("noise")
    w = root.winfo_width()
    h = root.winfo_height()

    for _ in range(30):
        x = random.randint(0, w)
        y = random.randint(0, h)
        scanline_canvas.create_line(x, y, x+2, y, fill="#0A0A0A", tags="noise")

    root.after(120, tv_noise)

tv_noise()

title_frame = tk.Frame(root, bg="black")
title_frame.pack(fill="x", pady=(20, 10))

title_label = tk.Label(
    title_frame,
    text="LOADING...",
    font=(RETRO_FONT, 32),
    fg="#00FF66",
    bg="black"
)

title_label.pack()

subtitle = tk.Label(
    title_frame,
    text="SUPER GAME CARTRIDGE",
    font=(RETRO_FONT, 12),
    fg="white",
    bg="black"
)
subtitle.pack()


# Search bar
search_var = tk.StringVar()

search_entry = tk.Entry(
    root,
    textvariable=search_var,
    font=(RETRO_FONT, 12),
    bg="black",
    fg="white",
    insertbackground="white",
    highlightthickness=2,
    highlightbackground="white",
    highlightcolor="white",
    bd=0
)

search_entry.pack(fill="x", padx=60, pady=(20, 10))


# Create a Listbox to display ROM files
rom_listbox = tk.Listbox(
    root,
    height=30,
    width=80,
    bg="black",
    fg="#00FF66",
    font=(RETRO_FONT, 14),
    selectbackground="black",
    activestyle="none",
    bd=0,
    highlightthickness=0
)

page_label = tk.Label(
    root,
    text="PAGE 1 / 1",
    font=(RETRO_FONT, 12),
    fg="white",
    bg="black"
)
page_label.pack(pady=(10, 20))


frame_border = tk.Frame(root, bg="#222", padx=12, pady=12)
frame_border.pack(expand=True, padx=40, pady=20)

rom_listbox.pack(in_=frame_border, expand=True, fill="both")

rom_listbox.bindtags((rom_listbox, root, "all"))

def get_rom_files(directory):
    return [
        (f, f.replace('_', ' ').replace('.nes', ''))
        for f in os.listdir(directory)
        if f.endswith('.nes')
    ]
    
    
def update_listbox():
    rom_listbox.delete(0, tk.END)

    start = current_page * PAGE_SIZE
    end = start + PAGE_SIZE
    page_items = filtered_roms[start:end]

    for i, (_, display) in enumerate(page_items, start=1 + current_page * PAGE_SIZE):
        rom_listbox.insert(tk.END, f"{i:03d}. {display}")


    if page_items:
        rom_listbox.select_set(current_index)
        rom_listbox.activate(current_index)

    # UPDATE PAGE LABEL (ADD THIS)
    total_pages = max(1, (len(filtered_roms) + PAGE_SIZE - 1) // PAGE_SIZE)
    page_label.config(text=f"PAGE {current_page + 1} / {total_pages}")

    update_pointer()


# Bind Up and Down arrow keys for navigation
def on_up(event):
    global current_page, current_index

    if current_index > 0:
        current_index -= 1
    else:
        if current_page > 0:
            current_page -= 1

            # Go to last item of previous page
            remaining = len(filtered_roms) - current_page * PAGE_SIZE
            current_index = min(PAGE_SIZE, remaining) - 1

    pygame.mixer.Sound.play(move_sound)
    update_listbox()
    return "break"


def on_down(event):
    global current_page, current_index

    page_start = current_page * PAGE_SIZE
    page_end = min(page_start + PAGE_SIZE, len(filtered_roms))

    if current_index < page_end - page_start - 1:
        current_index += 1
    else:
        if page_end < len(filtered_roms):
            current_page += 1
            current_index = 0

    pygame.mixer.Sound.play(move_sound)
    update_listbox()
    return "break"

def on_right(event):
    global current_page, current_index
    if (current_page + 1) * PAGE_SIZE < len(filtered_roms):
        current_page += 1
        current_index = 0
        pygame.mixer.Sound.play(side_sound)
        update_listbox()
    return "break"

def on_left(event):
    global current_page, current_index
    if current_page > 0:
        current_page -= 1
        current_index = 0
        pygame.mixer.Sound.play(side_sound)
        update_listbox()
    return "break"


search_var.trace_add("write", on_search)

roms_folder = resource_path(os.path.join("NES Games", "Games"))
all_roms = get_rom_files(roms_folder)
filtered_roms = all_roms.copy()
game_count = len(all_roms)
title_label.config(text=f"{game_count} IN 1")

update_listbox()

search_entry.insert(0, "Search...")
search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, tk.END))
search_entry.bind("<FocusIn>", clear_placeholder)

root.bind('<Up>', on_up)
root.bind('<Down>', on_down)
root.bind('<Right>', on_right)
root.bind('<Left>', on_left)
root.bind('<Return>', on_select)
root.bind("<Escape>", on_escape)

boot = tk.Label(
    root,
    text="INSERT CARTRIDGE",
    font=(RETRO_FONT, 22),
    fg="#00FF66",
    bg="black"
)
boot.place(relx=0.5, rely=0.5, anchor="center")

def hide_boot():
    boot.destroy()

root.after(1500, hide_boot)



# Automatically select the first item
rom_listbox.select_set(0)
rom_listbox.activate(0)

root.after(100, force_focus)
root.after(150, start_ui)


scanline_canvas.lower(root)

frame_border.lift()
rom_listbox.lift()
title_frame.lift()
page_label.lift()
search_entry.lift()

root.mainloop()