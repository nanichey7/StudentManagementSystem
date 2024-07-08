from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas as pd  # Ensure you have pandas installed

# Global variables for current time and date
currentTime = ''
date = ''

# functions
def clock():
    global currentTime, date
    time_ = time.strftime('%H:%M:%S')
    date_ = time.strftime('%d/%m/%Y')
    datetimeLabel.config(text=f'Date: {date_}\nTime: {time_}')
    datetimeLabel.after(1000, clock)
    currentTime = time_
    date = date_

def iexit():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()

def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv',
                                       filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
    if not url:
        return  # User cancelled the save dialog

    indexing = studentTable.get_children()
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    # Creating a DataFrame with the fetched data
    table = pd.DataFrame(newlist, columns=['ID', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'DOB', 'Added Date', 'Added Time'])

    # Saving the DataFrame to CSV
    try:
        table.to_csv(url, index=False)
        messagebox.showinfo('Success', 'Data is saved successfully')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred while saving the data: {e}')

def toplevel_data(title, button_text, command):
    global idEntry, phoneEntry, nameEntry, emailEntry, addressEntry, DOBEntry, genderEntry, screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    idLabel = Label(screen, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    DOBLabel = Label(screen, text='DOB', font=('times new roman', 20, 'bold'))
    DOBLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    DOBEntry = Entry(screen, font=('roman', 15), width=24)
    DOBEntry.grid(row=6, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)

def update_data():
    query = 'update student set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s where id=%s'
    mycursor.execute(query, (nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), DOBEntry.get(), date, currentTime, idEntry.get()))
    con.commit()
    messagebox.showinfo('Success', f'ID {idEntry.get()} is modified successfully', parent=screen)
    screen.destroy()
    show_student()

def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def delete_student():
    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, (content_id,))
    con.commit()
    messagebox.showinfo('Deleted', f'This {content_id} is deleted successfully')
    show_student()

def search_data():
    query = 'select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query, (idEntry.get(), nameEntry.get(), emailEntry.get(), phoneEntry.get(), addressEntry.get(), genderEntry.get(), DOBEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def add_data():
    # Check if any of the required fields are empty
    if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or addressEntry.get() == '' or emailEntry.get() == '' or DOBEntry.get() == '' or genderEntry.get() == '':
        messagebox.showerror('Error', 'All Fields are required', parent=screen)
    else:
        try:
            # Insert data into the database
            query = 'insert into student values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            mycursor.execute(query, (idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), DOBEntry.get(), date, currentTime))
            con.commit()
            # Prompt the user to confirm if they want to clear the form
            result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clear the form?')
            if result:
                # Clear the form fields
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                DOBEntry.delete(0, END)
                genderEntry.delete(0, END)
                screen.destroy()
            else:
                pass
        except Exception as e:
            # Show an error message if there is an issue with the insertion
            messagebox.showerror('Error', f'ID cannot be repeated\n{str(e)}', parent=screen)
            return
        # Refresh the student table to show the newly added data
        show_student()

def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)  # Remove color formatting
    count += 1
    sliderLabel.after(300, slider)


def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=userEntry.get(), password=passwordEntry.get())
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Invalid Details', parent=connectWindow)
            return
        try:
            query = 'create database studentmanagementsystem'
            mycursor.execute(query)
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
            query = 'create table student(id int not null primary key, name varchar(30), mobile varchar(10), email varchar(30), address varchar(100), gender varchar(20), dob varchar(20), date varchar(50), time varchar(50))'
            mycursor.execute(query)
        except:
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database connection is successful', parent=connectWindow)
        connectWindow.destroy()
        AddStudentButton.config(state=NORMAL)
        SearchStudentButton.config(state=NORMAL)
        UpdateStudentButton.config(state=NORMAL)
        ShowStudentButton.config(state=NORMAL)
        DeleteStudentButton.config(state=NORMAL)
        ExportStudentButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0, 0)

    hostnameLabel = Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20)
    hostEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)
    userEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    userEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)
    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2, show='*')
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton = ttk.Button(connectWindow, text='Connect', command=connect)
    connectButton.grid(row=3, columnspan=2)

# Main Application
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.title('Student Management System')
root.geometry('1174x680+50+50')
root.resizable(False, False)

datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()

s = 'Welcome to Student Management System'
count = 0
text = ''
sliderLabel = Label(root, text=s, font=('arial', 20, 'italic bold'), relief=RIDGE, borderwidth=4, width=35, bg='cadet blue')
sliderLabel.place(x=300, y=0)
slider()

connectButton = ttk.Button(root, text='Connect Database', command=connect_database)
connectButton.place(x=980, y=0)

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file='student.png')
logoLabel = Label(leftFrame, image=logo_image)
logoLabel.grid(row=0, column=0)

AddStudentButton = ttk.Button(leftFrame, text='Add Student', width=25, state=DISABLED, command=lambda: toplevel_data('Add Student', 'Add', add_data))
AddStudentButton.grid(row=1, column=0, pady=20)

SearchStudentButton = ttk.Button(leftFrame, text='Search Student', width=25, state=DISABLED, command=lambda: toplevel_data('Search Student', 'Search', search_data))
SearchStudentButton.grid(row=2, column=0, pady=20)

UpdateStudentButton = ttk.Button(leftFrame, text='Update Student', width=25, state=DISABLED, command=lambda: toplevel_data('Update Student', 'Update', update_data))
UpdateStudentButton.grid(row=3, column=0, pady=20)

ShowStudentButton = ttk.Button(leftFrame, text='Show Student', width=25, state=DISABLED, command=show_student)
ShowStudentButton.grid(row=4, column=0, pady=20)

DeleteStudentButton = ttk.Button(leftFrame, text='Delete Student', width=25, state=DISABLED, command=delete_student)
DeleteStudentButton.grid(row=5, column=0, pady=20)

ExportStudentButton = ttk.Button(leftFrame, text='Export Data', width=25, state=DISABLED, command=export_data)
ExportStudentButton.grid(row=6, column=0, pady=20)

ExitButton = ttk.Button(leftFrame, text='Exit', width=25, command=iexit)
ExitButton.grid(row=7, column=0, pady=20)

rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=820, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('ID', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'DOB', 'Added Date', 'Added Time'), xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(fill=BOTH, expand=1)

studentTable.heading('ID', text='ID')
studentTable.heading('Name', text='Name')
studentTable.heading('Mobile', text='Mobile No')
studentTable.heading('Email', text='Email Address')
studentTable.heading('Address', text='Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('DOB', text='D.O.B')
studentTable.heading('Added Date', text='Added Date')
studentTable.heading('Added Time', text='Added Time')

studentTable.column('ID', width=100, anchor=CENTER)
studentTable.column('Name', width=200, anchor=CENTER)
studentTable.column('Mobile', width=200, anchor=CENTER)
studentTable.column('Email', width=300, anchor=CENTER)
studentTable.column('Address', width=200, anchor=CENTER)
studentTable.column('Gender', width=100, anchor=CENTER)
studentTable.column('DOB', width=150, anchor=CENTER)
studentTable.column('Added Date', width=150, anchor=CENTER)
studentTable.column('Added Time', width=150, anchor=CENTER)

style = ttk.Style()
style.configure('Treeview', rowheight=40, font=('arial', 12), background='cadet blue', fieldbackground='cadet blue')
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='red')

studentTable.config(show='headings')

root.mainloop()
