from tkinter import *
from tkinter import ttk, messagebox
import functions as fns
import mysql.connector as ms
import tkcalendar as tkcal
import datetime

# main window
root = Tk()
root.title('Appointment system')

# image object for icon
icon = PhotoImage(file="./logo1.png")
root.iconphoto(1, icon)

# dimensions of window
root.geometry('1000x700')
# root.maxsize(500,500)
root.minsize(550, 350)

# tab navigation
tabs = ttk.Notebook(root)


def handleTabChange(e):
    if tabs.index(CURRENT) != 4:
        tabs.hide(4)
        bookAppPatientId_Entry.delete(0, END)
        bookAppPatientName_Entry.delete(0, END)
        time_Var.set('9 a.m - 12 p.m')
        calendar.selection_clear()
        bookAppDoc_Var.set('')


def temp(e):
    tabs.select(4)


tabs.bind('<<NotebookTabChanged>>', handleTabChange)
root.bind('<Control-a>', temp)

# screens
home_Screen = Frame(root)
existingUser_Screen = Frame(root)
newUser_Screen = Frame(root)
generateToken_Screen = Frame(root)
bookAppointment_Screen = Frame(root)

# adding screens to the tab navigation structure
tabs.add(home_Screen, text='Home')
tabs.add(existingUser_Screen, text='Existing User')
tabs.add(newUser_Screen, text='New User')
tabs.add(generateToken_Screen, text='Generate token')
tabs.add(bookAppointment_Screen, text='Book Appointment')

# hiding temporary tab
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
            # exUserId is number
            exUserId = int(exUserId)
            patientName = fns.getPatientName(db, exUserId)
            if patientName != None:
                tabs.select(4)
                bookAppPatientId_Entry.insert(0, exUserId)
                bookAppPatientName_Entry.insert(0, patientName)

            else:
                messagebox.showinfo('User does not exist',
                                    'User does not exist. Please create user')
        except ValueError:
            # exUserId contains other characters
            messagebox.showerror(
                'Invalid entry', 'Please enter a valid patient ID')

    else:
        # user submitted with empty entry widget
        messagebox.showerror(
            'Invalid entry', 'Please enter a valid patient ID')
    exUserId_Entry.delete(0, END)


exUser_Label = Label(existingUser_Screen,
                     text='Exisiting User Appointment', font='comicsans 20 underline')
exUser_Label.place(relx=0.5, rely=0.35, anchor=CENTER)

exUserForm_Frame = Frame(existingUser_Screen, borderwidth=5, relief=GROOVE)
exUserForm_Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Tkinter variable to get user input from entry widget
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

# dummy list of doctors, to be taken from db
lst = [
    'Dr. Manoj Mathew (Pediatrics)',

    'Dr. Rahul Nair (Pediatrics)',

    'Dr. Sanjeev Menon (Pediatrics)',

    'Dr. Anakha Anil (Pediatrics)',

    'Dr. Arun Sanil (Pediatrics)',

    'Dr. Dheeraj (Pediatrics)',

    'Dr. Nizam Salim (Pediatrics)',

    'Dr. Mohan Kumar (Pediatrics)',

    'Dr. Rayhan Mohammed (Pediatrics)',

    'Dr. Anoop Menon (Pediatrics)',

    'Dr. Prithviraj Sukumaran (Pediatrics)',

    'Dr. Manju Warrier (Pediatrics)',

    'Dr. Anna Ben (Pediatrics)',

]


def isAppointmentBeforeToday(app_date):
    today = datetime.datetime.now()
    if app_date <= today:
        return True
    return False


def formatDate(rawDate):
    # rawDate = mm/dd/yy
    [mm, dd, yy] = rawDate.split('/')
    mm, dd, yyyy = int(mm), int(dd), int(yy)+2000
    dateObj = datetime.datetime(yyyy, mm, dd)
    dateString = dateObj.strftime('%d/%m/%y')
    return dateObj, dateString


def handleAppointmentSubmit():
    doc_name = bookAppDoc_Var.get()
    p_id = bookAppId_Var.get()
    p_name = bookAppName_Var.get()
    time = time_Var.get()
    rawDate = calendar.get_date()

    k = 0

    if doc_name and p_id and p_name and time and rawDate:

        (appDateObject, date) = formatDate(rawDate)

        if(isAppointmentBeforeToday(appDateObject)):
            messagebox.showerror(
                'Invalid date', f'Date should not be on or before {datetime.datetime.now().strftime("%d %B %Y")}')
            k = 1
        else:
            fns.createNewAppointment(db, sqlConn, doc_name, p_id, time, date)
            messagebox.showinfo('Appointment booked',
                                f'Appointment for {p_name} with id number {p_id} booked with {doc_name} on {date} during {time} ')
            tabs.select(0)
    else:
        messagebox.showerror(
            'Invalid entry', 'Please enter valid details')
    if k == 0:
        bookAppPatientId_Entry.delete(0, END)
        bookAppPatientName_Entry.delete(0, END)
        time_Var.set('9 a.m - 12 p.m')
        bookAppDoc_Var.set('')
    calendar.selection_clear()


bookApp_Label = Label(bookAppointment_Screen,
                      text="Book an Appointment", font="comicsans 20 underline")
bookApp_Label.pack()

bookApp_Frame = Frame(bookAppointment_Screen, borderwidth=5, relief=GROOVE)
bookApp_Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Tkinter variable to get user input from entry widget
bookAppDoc_Var = StringVar()
bookAppId_Var = StringVar()
bookAppName_Var = StringVar()


bookAppDoc_Label = Label(bookApp_Frame, text='Doctor', font='sans 14')
bookAppDoc_Dropbox = ttk.Combobox(
    bookApp_Frame, font='sans 14', state='readonly', textvariable=bookAppDoc_Var, width=25)

bookAppPatientId_Label = Label(
    bookApp_Frame, text='Patient ID', font='sans 14')
bookAppPatientId_Entry = Entry(
    bookApp_Frame, font='sans 14', width=27, textvariable=bookAppId_Var)

bookAppPatientName_Label = Label(
    bookApp_Frame, text='Patient Name', font='sans 14')
bookAppPatientName_Entry = Entry(
    bookApp_Frame, font='sans 14', width=27, textvariable=bookAppName_Var)

time_Var = StringVar(bookApp_Frame, '9 a.m - 12 p.m')

Label(bookApp_Frame, text="Time Slot", font='sans 14').grid(row=3, column=0)

Radiobutton(bookApp_Frame, text='9 a.m - 12 p.m', value='9 a.m - 12 p.m',
            variable=time_Var, font='sans 13').grid(row=4, column=0)
Radiobutton(bookApp_Frame, text='1 p.m. - 3 p.m.', value='1 p.m. - 3 p.m.',
            variable=time_Var, font='sans 13').grid(row=4, column=1)
Radiobutton(bookApp_Frame, text='4 p.m. - 6 p.m.', value='4 p.m. - 6 p.m.',
            variable=time_Var, font='sans 13').grid(row=5, column=0)
Radiobutton(bookApp_Frame, text='7 p.m. - 9 p.m.', value='7 p.m. - 9 p.m.',
            variable=time_Var, font='sans 13').grid(row=5, column=1)


bookAppDate_Label = Label(bookApp_Frame, text="Date", font='sans 14')
calendar = tkcal.Calendar(bookApp_Frame, selectmode="day")


bookAppDoc_Label.grid(row=0, column=0, pady=10)
bookAppDoc_Dropbox.grid(row=0, column=1, pady=10)

bookAppPatientId_Label.grid(row=1, column=0, pady=5)
bookAppPatientId_Entry.grid(row=1, column=1, padx=5, pady=5)

bookAppPatientName_Label.grid(row=2, column=0, pady=5)
bookAppPatientName_Entry.grid(row=2, column=1, padx=5, pady=5)

bookAppDate_Label.grid(row=6, column=0)
calendar.grid(row=6, column=1, pady=5)

bookAppSubmit_Frame = Frame(bookApp_Frame)
bookAppSubmit_Frame.grid(row=7, columnspan=2)

bookAppSubmit_Button = Button(bookAppSubmit_Frame, text='Book Appointment',
                              font='sans 13', command=handleAppointmentSubmit)
bookAppSubmit_Button.pack(pady=10)


# adds values of the list to dropbox
bookAppDoc_Dropbox['values'] = lst

# =================================== BOOK APPOINTMENT ======================================== #


# =================================== NEW USER ======================================== #


# =================================== NEW USER ======================================== #


root.mainloop()
