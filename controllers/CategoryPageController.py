from controllers.DBUtil import * 
import tkinter as tk

def saveCategory(nameentry, feedbackLabel):
    name = nameentry.get().capitalize()
    valid = checkValidCategoryEntry(name)
    if valid == False:
        feedbackLabel.configure(text="")
        feedbackLabel.configure(text="Please fill out all required fields.")
    else: 
        print("saving")


def checkValidCategoryEntry(name):
    if len(name) == 0:
        return False
    else:
        return True


