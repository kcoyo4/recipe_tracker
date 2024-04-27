from tkinter import *
from tkinter import ttk
import tkinter as tk
import customtkinter as ctk



from controllers.IngredientPageController import * 
from controllers.DBUtil import *
from controllers.AddRecipeController import * 
from controllers.CategoryPageController import * 
from controllers.AppliancePageController import * 

cursor = getCursor()
connection = getConnection()

#Setting up the GUI window & Frames
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("1440x780")
root.title("Recipe Tracker")

#Two Frames

# Tall Left Frame
leftFrame = ctk.CTkFrame(root, height = 700, width = 200, fg_color = 'gray', bg_color = 'gray')
leftFrame.pack(anchor = 'w', side = LEFT,fill = Y, expand = FALSE)

# Large Right Frame
mainFrame = ctk.CTkFrame(root, height = 700, width = 300, fg_color = 'transparent', bg_color = 'transparent')
mainFrame.pack(anchor = 's', side = BOTTOM, fill = BOTH, expand = TRUE)

# Header Frame
headerFrame = ctk.CTkFrame(root, height = 150, width = 300, fg_color = 'transparent', bg_color = 'transparent')
headerFrame.pack(anchor = 'n', side = TOP, fill = BOTH, expand = FALSE)

# Label for the Tall Left Frame 'Main Menu'
leftTitle = ctk.CTkLabel(master = leftFrame, text = "Main Menu", font = ctk.CTkFont(size = 40, weight = 'normal'))
leftTitle.pack(padx = 20, pady = 20)

# Search Bar
searchBar = ctk.CTkEntry(headerFrame, width = 300, height = 30, bg_color = 'transparent',
                        fg_color = 'transparent', placeholder_text = "Search")
searchBar.pack(padx = 20, pady = 20)

def clear_fields():
    name_text.delete(0, tk.END)
    prepTime_text.delete(0, tk.END)
    cookTime_text.delete(0, tk.END)
    serving_text.delete(0, tk.END) 
    description_text.delete(1.0, tk.END) 
    instruction_text.delete(1.0, tk.END)


def clearPage():
    for frame in mainFrame.winfo_children():
        frame.destroy()
    for frame in headerFrame.winfo_children():
        frame.pack_forget()

def add_recipes():
    
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

def addRecipePage():
    clearPage()
    global name_text, prepTime_text,cookTime_text,serving_text,description_text,instruction_text
  

    name_label = tk.Label(mainFrame, text = "Name of the recipe")
    name_text = ctk.CTkEntry(mainFrame)
    name_label.grid(row=0, column=0,padx=5)
    name_text.grid(row=0, column=1,padx=5)

    prepTime_label = tk.Label(mainFrame, text= "Preparation time")
    prepTime_text = ctk.CTkEntry(mainFrame, placeholder_text = "input minutes")
    prepTime_label.grid(row=1, column=0,padx=5,pady=5)
    prepTime_text.grid(row=1, column=1,padx=5,pady=5)

    cookTime_label = tk.Label(mainFrame, text= "Cook time")
    cookTime_text = ctk.CTkEntry(mainFrame, placeholder_text = "input minutes")
    cookTime_label.grid(row=2, column=0,padx=5,pady=5)
    cookTime_text.grid(row=2, column=1,padx=5,pady=5)

    serving_label = tk.Label(mainFrame, text= "Serving size")
    serving_text = ctk.CTkEntry(mainFrame, placeholder_text = "number of people")
    serving_label.grid(row=3, column=0,padx=5,pady=5)
    serving_text.grid(row=3, column=1,padx=5,pady=5)

    description_label = tk.Label(mainFrame, text= "Description")
    description_text = tk.Text(mainFrame, width= 60, height= 5)
    description_label.grid(row=4, column=0,padx=5,pady=5,sticky="nsew")
    description_text.grid(row=4, column=1,padx=5,pady=5,sticky="nsew")

    instruction_label = tk.Label(mainFrame, text= "Instruction")
    instruction_text = tk.Text(mainFrame, width= 60, height= 10)
    instruction_label.grid(row=5, column=0,padx=5,pady=5,sticky="nsew")
    instruction_text.grid(row=5, column=1,padx=5,pady=5,sticky="nsew")

    # image_label = tk.Label(mainFrame)
    # upload_button = ctk.CTkButton(mainFrame, text="Upload Image", command=lambda: upload_image())
    # # image_label.pack()
    # upload_button.pack(pady=10)
    # upload_button.grid(row=8, column=1,padx=5,pady=20)

    submit_button = ctk.CTkButton(mainFrame,text="Upload Image & Submit",command=add_recipes)
    submit_button.grid(row=11,column=1,padx=5,pady=20)

    # clear_button = ctk.CTkButton(mainFrame,text="Clear content", command = clear_fields)
    # clear_button.grid(row=10,column=1)


def addIngredientPage():
    clearPage()
    nameentry = ctk.CTkEntry(mainFrame, width = 140, height = 30, bg_color = 'transparent',
                          fg_color = 'transparent', placeholder_text = "Name")
    nameentry.pack(padx = 20, pady = 20, side=tk.LEFT)
    ingredientcategories = getIngredientCategories()
    combobox = ctk.CTkComboBox(mainFrame, values=ingredientcategories)
    combobox.set("Select an Ingredient Category")  # set initial value
    combobox.pack(padx=20, pady=10, side=tk.LEFT)
    feedbackLabel = ctk.CTkLabel(mainFrame, text="")
    savebutton = ctk.CTkButton(mainFrame, text = " Save ", command=lambda: saveIngredient(nameentry, combobox, feedbackLabel))
    savebutton.pack(padx=20, pady=10, side=tk.LEFT)
    feedbackLabel.pack(padx=20, pady=10, side=tk.LEFT)

def addCategoryPage():
    clearPage()
    nameentry = ctk.CTkEntry(mainFrame, width = 140, height = 30, bg_color = 'transparent',
                          fg_color = 'transparent', placeholder_text = "Name")
    feedbackLabel = ctk.CTkLabel(mainFrame, text="")
    savebutton = ctk.CTkButton(mainFrame, text = " Save ", command=lambda: saveCategory(nameentry, feedbackLabel))
    nameentry.pack(padx = 20, pady = 20, side=tk.LEFT)
    savebutton.pack(padx=20, pady=10, side=tk.LEFT)
    feedbackLabel.pack(padx=20, pady=10, side=tk.LEFT)

def addAppliancePage():
    clearPage()
    nameentry = ctk.CTkEntry(mainFrame, width = 140, height = 30, bg_color = 'transparent',
                          fg_color = 'transparent', placeholder_text = "Name")
    feedbackLabel = ctk.CTkLabel(mainFrame, text="")
    savebutton = ctk.CTkButton(mainFrame, text = " Save ", command=lambda: saveAppliance(nameentry, feedbackLabel))
    nameentry.pack(padx = 20, pady = 20, side=tk.LEFT)
    savebutton.pack(padx=20, pady=10, side=tk.LEFT)
    feedbackLabel.pack(padx=20, pady=10, side=tk.LEFT)

def removeRecipe():
    clearPage()
    print("Removed!")

def showTable():
    clearPage()
    searchBar.pack(padx = 20, pady = 20)
   
# BUTTONS
recipeButton = ctk.CTkButton(master = leftFrame, text = "Home ", command = showTable)
addRecipeButton = ctk.CTkButton(master = leftFrame, text = " + Add Recipe ", command = addRecipePage)
addIngredientButton = ctk.CTkButton(master = leftFrame, text = " + Add Ingredient ", command = addIngredientPage)
addCategoryButton = ctk.CTkButton(master = leftFrame, text = " + Add Category ", command = addCategoryPage)
addApplianceButton = ctk.CTkButton(master = leftFrame, text = " + Add Appliance ", command = addAppliancePage)
removeRecipeButton = ctk.CTkButton(master = leftFrame, text = " - Remove Recipe ", command = removeRecipe)


recipeButton.pack(pady = 20)
addRecipeButton.pack(pady = 20)
addIngredientButton.pack(pady = 20)
addCategoryButton.pack(pady = 20)
addApplianceButton.pack(pady = 20)
removeRecipeButton.pack(pady = 20)

root.mainloop()