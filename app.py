from tkinter import *

from tkinter import ttk

import tkinter as tk

import customtkinter as ctk

ctk.set_appearance_mode("light")

ctk.set_default_color_theme("blue")

root = ctk.CTk()

root.geometry("1440x780")

root.title("Recipe Tracker")


def showTable():
    table.pack(fill = 'both', expand = TRUE)

def removeItem():
    print("Removed!")

#Two Frames

# Tall Left Frame

leftFrame = ctk.CTkFrame(root, height = 700, width = 200, fg_color = 'gray', bg_color = 'gray')
leftFrame.pack(anchor = 'w', side = LEFT,fill = Y, expand = FALSE)

# Large Right Frame

otherFrame = ctk.CTkFrame(root, height = 700, width = 300, fg_color = 'transparent', bg_color = 'transparent')
otherFrame.pack(anchor = 's', side = BOTTOM, fill = BOTH, expand = TRUE)

# Header Frame

headerFrame = ctk.CTkFrame(root, height = 150, width = 300, fg_color = 'transparent', bg_color = 'transparent')
headerFrame.pack(anchor = 'n', side = TOP, fill = BOTH, expand = FALSE)


# Label for the Tall Left Frame 'Main Menu'

leftTitle = ctk.CTkLabel(master = leftFrame, text = "Main Menu", font = ctk.CTkFont(size = 40, weight = 'normal'))
leftTitle.pack(padx = 20, pady = 20)

# Buttons
recipeButton = ctk.CTkButton(master = leftFrame, text = "Recipes: ", command = showTable)
recipeButton.pack(pady = 20)


'''
When you add an item inside of the table, what happens?
1. You click on the add recipes button. 
2. A new window pops open demanding you to input information.
3. The new window closes by you saving it.
4. The new entry is included in the table.
'''

def addItem():
    print("Added!")

addRecipe = ctk.CTkButton(master = leftFrame, text = " + Add Recipe ", command = addItem)
addRecipe.pack(pady = 20)

#addWindow = ctk.CTkToplevel()

removeRecipe = ctk.CTkButton(master = leftFrame, text = " - Remove Recipe ", command = removeItem)

removeRecipe.pack(pady = 20)

# Treeview

# Define Columns

chosen_columns = ("name", "cuisine", "dateAdded")

# Define Table
table = ttk.Treeview(master = otherFrame, columns = chosen_columns, show = 'headings')

# Format our Columns

# Define Columns Names
table.heading('name', text = "Recipe Name")
table.heading('cuisine', text = "Cuisine")
table.heading('dateAdded', text = "Date Introduced")

# Search Bar

searchBar = ctk.CTkEntry(headerFrame, width = 300, height = 30, bg_color = 'transparent',
                          fg_color = 'transparent', placeholder_text = "Search")
searchBar.pack(padx = 20, pady = 20)


root.mainloop()
