import tkinter as tk
import json
import subprocess
import os
from PIL import Image, ImageTk

# Function to load the settings from the JSON file
def load_settings(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not a valid JSON file.")
        exit(1)

# Function to check if an image exists
def image_exists(image_path):
    if not os.path.isfile(image_path):
        print(f"Error: Image '{image_path}' does not exist.")
        return False
    return True

# Function to handle the tile click event
def on_tile_click(command):
    try:
        # Pass the command string directly to the shell for execution
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while executing command: {e}")

# Function to close the window when Escape key is pressed
def on_escape(event):
    root.quit()

# Set up the main window
root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")

# Bind the Escape key to close the app
root.bind("<Escape>", on_escape)

# Load settings from the JSON file
settings = load_settings('settings.json')

# Check if the background image exists
bg_image_path = settings.get('background_image')
if not bg_image_path or not image_exists(bg_image_path):
    print("Error: Background image does not exist.")
    exit(1)

# Load the background image
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas and place the background image on it
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bd=0, highlightthickness=0)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, image=bg_photo, anchor=tk.NW)

# Tile settings: Calculate positions
tile_size = settings["tile_size"]
tile_gap = settings["tile_gap"]
tiles = settings["tiles"]
tile_count = len(tiles)

# Calculate the horizontal and vertical positioning of the tiles
tile_x_start = (root.winfo_screenwidth() - (tile_count * tile_size + (tile_count - 1) * tile_gap)) // 2
tile_y_start = (root.winfo_screenheight() - tile_size) // 2  # Vertically center tiles

# Function to create buttons for tiles and associate the command
def create_tile_button(tile, x, y):
    tile_img_path = tile.get("image")
    if not tile_img_path or not image_exists(tile_img_path):
        print(f"Error: Tile image '{tile_img_path}' does not exist.")
        exit(1)

    tile_img = Image.open(tile_img_path)
    tile_img = tile_img.resize((tile_size, tile_size), Image.Resampling.LANCZOS)
    tile_photo = ImageTk.PhotoImage(tile_img)

    # Create a button with no border and flat relief style (no border)
    button = tk.Button(canvas, image=tile_photo, bd=0, highlightthickness=0, relief="flat", command=lambda: on_tile_click(tile["command"]))
    button.image = tile_photo  # Keep a reference to the image
    button.place(x=x, y=y)

# Create the tiles on the canvas
for index, tile in enumerate(tiles):
    # Calculate tile position
    tile_x = tile_x_start + index * (tile_size + tile_gap)
    tile_y = tile_y_start
    create_tile_button(tile, tile_x, tile_y)

# Start the Tkinter event loop
root.mainloop()
