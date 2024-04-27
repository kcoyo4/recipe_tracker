from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import shutil
import os

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((300, 300))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)
        # image_label.config(image=photo)
        # image_label.image = photo  # Keep a reference to avoid garbage collection
        # save_image(file_path)
        messagebox.showinfo("Success", "Image uploaded successfully!")
        return file_path
    else:
        return None

def save_image(file_path):
    save_dir = "saved_images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    filename = os.path.basename(file_path)
    shutil.copy(file_path, os.path.join(save_dir, filename))
    print("Image saved to:", os.path.join(save_dir, filename))
    return os.path.join(save_dir,filename)
    