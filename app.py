from tkinter import *
from tkinter import ttk
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk


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
root.geometry("1430x980")
root.title("Recipe Tracker")

#Two Frames

# Tall Left Frame
leftFrame = ctk.CTkFrame(root, height = 700, width = 500, fg_color = 'gray', bg_color = 'gray')
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


def image_click(even,image_path):
    clearPage()
    print("Image clicked")
    frame_image = LabelFrame(mainFrame, text="the image of the recipe",padx=20,pady=20)
    image = Image.open(image_path)
    image.thumbnail((300, 300))
    image_one = ImageTk.PhotoImage(image)

    image_label = tk.Label(frame_image, image=image_one)
    image_label.image = image_one
    image_label.pack(padx=20,pady=20)

    frame_image.grid(row = 0, column=0, padx=10,pady=10)


    frame_info = LabelFrame(mainFrame,text="the info of a recipe",padx=20,pady=20)
    frame_info.grid(row = 0, column=1, padx=10,pady=10)

    try:
        # Fetch recipe information from the database based on the image path
        cursor.execute("SELECT * FROM Recipes WHERE imagePath = %s", (image_path,))
        recipe_info = cursor.fetchone()
        if recipe_info:
            # Extract recipe information
            recipe_name = ctk.CTkLabel(frame_info, text = recipe_info[1],font = ctk.CTkFont(size = 30, weight = 'normal'))
            recipe_name.grid(row = 0, column=0)

            d_label = ctk.CTkLabel(frame_info, text = "Description")
            d_label.grid(row = 1, column=0)
            description = ctk.CTkLabel(frame_info, text = recipe_info[6])
            description.grid(row = 2, column=0, columnspan = 3,rowspan = 4)

            p_label = ctk.CTkLabel(frame_info, text = "Prep Time: ")
            p_label.grid(row = 7, column=0)
            prep_time = recipe_info[3]
            prep_l= ctk.CTkLabel(frame_info, text = prep_time)
            prep_l.grid(row = 7, column=1)

            c_label = ctk.CTkLabel(frame_info, text = "Cook Time: ")
            c_label.grid(row = 8, column=0)
            cook_time = recipe_info[4]
            cook_l = ctk.CTkLabel(frame_info, text = cook_time)
            cook_l.grid(row = 8, column=1)
         
            Total_Time = prep_time + cook_time
            t_label = ctk.CTkLabel(frame_info, text = "Total Time: ")
            t_label.grid(row = 9, column=0)
            total_l = ctk.CTkLabel(frame_info, text = Total_Time)
            total_l.grid(row = 9, column=1)
            

            instr_label = ctk.CTkLabel(frame_info, text = "Instruction")
            instr_label.grid(row=10,column = 0)
            in_label = ctk.CTkLabel(frame_info, text = recipe_info[7])
            in_label.grid(row=11,column = 0, rowspan = 9)

            # # Display the recipe information
            print("Recipe Name:", recipe_name)
            # print("Cook Time:", cook_time)
            # print("Preparation Time:", prep_time)
            # print("Description:", description)
            # print("Instructions:", instructions)
        else:
            print("Recipe not found")
    except Exception as e:
        print(f"Error fetching recipe information: {e}")













def display_recipes():
    clearPage()
    # Search Bar
    searchBar = ctk.CTkEntry(headerFrame, width = 300, height = 30, bg_color = 'transparent',
                            fg_color = 'transparent', placeholder_text = "Search")
    searchBar.pack(padx = 20, pady = 20)


    cursor.execute("SELECT * FROM Recipes")
    result = cursor.fetchall()
    row_even_num = 0 # for display the image of each recipe
    row_odd_num = 1  # for display the name of the each recipe
    column_num = 0
    gap_size = 15
    
    

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
            



# clear out the text content after done with the submision 
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
    description_text = tk.Text(mainFrame, width= 60, height= 10)
    description_label.grid(row=4, column=0,padx=5,pady=5,sticky="nsew")
    description_text.grid(row=4, column=1,padx=5,pady=5,sticky="nsew")

    instruction_label = tk.Label(mainFrame, text= "Instruction")
    instruction_text = tk.Text(mainFrame, width= 60, height= 20)
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
recipeButton = ctk.CTkButton(master = leftFrame, text = "Home ", command = display_recipes)
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