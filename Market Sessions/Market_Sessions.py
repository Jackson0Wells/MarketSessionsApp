import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
from datetime import datetime, timedelta, timezone
import json

# Define all settings directly in the script
settings = {
    'hide_panel_setting': 0,
    'transparency': 1.0,  # Default transparency
    'image_width': 1024,  # Default image width
    'image_height': 576,  # Default image height
}

def create_minimize_button(parent):
    minimize_button = tk.Button(parent, text="_", command=minimize_app, bg="#AAAAAA", fg="#FFFFFF")
    minimize_button.pack(side=tk.RIGHT)
    return minimize_button

def start_move_image(event):
    image_window.x = event.x
    image_window.y = event.y

def stop_move_image(event):
    image_window.x = None
    image_window.y = None

def start_resize(event):
    image_window.resize_x = event.x
    image_window.resize_y = event.y
    image_window.width = image_window.winfo_width()
    image_window.height = image_window.winfo_height()

def stop_resize(event):
    image_window.resize_x = None
    image_window.resize_y = None

def on_move_image(event):
    if image_window.x is not None and image_window.y is not None:
        deltax = event.x - image_window.x
        deltay = event.y - image_window.y
        x = image_window.winfo_x() + deltax
        y = image_window.winfo_y() + deltay
        image_window.geometry(f"+{x}+{y}")

def on_resize(event):
    if image_window.resize_x is not None and image_window.resize_y is not None:
        new_width = event.x - image_window.resize_x + image_window.width
        new_height = event.y - image_window.resize_y + image_window.height
        resize_image(new_width, new_height)

def resize_image(image, new_width, new_height):
    global image_label
    if image_visible:
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)  # Use Image.LANCZOS instead of Image.ANTIALIAS
        photo_image = ImageTk.PhotoImage(resized_image)
        image_label.configure(image=photo_image)
        image_label.image = photo_image  # Keep a reference
        image_window.geometry(f"{new_width}x{new_height}")

SA_TIME_ZONE_OFFSET = timedelta(hours=2)

market_sessions = {
    'Sydney': {'start': 21, 'end': 6, 'description': 'Sydney Session | Accumulation'},  # 9 PM - 6 AM UTC
    'Tokyo': {'start': 0, 'end': 9, 'description': 'Tokyo Session | Accumulation'},     # 12 AM - 9 AM UTC
    'London': {'start': 7, 'end': 16, 'description': 'London Session | Manipulation'},   # 7 AM - 4 PM UTC
    'New York': {'start': 13, 'end': 22, 'description': 'New York Session | Distribution'},  # 1 PM - 10 PM UTC
}

def get_session_info():
    now_utc = datetime.now(timezone.utc)
    session_info = {}
    
    for session, details in market_sessions.items():
        start_hour = details['start']
        end_hour = details['end']
        
        # Calculate today's start and end times in UTC
        start_time_utc = datetime(now_utc.year, now_utc.month, now_utc.day, start_hour, tzinfo=timezone.utc)
        end_time_utc = datetime(now_utc.year, now_utc.month, now_utc.day, end_hour, tzinfo=timezone.utc)
        
        # Adjust for sessions that end after midnight UTC
        if start_hour > end_hour:
            end_time_utc += timedelta(days=1)
        
        # Determine status and countdown
        if start_time_utc <= now_utc < end_time_utc:
            status = 'Active'
            countdown = end_time_utc - now_utc
        else:
            status = 'Inactive'
            countdown = start_time_utc - now_utc
            if countdown.days < 0:
                countdown = (start_time_utc + timedelta(days=1)) - now_utc
        
        countdown_formatted = str(countdown).split('.')[0]  # Remove microseconds
        session_info[session] = {'status': status, 'countdown': countdown_formatted}

    return session_info

def setup_session_labels(frame):
    column_headers = ['Session', 'Status', 'Countdown']
    for i, header in enumerate(column_headers):
        tk.Label(frame, text=header, fg="#FFFFFF", bg="#222222", font=('Arial', 10, 'bold')).grid(row=0, column=i, padx=10, sticky='ew')
    
    global session_labels
    session_labels = {}
    for i, (session, details) in enumerate(market_sessions.items(), start=1):
        description_label = tk.Label(frame, text=details['description'], fg="#FFFFFF", bg='#222222', font=('Arial', 10))
        description_label.grid(row=i, column=0, padx=10, sticky="w")
        status_label = tk.Label(frame, text="", fg="#FFFFFF", bg='#222222', font=('Arial', 10))
        status_label.grid(row=i, column=1, padx=10)
        countdown_label = tk.Label(frame, text="", fg="#FFFFFF", bg='#222222', font=('Arial', 10))
        countdown_label.grid(row=i, column=2, padx=10)
        session_labels[session] = (description_label, status_label, countdown_label)

def update_labels():
    session_info = get_session_info()
    for session, details in session_info.items():
        _, status_label, countdown_label = session_labels[session]
        status, countdown = details['status'], details['countdown']
        status_label.config(text=status, fg="#00FF00" if status == 'Active' else "#FF0000")
        countdown_label.config(text=countdown, fg="#FFFFFF")
    root.after(1000, update_labels)

def toggle_session_panel():
    if settings['hide_panel_setting']:  # Check the setting directly from the settings dictionary
        session_panel_frame.pack_forget()
    else:
        session_panel_frame.pack(expand=True, fill='both', padx=10, pady=0)

def open_settings():
    global settings_visible, settings_frame, width_entry, height_entry

    # Load settings from file
    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, use default settings
        print("Settings file not found. Using default settings.")
        settings = {
            'hide_panel_setting': 0,
            'transparency': 1.0,  # Default transparency
            'image_width': 1024,  # Default image width
            'image_height': 576,  # Default image height
        }

    if settings_visible:
        settings_frame.pack_forget()
        settings_visible = False
        root.geometry("450x140")
    else:
        settings_frame.pack(after=title_frame, fill=tk.X, padx=10, expand=True)
        settings_visible = True
        root.geometry("450x280")  # Adjusted geometry for when settings are visible

        # Populate settings entries with current settings
        width_entry.delete(0, tk.END)
        width_entry.insert(0, settings['image_width'])
        height_entry.delete(0, tk.END)
        height_entry.insert(0, settings['image_height'])

        # Call toggle_session_panel() after it's defined
        toggle_session_panel()

def increase_transparency():
    current_transparency = root.attributes('-alpha')
    new_transparency = min(current_transparency + 0.1, 1.0)
    root.attributes('-alpha', new_transparency)
    settings['transparency'] = new_transparency
    if image_visible:
        image_window.attributes('-alpha', new_transparency)

def decrease_transparency():
    current_transparency = root.attributes('-alpha')
    new_transparency = max(current_transparency - 0.1, 0.1)
    root.attributes('-alpha', new_transparency)
    settings['transparency'] = new_transparency
    if image_visible:
        image_window.attributes('-alpha', new_transparency)

def decrease_image_size():
    current_width = int(width_entry.get())
    current_height = int(height_entry.get())
    if current_width > 100 and current_height > 100:  # Ensure minimum size
        width_entry.delete(0, tk.END)
        height_entry.delete(0, tk.END)
        width_entry.insert(0, current_width - 50)
        height_entry.insert(0, current_height - 50)

def increase_image_size():
    current_width = int(width_entry.get())
    current_height = int(height_entry.get())
    width_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    width_entry.insert(0, current_width + 50)
    height_entry.insert(0, current_height + 50)

def load_settings():
    global settings
    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, use default settings
        print("Settings file not found. Using default settings.")
        settings = {
            'hide_panel_setting': 0,
            'transparency': 1.0,  # Default transparency
            'image_width': 1024,  # Default image width
            'image_height': 576,  # Default image height
        }

    # Update the displayed image size based on loaded settings
    global image_size
    image_size = (settings['image_width'], settings['image_height'])


def save_settings():
    settings['image_width'] = int(width_entry.get())
    settings['image_height'] = int(height_entry.get())
    settings['transparency'] = root.attributes('-alpha')  # Get current transparency value
    settings['hide_panel_setting'] = settings['hide_panel_setting']  # Update hide_panel_setting
    with open("settings.json", 'w') as file:
        json.dump(settings, file)

    # Update the displayed image size
    global image_size, image
    image_size = (settings['image_width'], settings['image_height'])

    # Apply changes to the currently displayed image
    if image_visible:
        resize_image(image, settings['image_width'], settings['image_height'])


# Initialize global variables for image functionality
image_window = None
image_label = None
image_size = (settings['image_width'], settings['image_height'])  # Default image size

def toggle_image():
    global image_visible, image_window, image_label, image_size, image

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the image
    image_path = os.path.join(script_dir, "Images", "Patterns", "Patterns.png")

    if image_visible:
        image_window.destroy()
        image_visible = False
    else:
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize(image_size, Image.LANCZOS)
            photo_image = ImageTk.PhotoImage(image)

            image_window = tk.Toplevel(root)
            image_window.geometry(f"{image_size[0]}x{image_size[1]}")
            image_window.overrideredirect(True)
            image_window.attributes('-alpha', settings['transparency'])  # Apply transparency
            image_window.attributes('-topmost', True)  # Always stay on top

            image_label = tk.Label(image_window, image=photo_image)
            image_label.pack(fill='both', expand=True)
            image_label.image = photo_image  # Keep a reference

            # Bindings for moving and resizing the image window
            image_window.bind("<ButtonPress-1>", start_move_image)
            image_window.bind("<ButtonRelease-1>", stop_move_image)
            image_window.bind("<B1-Motion>", on_move_image)
            image_window.bind("<ButtonPress-3>", start_resize)
            image_window.bind("<ButtonRelease-3>", stop_resize)
            image_window.bind("<B3-Motion>", on_resize)

            image_visible = True
        else:
            print("Image file not found.")

def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def on_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("450x140")
    root.configure(bg='#222222')
    root.overrideredirect(True)
    root.attributes('-topmost', True)

    settings_visible = False
    image_visible = False

    def close_app():
        root.destroy()

    def minimize_app(event=None):
        if settings_visible:
            settings_frame.pack_forget()
        root.update_idletasks()
        root.overrideredirect(False)
        root.iconify()

    def restore_app():
        root.overrideredirect(True)
        root.deiconify()
        if settings_visible:
            settings_frame.pack(after=title_frame, fill=tk.X, padx=10)

    title_frame = tk.Frame(root, bg='#222222', height=25)
    title_frame.pack(fill=tk.X)
    title_frame.pack_propagate(False)

    title_label = tk.Label(title_frame, text="Market Sessions", fg="#FFFFFF", bg='#222222', font=('Arial', 12))
    title_label.pack(side=tk.LEFT, padx=10)

    close_button = tk.Button(title_frame, text="X", command=close_app, bg="#FF0000", fg="#FFFFFF")
    close_button.pack(side=tk.RIGHT, padx=5)

    minimize_button = create_minimize_button(title_frame)

    settings_button = tk.Button(title_frame, text="Settings", command=open_settings, bg="#AAAAAA", fg="#FFFFFF")
    settings_button.pack(side=tk.RIGHT, padx=5)

    settings_frame = tk.Frame(root, bg='#333333')

    transparency_label = tk.Label(settings_frame, text="GUI Transparency", bg="#333333", fg="#FFFFFF")
    transparency_label.grid(row=0, column=0, padx=(10, 0), sticky='w')

    decrease_button = tk.Button(settings_frame, text="<", command=decrease_transparency, bg="#444444", fg="#FFFFFF")
    decrease_button.grid(row=0, column=1, padx=(10, 10))

    increase_button = tk.Button(settings_frame, text=">", command=increase_transparency, bg="#444444", fg="#FFFFFF")
    increase_button.grid(row=0, column=2, padx=(0, 10))

    width_label = tk.Label(settings_frame, text="Image Width:", bg="#333333", fg="#FFFFFF")
    width_label.grid(row=1, column=0, padx=(10, 0), sticky='w')

    width_entry = tk.Entry(settings_frame, bg="#444444", fg="#FFFFFF", width=10)
    width_entry.grid(row=1, column=1, padx=(10, 10), sticky='w')

    height_label = tk.Label(settings_frame, text="Image Height:", bg="#333333", fg="#FFFFFF")
    height_label.grid(row=2, column=0, padx=(10, 0), sticky='w')

    height_entry = tk.Entry(settings_frame, bg="#444444", fg="#FFFFFF", width=10)
    height_entry.grid(row=2, column=1, padx=(10, 10), sticky='w')

    decrease_size_button = tk.Button(settings_frame, text="-", command=decrease_image_size, bg="#AAAAAA", fg="#FFFFFF")
    decrease_size_button.grid(row=1, column=2, padx=(0, 10))

    increase_size_button = tk.Button(settings_frame, text="+", command=increase_image_size, bg="#AAAAAA", fg="#FFFFFF")
    increase_size_button.grid(row=2, column=2, padx=(0, 10))

    # Place the "Save" button
    save_button = tk.Button(settings_frame, text="Update Image Size", command=save_settings, bg="#666666", fg="#FFFFFF")
    save_button.grid(row=3, column=1, pady=(10, 0), sticky='W')

    # Place the "Toggle Image" button next to the "Save" button
    image_button = tk.Button(settings_frame, text="Toggle Image", command=toggle_image, bg="#AAAAAA", fg="#FFFFFF")
    image_button.grid(row=3, column=2, pady=(10, 0), sticky='W')

    session_panel_frame = tk.Frame(root, bg='#222222')
    setup_session_labels(session_panel_frame)

    root.protocol("WM_DELETE_WINDOW", close_app)
    root.bind("<Unmap>", lambda e: root.overrideredirect(False) if root.state() == 'iconic' else None)
    root.bind("<Map>", lambda e: restore_app() if root.state() == 'normal' else None)
    root.bind("<ButtonPress-1>", start_move)
    root.bind("<ButtonRelease-1>", stop_move)
    root.bind("<B1-Motion>", on_move)

    toggle_session_panel()
    update_labels()

    root.mainloop()


