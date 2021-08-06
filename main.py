from tkinter import *
from tkinter import ttk

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


# screens
###########################
home_Screen = Frame(tabs)
existingUser_Screen = Frame(tabs)
newUser_Screen = Frame(tabs)
generateToken_Screen = Frame(tabs)
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


root.mainloop()
