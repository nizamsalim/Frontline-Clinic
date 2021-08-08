from tkinter import *
from tkinter import ttk
from tkinter import messagebox

root = Tk()
root.title('Appointment system')
icon = PhotoImage(file="./logo1.png")
root.iconphoto(False, icon)
root.geometry('1000x700')
# root.maxsize(500,500)
root.minsize(550, 350)


tabs = ttk.Notebook(root, padding=0)


def changePage(screen):
    # print(screen)
    screenList = ['existingUser', 'newUser', 'token']
    for i in range(len(screenList)):
        if screenList[i] == screen:
            tabs.select(i+1)


def handleSubmit():
    userId = userIdVar.get()
    if(userId):
        print(userId)
    else:
        messagebox.showerror('Invalid', 'Please enter a valid user ID')


# screens
###########################
home_Screen = Frame(tabs)
existingUser_Screen = Frame(tabs)
newUser_Screen = Frame(tabs)
generateToken_Screen = Frame(tabs)

scrollbar = Scrollbar(tabs)
scrollbar.pack(side=RIGHT, fill=Y)

###########################

# adding screens to tabs
###########################
tabs.add(home_Screen, text="Home")
tabs.add(existingUser_Screen, text="Existing User")
tabs.add(newUser_Screen, text="New User")
tabs.add(generateToken_Screen, text="Generate token")
###########################

# packing tabs
tabs.pack(expand=1, fill="both", padx=0, pady=0)

# home screen
###########################
buttons_Frame = Frame(home_Screen)
buttons_Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

welcome_Label = Label(
    buttons_Frame, text='Frontline Clinic \n Appointments system', font='comicsans 35 bold')
welcome_Label.pack(pady=20)

Button(buttons_Frame, text='Appointment for existing user', font=20, width=25,
       command=lambda: changePage('existingUser')).pack(pady=10)
Button(buttons_Frame, text='Appointment for new user', width=25,
       font=20, command=lambda: changePage('newUser')).pack(pady=8)
Button(buttons_Frame, text='Generate token',
       command=lambda: changePage('token'), width=25, font=20).pack(pady=8)
###########################

# existing user screen
###########################
container_Frame = Frame(existingUser_Screen)
container_Frame.place(relx=0.5, rely=0.35, anchor=CENTER)

heading_Label = Label(
    container_Frame, text='Existing user appointment', font='comicsans 20 underline')
heading_Label.pack()

form_Frame = Frame(existingUser_Screen, borderwidth=3,
                   relief=SUNKEN, )
form_Frame.place(relx=0.5, rely=0.5, anchor=CENTER, )

userIdVar = StringVar()

userId_Entry = Entry(form_Frame, font="comicsans 15", textvariable=userIdVar)
userId_Label = Label(form_Frame, text='User ID', font="comicsans 15")

userId_Label.grid(row=0, column=0, pady=10, padx=10)
userId_Entry.grid(row=0, column=1, pady=10, padx=10)

submit_Button = Button(form_Frame, text='Submit',
                       command=handleSubmit, font="comicsans 14")
submit_Button.grid(row=1, column=0, pady=5)

###########################


root.mainloop()
