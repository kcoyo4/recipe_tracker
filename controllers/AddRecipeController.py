from controllers.DBUtil import * 
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import shutil
import os

def add_recipes(name_text, prepTime_text, cookTime_text, serving_text, description_text, instruction_text): 
        image_path = upload_image()
        # Execute the SQL command to insert the recipe into the database
        if image_path:
            sql_command = "INSERT INTO Recipes(recipeName,imagePath, prepTime, cookTime, servingSize, descriptions, instructions) VALUES (%s, %s, %s, %s, %s, %s,%s)"
            values = (name_text.get(),image_path,prepTime_text.get(),cookTime_text.get(),serving_text.get(),description_text.get("1.0", tk.END),instruction_text.get("1.0", tk.END))
            cursor.execute(sql_command, values)
            # Commit the transaction
            connection.commit()
            # Clear the entry fields
            clear_fields()
            # Print a success message
            print("Recipe added successfully!")
        else:
            messagebox.showerror("Error", "Please upload an image before adding the recipe.")

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((300, 300))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)
        # image_label.configure(image=photo)
        # image_label.image = photo  # Keep a reference to avoid garbage collection
        save_image(file_path)
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
    
# clear out the text content after done with the submision 
def clear_fields(name_text, prepTime_text, cookTime_text, serving_text, description_text, instruction_text):
    name_text.delete(0, tk.END)
    prepTime_text.delete(0, tk.END)
    cookTime_text.delete(0, tk.END)
    serving_text.delete(0, tk.END) 
    description_text.delete(1.0, tk.END) 
    instruction_text.delete(1.0, tk.END)
    

def getCategories():
    query = "SELECT categoryName FROM Categories"
    # Execute the query
    cursor.execute(query)
    # Fetch all results from the executed query
    results = cursor.fetchall()
    # Extract the names from the results and store them in a list
    names = [row[0] for row in results]
    return names

def getAppliances():
    query = "SELECT applianceName FROM Appliances"
    # Execute the query
    cursor.execute(query)
    # Fetch all results from the executed query
    results = cursor.fetchall()
    # Extract the names from the results and store them in a list
    names = [row[0] for row in results]
    return names


def getIngredients(ID):
    query = "SELECT ingName FROM Ingredients WHERE ingtypeID = '" + ID + "'"
    # Execute the query
    cursor.execute(query)
    # Fetch all results from the executed query
    results = cursor.fetchall()
    # Extract the names from the results and store them in a list
    names = [row[0] for row in results]
    return names

def getUnits():
    query = "SELECT unitName FROM Units"
    # Execute the query
    cursor.execute(query)
    # Fetch all results from the executed query
    results = cursor.fetchall()
    # Extract the names from the results and store them in a list
    names = [row[0] for row in results]
    return names

def addCategory(category_combo,  category_listbox):
    category = category_combo.get()

    if category:
        entry = f"{category}"
        category_listbox.insert(tk.END, entry)
        # Clear input fields after adding
        category_listbox.set("")
    else:
        tk.messagebox.showwarning("Input Error", "Please fill in all fields.")


def addRecipeIngredient(ingredient_combo, quantity_entry, unit_combo, ingredient_listbox):
    ingredient = ingredient_combo.get()
    quantity = quantity_entry.get()
    unit = unit_combo.get()
    
    if ingredient and quantity and unit:
        entry = f"{ingredient} - {quantity} {unit}"
        ingredient_listbox.insert(tk.END, entry)
        # Clear input fields after adding
        ingredient_combo.set("")
        quantity_entry.delete(0, tk.END)
        unit_combo.set("")
    elif ingredient and quantity:
        entry = f"{ingredient} - {quantity}"
        ingredient_listbox.insert(tk.END, entry)
        ingredient_combo.set("")
        quantity_entry.delete(0, tk.END)
        unit_combo.set("")
    else:
        tk.messagebox.showwarning("Input Error", "Please fill in all fields.")

def addAppliance(appliance_combo,  appliance_listbox):
    appliance = appliance_combo.get()

    if appliance:
        entry = f"{appliance}"
        appliance_listbox.insert(tk.END, entry)
        # Clear input fields after adding
        appliance_listbox.set("")
    else:
        tk.messagebox.showwarning("Input Error", "Please fill in all fields.")