from tkinter import *
from tkinter import ttk
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from CTkListbox import *

from controllers.IngredientPageController import * 
from controllers.DBUtil import *
from controllers.AddRecipeController import * 
from controllers.CategoryPageController import * 
from controllers.AppliancePageController import *
from controllers.individualRecipePageController import * 

cursor = getCursor()
connection = getConnection()

#Setting up the GUI window & Frames
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("1440x780")
root.title("Recipe Tracker")

#Two Frames
base_font = ctk.CTkFont(family="Poplar Std")
# Tall Left Frame
leftFrame = ctk.CTkFrame(root, height = 700, width = 500, fg_color = 'gray', bg_color = 'gray')
leftFrame.pack(anchor = 'w', side = LEFT,fill = Y, expand = FALSE)
# Right Frame
rightFrame = ctk.CTkFrame(root, height=700, width=200, fg_color='light gray', bg_color='light gray')
rightFrame.pack(anchor='e', side=RIGHT, fill=Y, expand=FALSE)
# Group Window
groupWindow = ctk.CTkFrame(root, height = 700, width = 500, fg_color = 'transparent', bg_color = 'transparent')
groupWindow.pack(anchor = 'n', fill = BOTH, expand = TRUE)

# Main Window
mainFrame = ctk.CTkFrame(groupWindow, height = 700, width = 300, fg_color = 'transparent', bg_color = 'transparent')
mainFrame.pack(anchor = 's', side = BOTTOM, fill = BOTH, expand = TRUE)

# Header Frame
headerFrame = ctk.CTkFrame(groupWindow, height = 150, width = 300, fg_color = 'transparent', bg_color = 'transparent')
headerFrame.pack(anchor = 'n', side = TOP, fill = BOTH, expand = FALSE)

# Label for the Tall Left Frame 'Main Menu'
leftTitle = ctk.CTkLabel(master = leftFrame, text = "ReciPedia", font = ctk.CTkFont(family="Calibri", size = 40, weight = 'normal'))
leftTitle.pack(padx = 20, pady = 20)



def image_click(even,image_path):
    clearPage()
    print("Image clicked")
    frame_left = ctk.CTkFrame(mainFrame, fg_color = 'transparent', bg_color = 'transparent')
    frame_left.grid(row = 0, column=0,padx=10,pady=10)

    frame_image = LabelFrame(frame_left, padx=20,pady=20)
    frame_image.grid(row = 0, column=0,padx=10,pady=10)

    image = Image.open(image_path)
    image.thumbnail((300, 300))
    image_one = ImageTk.PhotoImage(image)

    image_label = tk.Label(frame_image, image=image_one)
    image_label.image = image_one
    image_label.pack(padx=20,pady=20)

    frame_bottominfo = LabelFrame(frame_left,padx=20,pady=20)
    frame_bottominfo.grid(row = 1, column=0,rowspan=3, padx=10,pady=10)

    frame_info = LabelFrame(mainFrame,padx=20,pady=20)
    frame_info.grid(row = 0, column=1,rowspan=3, padx=10,pady=10)

    try:
        # Fetch recipe information from the database based on the image path
        cursor.execute("SELECT * FROM Recipes WHERE imagePath = %s", (image_path,))
        recipe_info = cursor.fetchone()
        if recipe_info:
            # Extract recipe information
            recipeID = recipe_info[0]
            recipe_name = ctk.CTkLabel(frame_info, text = recipe_info[1],font = ctk.CTkFont(size = 30, weight = 'normal'))
            recipe_name.grid(row = 0, column=0)

            d_label = ctk.CTkLabel(frame_info, text = "Description", width = 40,font=("Helvetica", 15))
            d_label.grid(row = 1, column=0)
            description = tk.Text(frame_info, wrap=tk.WORD, height=5, width=60, font=("Helvetica", 15))
            description.insert(tk.END,recipe_info[6])
            description.configure(state="disabled")
            description.grid(row = 2, column=0, columnspan = 3,rowspan = 4)

            prep_time = recipe_info[3]
            p_label = ctk.CTkLabel(frame_info, text = "Prep Time:     " + str(prep_time),font=("Helvetica", 15))
            p_label.grid(row = 7, column=0)

            cook_time = recipe_info[4]
            c_label = ctk.CTkLabel(frame_info, text = "Cook Time:     " + str(cook_time),font=("Helvetica", 15))
            c_label.grid(row = 8, column=0)
            
            Total_Time = prep_time + cook_time
            t_label = ctk.CTkLabel(frame_info, text = "Total Time:     " + str(Total_Time),font=("Helvetica", 15))
            t_label.grid(row = 9, column=0)
            
            s_label = ctk.CTkLabel(frame_info, text = "Serving Size:     " + str(recipe_info[5]),font=("Helvetica", 15))
            s_label.grid(row = 10, column=0)
            
            instr_label = ctk.CTkLabel(frame_info, text = "Instruction",font=("Helvetica", 15))
            instr_label.grid(row=11,column = 0)
            instruction = tk.Text(frame_info, wrap=tk.WORD,height=20,width=60,font=("Helvetica", 15))           
            instruction.insert(tk.END,recipe_info[7])
            instruction.configure(state="disabled")
            instruction.grid(row=12,column = 0, rowspan = 9)

            categories = getRecipeCategories(recipeID)
            category_text = ", ".join([getCategoryName(c) for c in categories])
            categorylabel = ctk.CTkLabel(frame_bottominfo, text="Categories: " + category_text)
            categorylabel.grid(row=0, column=0, padx=5, pady=5)

            appliances = getRecipeAppliances(recipeID)
            appliance_text = ", ".join([getApplianceName(a) for a in appliances])
            appliancelabel = ctk.CTkLabel(frame_bottominfo, text="Appliances Needed: " + appliance_text)
            appliancelabel.grid(row=1, column=0, padx=5, pady=5)

            ingredients = getRecipeIngredients(recipeID)
            listbox_label = ctk.CTkLabel(frame_bottominfo, text="Ingredients:")
            listbox_label.grid(row=2, column=0, padx=5, pady=5)
            ingredient_listbox = CTkListbox(frame_bottominfo, height=250, width=200)
            for ingredient, quantity, unit in ingredients:
                ingredient_listbox.insert(tk.END, f"{ingredient} - {quantity} {unit}")
            ingredient_listbox.grid(row=3, column=0, padx=5, pady=5)
        else:
            print("Recipe not found")
    except Exception as e:
        print(f"Error fetching recipe information: {e}")

def display_recipes():
    clearPage()
    def init():
        cursor.execute("SELECT * FROM Recipes")
        result = cursor.fetchall()
        displayResult(result)
    
    def displayHeader():
        headerFrame.pack()
        searchBar = ctk.CTkEntry(headerFrame, width = 300, height = 30, bg_color = 'transparent',
                                fg_color = 'transparent', placeholder_text = "Search")
        searchBar.grid(row=0, column=0, padx = 20, pady = 20)
        searchButton = ttk.Button(headerFrame, text="Search", command=lambda: getNameSearch(searchBar))
        searchButton.grid(row=0, column=1,padx=5, pady=5)

    def displayRight():
        rightFrame.configure(height=700, width=200, fg_color='light gray', bg_color='light gray')

        spacer = ctk.CTkLabel(rightFrame, text="More Search Options:")
        spacer.grid(row=0, column=0, padx=5, pady=20)

        category_label = ctk.CTkLabel(rightFrame, text="Category:")
        category_label.grid(row=1, column=0, padx=5, pady=5)

        category_options = getCategories()
        category_combo = ctk.CTkComboBox(rightFrame, values=category_options, state="readonly")
        category_combo.grid(row=2, column=0, padx=5, pady=5)

        categorySelect_button = ttk.Button(rightFrame, text="Search", command=lambda: getCategorySearch(category_combo))
        categorySelect_button.grid(row=2, column=1, padx=5, pady=5)
    
        #Appliance Selection
        appliance_label = ctk.CTkLabel(rightFrame, text="Appliance:")
        appliance_label.grid(row=3, column=0, padx=5, pady=5)

        appliance_options = getAppliances()
        appliance_combo = ctk.CTkComboBox(rightFrame, values=appliance_options, state="readonly")
        appliance_combo.grid(row=4, column=0, padx=5, pady=5)

        applianceSelect_button = ttk.Button(rightFrame, text="Search", command=lambda: getApplianceSearch(appliance_combo))
        applianceSelect_button.grid(row=4, column=1, padx=5, pady=5)
        
        duration_label = ctk.CTkLabel(rightFrame, text = "Duration (mins):")
        duration_text = ctk.CTkEntry(rightFrame)
        duration_label.grid(row=5, column=0,padx=5, pady=5)
        duration_text.grid(row=6, column=0,padx=5, pady=5)
        durationSelect_button = ttk.Button(rightFrame, text="Search", command=lambda: getDurationSearch(duration_text))
        durationSelect_button.grid(row=6, column=1, padx=5, pady=5)

        # Ingredient Category Selection
        ingcategory_label = ctk.CTkLabel(rightFrame, text="Ingredient Type:")
        ingcategory_label.grid(row=7, column=0, padx=5, pady=5)

        ingredientcategory_options = getIngredientCategories()
        ingcategory_combo = ctk.CTkComboBox(rightFrame, values=ingredientcategory_options, state="readonly")
        ingcategory_combo.grid(row=8, column=0, padx=5, pady=5)

        ingredientSelectionDisplay_button = ttk.Button(rightFrame, text="Select", command=lambda: displayIngSelection(ingcategory_combo))
        ingredientSelectionDisplay_button.grid(row=8, column=1, padx=5, pady=0)

    def displayIngSelection(combobox):
            category = combobox.get()
            if len(category) > 0:
                icID = str(getIngCatID(category))
                # Ingredient selection
                ingredient_label = ctk.CTkLabel(rightFrame, text="Ingredient:")
                ingredient_label.grid(row=9, column=0, padx=5, pady=5)

                ingredient_options = getIngredients(icID)
                ingredient_combo = ctk.CTkComboBox(rightFrame, values=ingredient_options, state="readonly")
                ingredient_combo.grid(row=10, column=0, padx=5, pady=5)
                ingredientSelect_button = ttk.Button(rightFrame, text="Search", command=lambda: getIngredientSearch(ingredient_combo))
                ingredientSelect_button.grid(row=10, column=1, padx=5, pady=5)

    def getNameSearch(searchBar):
        answer = searchBar.get()
        if answer == "":
            cursor.execute("SELECT * FROM Recipes")
            result = cursor.fetchall()
            print("None")
            displayResult(result)

        else:
            sqlStatement = "SELECT * FROM Recipes WHERE recipeName LIKE '%" + answer + "%'"
            cursor.execute(sqlStatement)
            result = cursor.fetchall()
            print("button")
            clearPage()
            displayResult(result)

    def getCategorySearch(combo):
        category = combo.get()
        categoryID = getCategoryID(category)
        query = (
            "SELECT Recipes.* FROM Recipes "
            + "INNER JOIN RecipeCategories ON Recipes.recipeID = RecipeCategories.recipeID "
            + "INNER JOIN Categories ON RecipeCategories.categoryID = Categories.categoryID "
            + "WHERE Categories.categoryID = %s"
        )
        cursor.execute(query, (categoryID,))
        result = cursor.fetchall()
        displayResult(result)

    def getApplianceSearch(combo):
        appliance = combo.get()
        applianceID = getApplianceID(appliance)
        query = (
            "SELECT Recipes.* FROM Recipes "
            + "INNER JOIN RecipeAppliances ON Recipes.recipeID = RecipeAppliances.recipeID "
            + "INNER JOIN Appliances ON RecipeAppliances.applianceID = Appliances.applianceID "
            + "WHERE Appliances.applianceID = %s"
        )
        cursor.execute(query, (applianceID,))
        result = cursor.fetchall()
        displayResult(result)

    def getIngredientSearch(combo):
        ingredient = combo.get()
        ingID = getIngredientID(ingredient)
        query = (
            "SELECT Recipes.* FROM Recipes "
            + "INNER JOIN RecipeIngredients ON Recipes.recipeID = RecipeIngredients.recipeID "
            + "INNER JOIN Ingredients ON RecipeIngredients.ingID = Ingredients.ingID "
            + "WHERE Ingredients.ingID = %s"
        )
        cursor.execute(query, (ingID,))
        result = cursor.fetchall()
        displayResult(result)

    def getDurationSearch(entry):
        duration = entry.get()
        if int(duration):
            query = "SELECT * FROM Recipes WHERE (prepTime + cookTime) <= %s"
            cursor.execute(query, (duration,))
            result = cursor.fetchall()
            clearPage()
            displayResult(result)
        else:
            messagebox.showerror("Error", f"Please input time in minutes.")

    def displayResult(result):
        clearPage()
        displayHeader()
        displayRight()
        row_even_num = 0 # for display the image of each recipe
        row_odd_num = 1  # for display the name of the each recipe
        column_num = 0
        gap_size = 15
        if result:
            for x in result:
                if column_num <= 2:
                    image_path = x[2]
                    try:
                        image = Image.open(image_path)
                        image.thumbnail((200, 200))
                        image_one = ImageTk.PhotoImage(image)

                        image_label = tk.Label(mainFrame, image=image_one)
                        image_label.image = image_one
                        image_label.grid(row=row_even_num, column=column_num, padx=gap_size,pady=gap_size)

                        image_label.bind("<Button-1>", lambda event, path=image_path: image_click(event, path))

                        name_label = tk.Label(mainFrame,text=x[1])
                        name_label.grid(row=row_odd_num, column=column_num)

                    except Exception as e:
                        print(f"Error opening image: {e}")
                else:
                    column_num = 0
                    row_even_num += 2
                    row_odd_num +=2
                    image_path = x[2]
                    try:
                        image = Image.open(image_path)
                        image.thumbnail((200, 200))
                        image_one = ImageTk.PhotoImage(image)

                        image_label = tk.Label(mainFrame, image=image_one)
                        image_label.image = image_one
                        image_label.grid(row=row_even_num, column=column_num)

                        image_label.bind("<Button-1>", lambda event, path=image_path: image_click(event, path))

                        name_label = tk.Label(mainFrame,text=x[1])
                        name_label.grid(row=row_odd_num, column=column_num)
                    except Exception as e:
                        print(f"Error opening image: {e}")
                
                column_num += 1
        else:
            label = tk.Label(mainFrame,text="No results")
            label.pack()
         
    init()
    displayHeader()
    displayRight()
            
def clearPage():
    for frame in mainFrame.winfo_children():
        frame.destroy()
    for frame in headerFrame.winfo_children():
        frame.pack_forget()
    headerFrame.pack_forget()
    for frame in rightFrame.winfo_children():
        frame.destroy()
    rightFrame.configure(height=0, width=0)

def addRecipePage():

    clearPage()
    name_label = ctk.CTkLabel(mainFrame, text = "Name of the recipe")
    name_text = ctk.CTkEntry(mainFrame)
    name_label.grid(row=0, column=0,padx=5, pady=20)
    name_text.grid(row=0, column=1,padx=5, pady=20)

    prepTime_label = ctk.CTkLabel(mainFrame, text= "Preparation time")
    prepTime_text = ctk.CTkEntry(mainFrame, placeholder_text = "input minutes")
    prepTime_label.grid(row=1, column=0,padx=5,pady=5)
    prepTime_text.grid(row=1, column=1,padx=5,pady=5)

    cookTime_label = ctk.CTkLabel(mainFrame, text= "Cook time")
    cookTime_text = ctk.CTkEntry(mainFrame, placeholder_text = "input minutes")
    cookTime_label.grid(row=2, column=0,padx=5,pady=5)
    cookTime_text.grid(row=2, column=1,padx=5,pady=5)

    serving_label = ctk.CTkLabel(mainFrame, text= "Serving size")
    serving_text = ctk.CTkEntry(mainFrame, placeholder_text = "number of people")
    serving_label.grid(row=3, column=0,padx=5,pady=5)
    serving_text.grid(row=3, column=1,padx=5,pady=5)

    description_label = ctk.CTkLabel(mainFrame, text= "Description")
    description_text = ctk.CTkTextbox(mainFrame, width= 60, height= 150)
    description_label.grid(row=4, column=0,padx=5,pady=5,sticky="nsew")
    description_text.grid(row=4, column=1,padx=5,pady=5,sticky="nsew")

    instruction_label = ctk.CTkLabel(mainFrame, text= "Instruction")
    instruction_text = ctk.CTkTextbox(mainFrame, width= 60, height= 150)
    instruction_label.grid(row=5, column=0,padx=5,pady=5,sticky="nsew")
    instruction_text.grid(row=5, column=1,padx=5,pady=5,sticky="nsew")

    # Category Selection
    category_label = ctk.CTkLabel(mainFrame, text="Category:")
    category_label.grid(row=0, column=2, padx=5, pady=5)

    category_options = getCategories()
    category_combo = ctk.CTkComboBox(mainFrame, values=category_options, state="readonly")
    category_combo.grid(row=0, column=3, padx=5, pady=5)

    cListbox_label = ctk.CTkLabel(mainFrame, text="Added Categories:")
    cListbox_label.grid(row=1, column=2, padx=5, pady=5)
    category_listbox = CTkListbox(mainFrame, height=60, width=150)
    category_listbox.grid(row=1, column=3, padx=5, pady=5)

    categorySelect_button = ttk.Button(mainFrame, text="Select", command=lambda: addCategory(category_combo, category_listbox))
    categorySelect_button.grid(row=0, column=4, padx=5, pady=5)

    # Ingredient Category Selection
    
    # ingredientadd_label = ctk.CTkLabel(mainFrame, text="Select an Ingredient Category to begin adding Ingredients.")
    # ingredientadd_label.grid(row=0, column=2, padx=5, pady=5)
    ingcategory_label = ctk.CTkLabel(mainFrame, text="Ingredient Type:")
    ingcategory_label.grid(row=2, column=2, padx=5, pady=5)

    ingredientcategory_options = getIngredientCategories()
    ingcategory_combo = ctk.CTkComboBox(mainFrame, values=ingredientcategory_options, state="readonly")
    ingcategory_combo.grid(row=2, column=3, padx=5, pady=5)

    ingredientSelectionDisplay_button = ttk.Button(mainFrame, text="Select", command=lambda:displayIngredientSelection(ingcategory_combo, ingredient_listbox))
    ingredientSelectionDisplay_button.grid(row=2, column=4, padx=5, pady=5)
    
    listbox_label = ctk.CTkLabel(mainFrame, text="Added Ingredients:")
    listbox_label.grid(row=4, column=2, padx=5, pady=5)
    ingredient_listbox = CTkListbox(mainFrame, height=250, width=200)
    ingredient_listbox.grid(row=4, column=3, padx=5, pady=5)

    #Appliance Selection
    appliance_label = ctk.CTkLabel(mainFrame, text="Appliance:")
    appliance_label.grid(row=5, column=2, padx=5, pady=5)

    appliance_options = getAppliances()
    appliance_combo = ctk.CTkComboBox(mainFrame, values=appliance_options, state="readonly")
    appliance_combo.grid(row=5, column=3, padx=5, pady=5)

    applianceSelect_button = ttk.Button(mainFrame, text="Select", command=lambda: addAppliance(appliance_combo,  appliance_listbox))
    applianceSelect_button.grid(row=5, column=4, padx=5, pady=5)

    appliance_label = ctk.CTkLabel(mainFrame, text="Added Appliances:")
    appliance_label.grid(row=6, column=2, padx=5, pady=5)
    appliance_listbox = CTkListbox(mainFrame, height=100, width=200)
    appliance_listbox.grid(row=6, column=3, padx=5, pady=5)

    # setImagePath()
    # image_label = ctk.CTkLabel(mainFrame, text ="")
    # upload_button = ctk.CTkButton(mainFrame, text="Upload Image", command=lambda: upload_image(image_label))
    # image_label.grid(row=1, column=2,padx=5,pady=20)
    # upload_button.grid(row=2, column=2,padx=5,pady=20)

    submit_button = ctk.CTkButton(mainFrame,text="Upload Image & Submit", command=lambda:saveRecipe(name_text, prepTime_text, cookTime_text, serving_text, description_text, instruction_text, category_listbox, ingredient_listbox, appliance_listbox))
    submit_button.grid(row=0,column=6,padx=5,pady=20)

    # clear_button = ctk.CTkButton(mainFrame,text="Clear content", command = clear_fields)
    # clear_button.grid(row=10,column=1)
    
def displayIngredientSelection(combobox, ingredient_listbox):
    category = combobox.get()
    if len(category) > 0:
        icID = str(getIngCatID(category))
        # Ingredient selection
        ingredient_label = ctk.CTkLabel(mainFrame, text="Ingredient:")
        ingredient_label.grid(row=3, column=2, padx=5, pady=5)

        ingredient_options = getIngredients(icID)
        ingredient_combo = ctk.CTkComboBox(mainFrame, values=ingredient_options, state="readonly")
        ingredient_combo.grid(row=3, column=3, padx=5, pady=5)

        # Quantity input
        quantity_label = ctk.CTkLabel(mainFrame, text="Quantity:")
        quantity_label.grid(row=3, column=4, padx=5, pady=5)

        quantity_entry = ctk.CTkEntry(mainFrame)
        quantity_entry.grid(row=3, column=5, padx=5, pady=5)

        # Unit selection
        unit_label = ctk.CTkLabel(mainFrame, text="Unit:")
        unit_label.grid(row=3, column=6, padx=5, pady=5)

        unit_options = getUnits()
        unit_combo = ctk.CTkComboBox(mainFrame, values=unit_options, state="readonly")
        unit_combo.grid(row=3, column=7, padx=5, pady=5)

        add_button = ttk.Button(mainFrame, text="Add", command=lambda: addRecipeIngredient(ingredient_combo, quantity_entry, unit_combo, ingredient_listbox))
        add_button.grid(row=3, column=8, padx=5, pady=5)

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
   
# BUTTONS
recipeButton = ctk.CTkButton(master = leftFrame, text = "Home ", command = display_recipes)
addRecipeButton = ctk.CTkButton(master = leftFrame, text = " + Add Recipe ", command = addRecipePage)
addIngredientButton = ctk.CTkButton(master = leftFrame, text = " + Add Ingredient ", command = addIngredientPage)
addCategoryButton = ctk.CTkButton(master = leftFrame, text = " + Add Category ", command = addCategoryPage)
addApplianceButton = ctk.CTkButton(master = leftFrame, text = " + Add Appliance ", command = addAppliancePage)

recipeButton.pack(pady = 20)
addRecipeButton.pack(pady = 20)
addIngredientButton.pack(pady = 20)
addCategoryButton.pack(pady = 20)
addApplianceButton.pack(pady = 20)
#Setting up
display_recipes()
root.mainloop()