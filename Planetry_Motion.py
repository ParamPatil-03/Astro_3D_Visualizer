from skyfield.api import load
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import os
from PIL import Image

planet = load('de421.bsp')
planet_dict = {
    "Mercury": planet["MERCURY BARYCENTER"],
    "Venus": planet["venus"],
    "Earth": planet["earth"],
    "Mars": planet["mars"],
    "Jupiter": planet["JUPITER BARYCENTER"],
    "Saturn": planet["SATURN BARYCENTER"],
    "Uranus": planet["URANUS BARYCENTER"],
    "Neptune": planet["NEPTUNE BARYCENTER"]
}

colors = {
    "Mercury": "#A57C1B", "Venus": "#E3BB76", "Earth": "#4F4CB0", "Mars": "#E27B58",
    "Jupiter": "#C88B3A", "Saturn": "#C5AB6E", "Uranus": "#93B8BE", "Neptune": "#6081FF",
    "Sun": "#FFD700"
}
sizes = {
    "Mercury": 20, "Venus": 40, "Earth": 45, "Mars": 35,
    "Jupiter": 100, "Saturn": 85, "Uranus": 60, "Neptune": 60,
    "Sun": 300
}

planet_data = {
    "Mercury": {"Mass": "3.30 × 10^23 kg", "Diameter": "4,879 km", "Gravity": "3.7 m/s²", "Day": "58.6 days", "Year": "88 days"},
    "Venus": {"Mass": "4.87 × 10^24 kg", "Diameter": "12,104 km", "Gravity": "8.87 m/s²", "Day": "243 days", "Year": "225 days"},
    "Earth": {"Mass": "5.97 × 10^24 kg", "Diameter": "12,742 km", "Gravity": "9.8 m/s²", "Day": "24 hours", "Year": "365.25 days"},
    "Mars": {"Mass": "6.39 × 10^23 kg", "Diameter": "6,779 km", "Gravity": "3.71 m/s²", "Day": "24h 37m", "Year": "687 days"},
    "Jupiter": {"Mass": "1.90 × 10^27 kg", "Diameter": "139,820 km", "Gravity": "24.79 m/s²", "Day": "9h 56m", "Year": "11.86 years"},
    "Saturn": {"Mass": "5.68 × 10^26 kg", "Diameter": "116,460 km", "Gravity": "10.44 m/s²", "Day": "10h 42m", "Year": "29.45 years"},
    "Uranus": {"Mass": "8.68 × 10^25 kg", "Diameter": "50,724 km", "Gravity": "8.69 m/s²", "Day": "17h 14m", "Year": "84 years"},
    "Neptune": {"Mass": "1.02 × 10^26 kg", "Diameter": "49,244 km", "Gravity": "11.15 m/s²", "Day": "16h 6m", "Year": "164.8 years"},
    "Sun": {"Mass": "1.99 × 10^30 kg", "Diameter": "1.39 million km", "Gravity": "274 m/s²", "Type": "Yellow Dwarf Star", "Temp": "5,500°C"}
}

ts = load.timescale()
start_time = ts.utc(2025, 1, 1)
current_days = 0
is_paused = False
speed_factor = 1.0
trails = {name: ([], [], []) for name in planet_dict}
MAX_TRAIL_LENGTH = 100

def update(frame):
    global current_days, is_paused
    
    if is_paused:
        return

    current_days += speed_factor
    time = start_time + current_days
    
    date_label.config(text=f"Date: {time.utc_strftime('%Y-%m-%d')}")

    selected = selected_planets.get()
    ax.clear()
    
    ax.set_facecolor('black')
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.line.set_color('white')
    ax.yaxis.line.set_color('white')
    ax.zaxis.line.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')

    ax.scatter(0, 0, 0, color=colors["Sun"], s=sizes["Sun"], label="Sun", edgecolors='orange', alpha=0.9, picker=True)

    planets_to_plot = planet_dict.keys() if selected == "ALL" else [selected]
    
    all_pos = []

    for name in planets_to_plot:
        pos = planet_dict[name].at(time).position.au
        x, y, z = pos[0], pos[1], pos[2]
        
        t_x, t_y, t_z = trails[name]
        t_x.append(x)
        t_y.append(y)
        t_z.append(z)
        if len(t_x) > MAX_TRAIL_LENGTH:
            t_x.pop(0)
            t_y.pop(0)
            t_z.pop(0)
            
        ax.plot(t_x, t_y, t_z, color=colors[name], alpha=0.5, linewidth=1)
        
        ax.scatter(x, y, z, color=colors[name], s=sizes[name], label=name, picker=True)
        all_pos.append(abs(x))
        all_pos.append(abs(y))
        all_pos.append(abs(z))

    max_range = max(all_pos) + 1.0 if all_pos else 2.0
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)
    
    ax.set_title("Solar System 3D (Click a planet!)", color='white', fontsize=15)

def on_pick(event):
    artist = event.artist
    try:
        label = artist.get_label()
        if label in planet_data:
            open_planet_detail(label)
    except AttributeError:
        pass

def open_planet_detail(name):
    detail_window = tk.Toplevel(root)
    detail_window.title(f"Planet Inspector: {name}")
    detail_window.geometry("800x500")
    detail_window.configure(bg='#1e1e1e')

    left_frame = tk.Frame(detail_window, bg='black', width=400)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    fig_detail = plt.figure(figsize=(4, 4), facecolor='black')
    ax_detail = fig_detail.add_subplot(111, projection='3d')
    canvas_detail = FigureCanvasTkAgg(fig_detail, master=left_frame)
    canvas_detail.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = 10 * np.outer(np.cos(u), np.sin(v))
    y = 10 * np.outer(np.sin(u), np.sin(v))
    z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

    script_dir = os.path.dirname(os.path.abspath(__file__))
    texture_path = os.path.join(script_dir, "assets", f"{name.lower()}.png")
    
    texture = None
    if os.path.exists(texture_path):
        try:
            print(f"Loading texture from: {texture_path}")
            img = Image.open(texture_path)
            img = img.resize((50, 50))
            texture = np.array(img) / 255.0
        except Exception as e:
            print(f"Error loading texture: {e}")
    else:
        print(f"Texture not found at: {texture_path}")

    def update_detail(frame):
        ax_detail.clear()
        ax_detail.set_facecolor('black')
        ax_detail.grid(False)
        ax_detail.axis('off')
        
        ax_detail.view_init(elev=30, azim=frame)
        
        if texture is not None:
            ax_detail.plot_surface(x, y, z, rstride=2, cstride=2, facecolors=texture, shade=False)
        else:
            ax_detail.plot_surface(x, y, z, color=colors.get(name, 'white'), alpha=0.9, rstride=5, cstride=5, shade=True)
            
        ax_detail.set_title(name, color='white', fontsize=20)

    anim_detail = FuncAnimation(fig_detail, update_detail, frames=np.arange(0, 360, 2), interval=50)
    canvas_detail.anim = anim_detail

    right_frame = tk.Frame(detail_window, bg='#2d2d2d', width=400, padx=20, pady=20)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    tk.Label(right_frame, text=name.upper(), font=('Arial', 24, 'bold'), bg='#2d2d2d', fg=colors.get(name, 'white')).pack(pady=(0, 20))
    
    info = planet_data.get(name, {})
    for key, value in info.items():
        row = tk.Frame(right_frame, bg='#2d2d2d')
        row.pack(fill=tk.X, pady=5)
        tk.Label(row, text=f"{key}:", font=('Arial', 12, 'bold'), bg='#2d2d2d', fg='#aaaaaa', width=15, anchor='w').pack(side=tk.LEFT)
        tk.Label(row, text=value, font=('Arial', 12), bg='#2d2d2d', fg='white', anchor='w').pack(side=tk.LEFT)

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    play_btn.config(text="▶ Play" if is_paused else "⏸ Pause")

def update_speed(val):
    global speed_factor
    speed_factor = float(val)

root = tk.Tk()
root.title("Planetary Motion 3D")
root.configure(bg='#1e1e1e')

style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background='#1e1e1e', foreground='white')
style.configure("TButton", background='#333', foreground='white', borderwidth=0)
style.map("TButton", background=[('active', '#555')])

main_frame = tk.Frame(root, bg='#1e1e1e')
main_frame.pack(fill=tk.BOTH, expand=True)

fig = plt.figure(figsize=(8, 6), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

canvas.mpl_connect('pick_event', on_pick)

controls_frame = tk.Frame(root, bg='#2d2d2d', pady=10)
controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

selected_planets = tk.StringVar(value="ALL")
dropdown_label = ttk.Label(controls_frame, text="Focus:", background='#2d2d2d', foreground='white')
dropdown_label.pack(side=tk.LEFT, padx=(20, 5))
dropdown = ttk.Combobox(controls_frame, textvariable=selected_planets, state="readonly", width=10)
dropdown["values"] = ["ALL"] + list(planet_dict.keys())
dropdown.pack(side=tk.LEFT, padx=5)

play_btn = tk.Button(controls_frame, text="⏸ Pause", command=toggle_pause, bg='#444', fg='white', relief=tk.FLAT)
play_btn.pack(side=tk.LEFT, padx=20)

speed_label = ttk.Label(controls_frame, text="Speed:", background='#2d2d2d', foreground='white')
speed_label.pack(side=tk.LEFT, padx=(10, 5))
speed_slider = tk.Scale(controls_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL, resolution=0.1, command=update_speed, bg='#2d2d2d', fg='white', highlightthickness=0, length=150)
speed_slider.set(1.0)
speed_slider.pack(side=tk.LEFT, padx=5)

date_label = ttk.Label(controls_frame, text="Date: 2025-01-01", font=('Consolas', 10), background='#2d2d2d', foreground='#00ff00')
date_label.pack(side=tk.RIGHT, padx=20)

animation = FuncAnimation(fig, update, interval=50, cache_frame_data=False)

root.mainloop()
