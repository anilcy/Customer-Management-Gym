from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3



###########################################    DATABASE   #################################################

database_connect=sqlite3.connect("database.db")

cursor=database_connect.cursor()

database_connect.execute("CREATE TABLE IF NOT EXISTS members( Name TEXT, Surname TEXT, Number INT, BeginningDate COMPLEX, DueDate COMPLEX, RemainingDays INT)")
database_connect.commit()


def insert_treeview():
    database_connect=sqlite3.connect("database.db")
    cursor=database_connect.cursor()
    cursor.execute("SELECT rowid, * FROM members")

    for i in cursor:
        print(i)
        tree.insert("", "end" , iid=i[0], values=i[0:])
        print("Data inserted.")


def add_data():
    database_connect=sqlite3.connect("database.db")
    cursor=database_connect.cursor()
    
    cursor.execute("INSERT INTO members VALUES(?,?,?,?,?,?)",(name_entry.get(), surname_entry.get(), 
    number_entry.get(), bdate_entry.get(), ddate_entry.get(), rdays_entry.get()))
    
    database_connect.commit()
    database_connect.close()
    
    tree.delete(*tree.get_children())  # Clean up the treeview
    insert_treeview()                  # then put the updated database back in the treeview to be able to see the new data(member info) without reopen the app

def remove_one():
    
    selected = tree.selection()
    if selected:
        rowid = selected[0]
        tree.delete(rowid)

        database_connect=sqlite3.connect("database.db")
        cursor=database_connect.cursor()
        cursor.execute("DELETE from members WHERE rowid = ?", (rowid,))
        database_connect.commit()
        database_connect.close()
    

def update():
    database_connect=sqlite3.connect("database.db")
    cursor=database_connect.cursor()
    
    selected = tree.selection()
    rowid=selected[0]

    tree.item(selected, text="", values=(rowid, name_entry.get(), surname_entry.get(), 
    number_entry.get(), bdate_entry.get(), ddate_entry.get(), rdays_entry.get()))


    cursor.execute("UPDATE members SET Name = ?, Surname= ?, Number= ?, BeginningDate= ?, DueDate= ?, RemainingDays=?  WHERE rowid=?",( name_entry.get(), surname_entry.get(), 
    number_entry.get(), bdate_entry.get(), ddate_entry.get(), rdays_entry.get(), rowid,))
    
    database_connect.commit()
    database_connect.close()


def select_record(e):          # have to pass a random parameter to have it work properly
    name_entry.delete(0, "end")
    surname_entry.delete(0, "end")
    number_entry.delete(0, "end")
    bdate_entry.delete(0, "end")
    ddate_entry.delete(0, "end")
    rdays_entry.delete(0, "end")
	

    selected= tree.selection()
    values = tree.item(selected, "values")    

    name_entry.insert(0, values[1])
    surname_entry.insert(0, values[2])
    number_entry.insert(0, values[3])
    bdate_entry.insert(0, values[4])
    ddate_entry.insert(0, values[5])
    rdays_entry.insert(0, values[6])
	
#################################################################################################

def clear_text():
    for i in {name_entry,surname_entry,number_entry,bdate_entry,ddate_entry,rdays_entry}:
        i.delete(0, 'end') 

#########################################  GUI - TKINTER  #######################################


root = tk.Tk() 

root.iconbitmap("workout.ico")

root.title("MEMBER INFORMATION")
                                                                                                                 
root.geometry("954x500+500+250")                                                                                 
root.maxsize(width=954, height=500)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)



########################################       FRAMES      ####################################################


def show_frame(frame):
    frame.tkraise()

frame1=tk.Frame(root, bg="#487179")
frame2=tk.Frame(root, bg="#487179")

for frame in(frame1, frame2):
    frame.grid(row=0, column=0, sticky="nsew")


############################################        FRAME 1         ###################################################    


photo=tk.PhotoImage(file="dumbell.gif")

photo_button=tk.PhotoImage(file="forward_icon.png")
photo_button=photo_button.subsample(10,10)

photo_label=tk.Label(frame1, image=photo, bg="#487179")
photo_label.grid(row=0, column=0)


space_label=tk.Label(frame1, text="                                   ", bg="#487179")
frame1_button=tk.Button(frame1, text="Exit", height=3, width=7, bg="#BDC4C5", command= root.destroy)
space_label1=tk.Label(frame1, text="                                   ", bg="#487179")
frame1_button1=tk.Button(frame1, text="Members    ", image=photo_button, compound=RIGHT, height=45, width=130, bg="#BDC4C5", command=lambda:show_frame(frame2))

space_label.grid(row=0, column=1)
frame1_button.grid(row=0, column=2)
space_label1.grid(row=0, column=3)
frame1_button1.grid(row=0, column=4)


############################################        FRAME 2        ####################################################
tree_scroll = tk.Scrollbar(frame2)
tree_scroll.pack(side=RIGHT, fill=Y)


tree=ttk.Treeview(frame2, yscrollcommand=tree_scroll.set)

tree_scroll.config(command=tree.yview) 

 

tree ["columns"]=("id","Name","Surname","Number","Beginning Date","Ending Date","Remaining days")
tree ['show'] = 'headings' ## To get rid of the first empty column

tree.column("id", width="35", anchor=CENTER)
tree.column("Name", width="200", anchor=CENTER)
tree.column("Surname", width="200", anchor=CENTER)
tree.column("Number", width="200", anchor=CENTER)
tree.column("Beginning Date", width="100", anchor=CENTER)
tree.column("Ending Date", width="100", anchor=CENTER)
tree.column("Remaining days", width="100", anchor=CENTER)

tree.heading("id", text="id")
tree.heading("Name", text="Name")
tree.heading("Surname", text="Surname")
tree.heading("Number", text="Number")
tree.heading("Beginning Date", text="Beginning Date")
tree.heading("Ending Date", text="Ending Date")
tree.heading("Remaining days", text="Remaining days")


tree.pack()

#################################### FRAME 2 - Entrys

info_labelf=tk.LabelFrame(frame2, text="Member Informations", bg="#487179")
info_labelf.pack(fill="none", expand=True)


name_label=tk.Label(info_labelf,text="Name", bg="#487179")
surname_label=tk.Label(info_labelf,text="Surname", bg="#487179")
number_label=tk.Label(info_labelf,text="Number", bg="#487179")
bdate_label=tk.Label(info_labelf,text="Beginning Date", bg="#487179")
ddate_label=tk.Label(info_labelf,text="Ending Date", bg="#487179")
rdays_label=tk.Label(info_labelf,text="Remaining Days", bg="#487179")


name_label.grid(row=0, column=0)
surname_label.grid(row=0, column=1)
number_label.grid(row=0, column=2)
bdate_label.grid(row=2, column=0)
ddate_label.grid(row=2, column=1)
rdays_label.grid(row=2, column=2)



name_entry=tk.Entry(info_labelf, justify=CENTER)
surname_entry=tk.Entry(info_labelf, justify=CENTER)
number_entry=tk.Entry(info_labelf, justify=CENTER)
bdate_entry=tk.Entry(info_labelf, justify=CENTER)
ddate_entry=tk.Entry(info_labelf, justify=CENTER)
rdays_entry=tk.Entry(info_labelf, justify=CENTER)


name_entry.grid(row=1, column=0, padx=10, pady=10)
surname_entry.grid(row=1, column=1, padx=10, pady=10)
number_entry.grid(row=1, column=2, padx=10, pady=10)
bdate_entry.grid(row=3, column=0, padx=10, pady=10)
ddate_entry.grid(row=3, column=1, padx=10, pady=10)
rdays_entry.grid(row=3, column=2, padx=10, pady=10)


####################################  FRAME 2 - Buttons

option_labelf=tk.LabelFrame(frame2, text="Options", bg="#487179")
option_labelf.pack(side=BOTTOM)


newmember_button = tk.Button(option_labelf, text="New member", bg="#BDC4C5", command= add_data)
remove_button = tk.Button(option_labelf, text="Remove selected member", bg="#BDC4C5", command=remove_one)
update_button = tk.Button(option_labelf, text="Update selected", bg="#BDC4C5", command= update)
clear_button = tk.Button(option_labelf, text="Clear entry boxes", bg="#BDC4C5", command= clear_text)

newmember_button.grid(row=1, column=0, padx=10, pady=10)
remove_button.grid(row=1, column=1, padx=10, pady=10)
update_button.grid(row=1, column=2, padx=10, pady=10)
clear_button.grid(row=1, column=3, padx=10, pady=10)

photo_back= PhotoImage(file="back_icon.png")
photo_back_button = photo_back.subsample(10, 10)

back_button=tk.Button(frame2, image=photo_back_button, compound=LEFT, bg="#BDC4C5", command=lambda:show_frame(frame1))
back_button.pack(side=LEFT, expand=TRUE, ipadx=5)


####################################################

tree.bind("<ButtonRelease-1>", select_record)

insert_treeview()

show_frame(frame1)

root.mainloop()

