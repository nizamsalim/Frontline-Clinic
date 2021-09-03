from tkinter import *
from tkinter import ttk, messagebox
import functions as fns
import mysql.connector as ms

root = Tk()
root.title('Appointment system')
icon = PhotoImage(file="./logo1.png")
root.iconphoto(1, icon)
root.geometry('1000x700')
# root.maxsize(500,500)
root.minsize(550, 350)

tabs = ttk.Notebook(root)

# screens
home_Screen = Frame(root)
existingUser_Screen = Frame(root)
newUser_Screen = Frame(root)
generateToken_Screen = Frame(root)

bookAppointment_Screen = Frame(root)

tabs.add(home_Screen, text='Home')
tabs.add(existingUser_Screen, text='Existing User')
tabs.add(newUser_Screen, text='New User')
tabs.add(generateToken_Screen, text='Generate token')

# temporary tab
tabs.add(bookAppointment_Screen, text='Book Appointment')
tabs.hide(4)

tabs.pack(expand=1, fill=BOTH)

# db config
sqlConn = ms.connect(
    host="localhost",
    user='root',
    passwd='nizam123',
    database='frontline'
)
db = sqlConn.cursor()


# ============================== HOME PAGE ======================================== #

buttons_Frame = Frame(home_Screen)
buttons_Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

welcome_Label = Label(
    buttons_Frame, text='Frontline Clinic \n Appointments System', font='algerian 30')
welcome_Label.pack(pady=10)

Button(buttons_Frame, text='Appointment for existing user',
       font='helvetica 15', width=25, command=lambda: tabs.select(1)).pack(pady=10)
Button(buttons_Frame, text='Appointment for new user', font='helvetica 15',
       width=25, command=lambda: tabs.select(2)).pack(pady=10)
Button(buttons_Frame, text='Generate token', font='helvetica 15',
       width=25, command=lambda: tabs.select(3)).pack(pady=10)

# ============================== HOME PAGE ======================================== #

# ============================== EXISTING USER APPOINTMENT ======================================== #


def exUserSubmit():
    exUserId = exUserId_Var.get()
    if(exUserId):
        try:
            exUserId = int(exUserId)
            patientName = fns.getPatientName(db, exUserId)
            if patientName != None:
                tabs.select(4)
                win = Toplevel(root)
                win.geometry('500x500')
            else:
                messagebox.showinfo('User does not exist',
                                    'User does not exist. Please create user')
        except ValueError:
            messagebox.showerror(
                'Invalid entry', 'Please enter a valid patient ID')

    else:
        messagebox.showerror(
            'Invalid entry', 'Please enter a valid patient ID')
    exUserId_Entry.delete(0, END)


exUser_Label = Label(existingUser_Screen,
                     text='Exisiting User Appointment', font='comicsans 20 underline')
exUser_Label.place(relx=0.5, rely=0.35, anchor=CENTER)

exUserForm_Frame = Frame(existingUser_Screen, borderwidth=5, relief=GROOVE)
exUserForm_Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

exUserId_Var = StringVar()

exUserId_Label = Label(exUserForm_Frame, text='Patient ID', font='lucida 15')
exUserId_Entry = Entry(
    exUserForm_Frame, font='comicsans 14', textvariable=exUserId_Var)

exUserId_Label.grid(row=0, column=0, padx=10, pady=10)
exUserId_Entry.grid(row=0, column=1, padx=10, pady=10)

exUserSubmit_Frame = Frame(exUserForm_Frame)
exUserSubmit_Frame.grid(row=1, columnspan=2)

exUserSubmit_Button = Button(
    exUserSubmit_Frame, text='Submit', font='helvetica 13', command=exUserSubmit)
exUserSubmit_Button.pack()

# ============================== EXISTING USER APPOINTMENT ======================================== #


# =================================== BOOK APPOINTMENT ======================================== #



# =================================== BOOK APPOINTMENT ======================================== #


root.mainloop()
