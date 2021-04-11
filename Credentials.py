#!/usr/bin/env python
# coding: utf-8

# Author: Cosimo Orlando
# Version: 1.0
#
# Purpose:
#       - This application has been developed to meet all those activities that require
#         the constant use of different credentials and updating of the same,
#         as in the smart-working. Rather than writing your credentials in a disorganized way,
#         it allows you to have an easily updated and organized DB that you can also comment on
#         (if you want to keep a note in mind).
#         The two buttons on the main screen allow you to directly copy the contents of
#         Username and Password, to easily paste these data into the interface you want,
#         without showing them the plain text (excellent system if you are in a call and
#         you cannot hide the window).
#
# Tested With:
#       - Python 3.8.5
#       - Windows 10
# Requires:
#       - Anaconda
# Dependecies:
#       - clipboard
#       - tkinter
#
# How To Istall the dependecies: (after Anaconda Python)
#       - pip install clipboard
#       - conda install -c anaconda tk


import tkinter as tk
from tkinter import messagebox
import clipboard
import json

root = tk.Tk()
root.title("Stupid Credential GUI")
root.geometry("300x240")

data = { "TEST":["usr", "psw", "comment"] }

try:
    with open('data.json') as json_file:
        data = json.load(json_file)
except:
    print("data.json load error\n")
    print("data.json proto creation...")
    
    with open("data.json", "w") as write_file:
        json.dump(data, write_file)
    write_file.close()
    
    if not bool(data):
        data = { "TEST":["usr", "psw", "comment"] }
    
    print("generation completed")

def usrCallBack():
    clipboard.copy(data[clicked.get()][0]) # User
    psw = clipboard.paste()

def pswCallBack():
    clipboard.copy(data[clicked.get()][1]) # Password
    psw = clipboard.paste()

def show(value):
    objlabel.config(text='\n'+value+'\n')

def saveToDB(value):
    drop.configure(state='disable')
    
    # update entry inside drop menu
    #print(value[0])
    #print(value[1])
    #print(value[2])
    
    #print(clicked.get())
    #print(data[clicked.get()][0])
    #print(data[clicked.get()][0])
    
    data[clicked.get()][0] = value[1]
    data[clicked.get()][1] = value[2]
    data[clicked.get()][2] = value[3]
    data[value[0]] = data.pop(clicked.get())
    
    # update drop menu list
    lst = list(data.keys())
    
    print(lst)
    
    # save data dict to json
    with open("data.json", "w") as write_file:
        json.dump(data, write_file)
    write_file.close()
    
    # remove default selection only, not the full list
    clicked.set('')
    
    # remove full list
    drop['menu'].delete(0, 'end')
    
    print(drop['menu'])
    
    for name in lst:
        drop['menu'].add_command(label=name, command=tk._setit(clicked, name))
    
    clicked.set(lst[0])
    
    drop.configure(state='normal')
    
    objlabel.config(text='\n'+clicked.get()+'\n')
    
    messagebox.showinfo("saving...", "DB saved!")
    
    print(clicked.get())

def newToDB():
    drop.configure(state='disable')
    
    data["NEW"] = ["usr", "psw", "comment"]
    
    # update drop menu list
    lst = list(data.keys())
    
    print(lst)
    
    # remove default selection only, not the full list
    clicked.set('')
    
    # remove full list
    drop['menu'].delete(0, 'end')
    
    #print(drop['menu'])
    
    for name in lst:
        drop['menu'].add_command(label=name, command=tk._setit(clicked, name))
    
    clicked.set(lst[-1])
    
    drop.configure(state='normal')
    
    objlabel.config(text='\n'+clicked.get()+'\n')
    
def editNewWindow():
    newWindow = tk.Toplevel(root)
    newWindow.title(clicked.get())
    newWindow.geometry("280x320")
    
    toplabel = tk.Label(newWindow, text ="Manage panel")
    
    itemlabel = tk.Label(newWindow, text="Item:")
    usrlabel = tk.Label(newWindow, text="User:")
    pswlabel = tk.Label(newWindow, text="Password:")
    cmtlabel = tk.Label(newWindow, text="Comment:")
    
    item_label = tk.Entry(newWindow, width=27)
    usr_label = tk.Entry(newWindow, width=27)
    psw_label = tk.Entry(newWindow, width=27)
    comment_txt = tk.Text(newWindow, height=10, width=20)
    
    item_label.insert(0, clicked.get())
    usr_label.insert(0, data[clicked.get()][0])
    psw_label.insert(0, data[clicked.get()][1])
    comment_txt.insert(tk.END, data[clicked.get()][2])
    
    # post data to saveToDB
    post = [item_label.get(), usr_label.get(), psw_label.get(), comment_txt.get("1.0", "end-1c")]
    
    def update_post(value):
        post[0] = item_label.get()
        post[1] = usr_label.get()
        post[2] = psw_label.get()
        post[3] = comment_txt.get("1.0", "end-1c")
        #print(post)
    
    # On Release update labels in post
    item_label.bind("<KeyRelease>", update_post)
    usr_label.bind("<KeyRelease>", update_post)
    psw_label.bind("<KeyRelease>", update_post)
    comment_txt.bind("<KeyRelease>", update_post)
    
    save_db = tk.Button(newWindow, text="Save to DB", padx = 15, command = lambda value=post: saveToDB(value))
    
    toplabel.grid(row=0, column=1)
    
    itemlabel.grid(row=1, column=0)
    item_label.grid(row=1, column=1)
    
    usrlabel.grid(row=2, column=0)
    usr_label.grid(row=2, column=1)
    
    pswlabel.grid(row=3, column=0)
    psw_label.grid(row=3, column=1)
    
    cmtlabel.grid(row=4, column=0)
    comment_txt.grid(row=4, column=1)
    
    tk.Label(newWindow, text ="").grid(row=5, column=1)
    save_db.grid(row=6, column=1, ipady=10)
    
def deleteFromDB():
    drop.configure(state='disable')
    
    data.pop(clicked.get())
    
    # update drop menu list
    lst = list(data.keys())
    
    print(lst)
    
    # save data dict to json
    with open("data.json", "w") as write_file:
        json.dump(data, write_file)
    write_file.close()
    
    # remove default selection only, not the full list
    clicked.set('')
    
    # remove full list
    drop['menu'].delete(0, 'end')
    
    print(drop['menu'])
    
    for name in lst:
        drop['menu'].add_command(label=name, command=tk._setit(clicked, name))
    
    # empty list exception fixing
    try:
        clicked.set(lst[0])
    except:
        print("empty list")
        lst = ["empty"]
        clicked.set(lst[0])
    
    drop.configure(state='normal')
    
    objlabel.config(text='\n'+clicked.get()+'\n')

lst = list(data.keys())
clicked = tk.StringVar()

# empty data list exception fixing
try:
    clicked.set(lst[0])
except:
    print("empty list")
    lst = ["empty"]
    clicked.set(lst[0])

# main menu configuration
drop = tk.OptionMenu(root, clicked, *lst, command=show)

objlabel = tk.Label(root, text='\n'+clicked.get()+'\n', font='Helvetica 18 bold', padx=70)
button_usr = tk.Button(root, text="usr", padx=15, command=usrCallBack)
button_pass = tk.Button(root, text="psw", padx=12, command=pswCallBack)


# cascade menu configuration
menu = tk.Menu(root)

submenu = tk.Menu(root, tearoff=0)
submenu.add_command(label="New", command=newToDB)
submenu.add_command(label="Edit", command=editNewWindow)
submenu.add_command(label="Delete", command=deleteFromDB)

menu.add_cascade(label="Credential", menu=submenu)

root.config(menu=menu)


# main menu design
root.grid_columnconfigure(1, weight=1)

drop.grid(row=1, column=1)
objlabel.grid(row=2, column=1)
button_usr.grid(row=3, column=1)
button_pass.grid(row=4, column=1)


root.mainloop()