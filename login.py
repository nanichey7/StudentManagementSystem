from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

def login():
    if usernameEntry.get()=='' or PasswordEntry.get()=='':
        messagebox.showerror('Error','Fields cannot be empty')
    elif usernameEntry.get()=='nanichey7' or PasswordEntry.get()=='24580':
        messagebox.showinfo('Success','Welcome')
        window.destroy()
        import sms

    else:
        messagebox.showerror('Error','Please enter correct credentials')
window = Tk()
window.geometry('1280x700+0+0')
window.title('Login')
window.resizable(False, False)

backgroundImage = ImageTk.PhotoImage(file='bg.jpg')
bgLabel = Label(window,image=backgroundImage)
bgLabel.place(x=0,y=0)

loginFrame=Frame(window,bg='white')
loginFrame.place(x=400,y=150)

logoImage=PhotoImage(file='logo.png')
logoLabel=Label(loginFrame,image=logoImage)
logoLabel.grid(row=0,column=0,columnspan=2,pady=10)

usernameImage=PhotoImage(file='user.png')
usernameLabel=Label(loginFrame,image=usernameImage,text='Username',compound=LEFT,font=('times new roman',20,'bold'),bg='white')
usernameLabel.grid(row=1,column=0,pady=10,padx=20)

usernameEntry=Entry(loginFrame,font=('calibri',18),bd=2)
usernameEntry.grid(row=1,column=1,padx=20)

PasswordImage=PhotoImage(file='password.png')
PasswordLabel=Label(loginFrame,image=PasswordImage,text='Password',compound=LEFT,font=('times new roman',20,'bold'),bg='white')
PasswordLabel.grid(row=2,column=0,pady=10,padx=20)

PasswordEntry=Entry(loginFrame,font=('calibri',18),bd=2)
PasswordEntry.grid(row=2,column=1,padx=20)

loginButton=Button(loginFrame,text='Login',font=('times new roman',14,'bold'),width=15,fg='white',bg='cornflowerblue',activebackground='cornflowerblue',activeforeground='white',cursor='hand2',command=login)
loginButton.grid(row=3,column=1)
window.mainloop()