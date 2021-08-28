from tkinter import *
from tkinter import ttk
root = Tk()
root.title('Appointment system')
icon = PhotoImage(file="./logo1.png")
root.iconphoto(False, icon)
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

tabs.pack(expand=True,fill=BOTH)

# ============================== HOME PAGE ======================================== #

buttons_Frame = Frame(home_Screen)
buttons_Frame.place(relx=0.5,rely=0.5,anchor=CENTER)

welcome_Label = Label(buttons_Frame,text='Frontline Clinic \n Appointments System',font='algerian 30')
welcome_Label.pack(pady=10)

Button(buttons_Frame,text='Appointment for existing user',font='helvetica 15',width=25).pack(pady=10)
Button(buttons_Frame,text='Appointment for new user',font='helvetica 15',width=25).pack(pady=10)
Button(buttons_Frame,text='Generate token',font='helvetica 15',width=25).pack(pady=10)

# ============================== HOME PAGE ======================================== #

root.mainloop()
