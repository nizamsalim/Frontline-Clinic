from tkinter import *
from tkinter import ttk, messagebox
import functions as fns
import tkcalendar as tkcal
import datetime


# main window
root = Tk()

# title of the windpw
root.title('Frontline Clinic')

# image object for icon
icon = PhotoImage(file="./logo1.png")
root.iconphoto(1, icon)

# dimensions of window
root.geometry('1000x700')


# db config
isConnected = fns.initDatabase()
if isConnected == False:
    messagebox.showerror("Error", "Database connection error")
    root.destroy()
    exit()

# tab navigation
tabs = ttk.Notebook(root)

# screens
home_Screen = Frame(root)
existingUser_Screen = Frame(root)
newUser_Screen = Frame(root)
generateToken_Screen = Frame(root)
bookAppointment_Screen = Frame(root)
manageDoctors_Screen = Frame(root)
managePatients_Screen = Frame(root)
viewAppointments_Screen = Frame(root)

# adding screens to the tab navigation structure
tabs.add(home_Screen, text='Home')
tabs.add(existingUser_Screen, text='Existing User')
tabs.add(newUser_Screen, text='New User')
tabs.add(generateToken_Screen, text='Generate token')
tabs.add(bookAppointment_Screen, text='Book Appointment')
tabs.add(manageDoctors_Screen, text='Manage doctors')
tabs.add(managePatients_Screen, text='Manage patients')
tabs.add(viewAppointments_Screen, text='View appointments')

# hiding temporary tab
tabs.hide(4)

# inserting the tab navigation bar in the UI
tabs.pack(expand=1, fill=BOTH)


# ====================================== HOME PAGE ================================================ #

# container for the nav buttons
buttons_Frame = Frame(home_Screen)
buttons_Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

welcome_Label = Label(
    buttons_Frame, text='Frontline Clinic', font='algerian 30')
welcome_Label.pack(pady=10)

# nav buttons
Button(buttons_Frame, text='Appointment for existing user',
       font='helvetica 15', width=25, command=lambda: tabs.select(1)).pack(pady=10)
Button(buttons_Frame, text='Appointment for new user', font='helvetica 15',
       width=25, command=lambda: tabs.select(2)).pack(pady=10)
Button(buttons_Frame, text='Generate token', font='helvetica 15',
       width=25, command=lambda: tabs.select(3)).pack(pady=10)
Button(buttons_Frame, text='Manage doctors', font='helvetica 15',
       width=25, command=lambda: tabs.select(5)).pack(pady=10)
Button(buttons_Frame, text='Manage patients', font='helvetica 15',
       width=25, command=lambda: tabs.select(6)).pack(pady=10)
Button(buttons_Frame, text='View appointments', font='helvetica 15',
       width=25, command=lambda: tabs.select(7)).pack(pady=10)


# ====================================== HOME PAGE ================================================ #


# ====================================== PAST APPOINTMENTS ================================================ #

"""function to fetch past appointments and display it in new window"""


def showPastAppointmentsWindow(p_id, nm):
    pastApp_Window = Toplevel(root)
    pastApp_Window.focus_force()
    pastApp_Window.title(f'Appointment history for {nm}')
    # fetches past appointments from the db
    appointments = fns.getPastAppointments(p_id)
    appointments.insert(0, ('Reference id', 'Doctor',
                        'Booking date', 'Appointment date', 'Status'))
    # displays data in table form
    for i in range(len(appointments)):
        for j in range(len(appointments[i])):
            Label(pastApp_Window, text=appointments[i][j], width=30, font='comicsans 10', relief=SUNKEN).grid(
                row=i, column=j)
    # closes the window if it loses focus
    pastApp_Window.bind('<FocusOut>', lambda e:  pastApp_Window.destroy())

# ====================================== PAST APPOINTMENTS ================================================ #

# ============================== EXISTING USER APPOINTMENT ======================================== #


"""function to handle submit button click for creating appointment for existing user"""


def exUserSubmit():
    exUserId = exUserId_Var.get()
    if(exUserId):
        try:
            # exUserId is number
            exUserId = int(exUserId)
            # checks whether id is present
            patientName = fns.getPatientName(exUserId)
            if patientName != None:
                # function to show past appointments
                showPastAppointmentsWindow(exUserId, patientName)
                # redirect to appointment-booking screen
                tabs.select(4)
                # populates id and name in the appointment-booking screen
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


# screen label
exUser_Label = Label(existingUser_Screen,
                     text='Exisiting User Appointment', font='comicsans 20 underline')
exUser_Label.place(relx=0.5, rely=0.35, anchor=CENTER)

exUserForm_Frame = Frame(existingUser_Screen, borderwidth=5, relief=GROOVE)
exUserForm_Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Tkinter variable to get user input from entry widget
exUserId_Var = StringVar()

# declaring label and text field for accepting patient id
exUserId_Label = Label(exUserForm_Frame, text='Patient ID', font='lucida 15')
exUserId_Entry = Entry(
    exUserForm_Frame, font='comicsans 14', textvariable=exUserId_Var)

# placing it in grid form
exUserId_Label.grid(row=0, column=0, padx=10, pady=10)
exUserId_Entry.grid(row=0, column=1, padx=10, pady=10)

# submit button
exUserSubmit_Frame = Frame(exUserForm_Frame)
exUserSubmit_Frame.grid(row=1, columnspan=2)

exUserSubmit_Button = Button(
    exUserSubmit_Frame, text='Submit', font='helvetica 13', command=exUserSubmit)
exUserSubmit_Button.pack()

# ============================== EXISTING USER APPOINTMENT ======================================== #
# =================================== BOOK APPOINTMENT ======================================== #

"""function to check whether entered date is on or before today"""


def isAppointmentBeforeToday(app_date):
    today = datetime.datetime.now()
    return True if app_date <= today else False


"""function to convert date object to readable format for display"""


def formatDate(rawDate):
    # rawDate = mm/dd/yy
    [mm, dd, yy] = rawDate.split('/')
    mm, dd, yyyy = int(mm), int(dd), int(yy)+2000
    dateObj = datetime.datetime(yyyy, mm, dd)
    dateString = dateObj.strftime('%d/%m/%y')
    return dateObj, dateString


"""function to handle book appointment submit"""


def handleAppointmentSubmit():
    # fetching data from the text fields
    doc_name = bookAppDoc_Var.get()
    p_id = bookAppId_Var.get()
    p_name = bookAppName_Var.get()
    time = time_Var.get()
    rawDate = calendar.get_date()

    k = 0

    if doc_name and p_id and p_name and time and rawDate:  # validation

        (appDateObject, date) = formatDate(rawDate)

        if(isAppointmentBeforeToday(appDateObject)):
            messagebox.showerror(
                'Invalid date', f'Date should not be on or before {datetime.datetime.now().strftime("%d %B %Y")}')
            k = 1
        else:
            # creates new appointment record
            app_id = fns.createNewAppointment(
                doc_name, p_id, time, date)
            messagebox.showinfo('Appointment booked',
                                f'Appointment for {p_name} booked with {doc_name} on {date} during {time}. Please note reference number {app_id}')
            # redirect to home page
            tabs.select(0)
    else:
        k = 1
        messagebox.showerror(
            'Invalid entry', 'Please enter valid details')
    """restoring screen states to initial values"""
    if k == 0:
        bookAppPatientId_Entry.delete(0, END)
        bookAppPatientName_Entry.delete(0, END)
        time_Var.set('9 a.m - 12 p.m')
        bookAppDoc_Var.set('')
    calendar.selection_clear()


# screen label
bookApp_Label = Label(bookAppointment_Screen,
                      text="Book an Appointment", font="comicsans 20 underline")
bookApp_Label.pack()

bookApp_Frame = Frame(bookAppointment_Screen, borderwidth=5, relief=GROOVE)
bookApp_Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Tkinter variable to get user input from entry widget
bookAppDoc_Var = StringVar()
bookAppId_Var = StringVar()
bookAppName_Var = StringVar()

"""input fields for doctor name, patient id, patient name"""
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

"""radio buttons to accept appointment time"""
Radiobutton(bookApp_Frame, text='9 a.m - 12 p.m', value='9 a.m - 12 p.m',
            variable=time_Var, font='sans 13').grid(row=4, column=0)
Radiobutton(bookApp_Frame, text='1 p.m. - 3 p.m.', value='1 p.m. - 3 p.m.',
            variable=time_Var, font='sans 13').grid(row=4, column=1)
Radiobutton(bookApp_Frame, text='4 p.m. - 6 p.m.', value='4 p.m. - 6 p.m.',
            variable=time_Var, font='sans 13').grid(row=5, column=0)
Radiobutton(bookApp_Frame, text='7 p.m. - 9 p.m.', value='7 p.m. - 9 p.m.',
            variable=time_Var, font='sans 13').grid(row=5, column=1)

"""calendar to input date"""
bookAppDate_Label = Label(bookApp_Frame, text="Date", font='sans 14')
calendar = tkcal.Calendar(bookApp_Frame, selectmode="day")

"""placing all UI elements in grid geometry"""
bookAppDoc_Label.grid(row=0, column=0, pady=10)
bookAppDoc_Dropbox.grid(row=0, column=1, pady=10)

bookAppPatientId_Label.grid(row=1, column=0, pady=5)
bookAppPatientId_Entry.grid(row=1, column=1, padx=5, pady=5)

bookAppPatientName_Label.grid(row=2, column=0, pady=5)
bookAppPatientName_Entry.grid(row=2, column=1, padx=5, pady=5)

bookAppDate_Label.grid(row=6, column=0)
calendar.grid(row=6, column=1, pady=5)

# submit button
bookAppSubmit_Frame = Frame(bookApp_Frame)
bookAppSubmit_Frame.grid(row=7, columnspan=2)

bookAppSubmit_Button = Button(bookAppSubmit_Frame, text='Book Appointment',
                              font='sans 13', command=handleAppointmentSubmit)
bookAppSubmit_Button.pack(pady=10)

"""function to fetch list of all doctors and insert it into the dropdown each time the screen is loaded"""


def populateDoctors():
    docDropdownList = fns.getDoctorsForDropDown()
    bookAppDoc_Dropbox['values'] = docDropdownList

# =================================== BOOK APPOINTMENT ======================================== #


# =================================== NEW USER ======================================== #

"""function to handle creation of new user"""


def handleNewUserSubmit():
    # fetching values from input fields
    name = nameVar.get()
    place = placeVar.get()
    age = ageVar.get()
    phone = phoneVar.get()

    if name and place and age and phone:  # validation
        # creates new user
        pid = fns.createNewUser(name, age, phone, place)
        messagebox.showinfo(
            'User created', f'User created successfully with id {pid}')

        # populates id and name in the appointment-booking screen
        bookAppPatientId_Entry.insert(0, str(pid))
        bookAppPatientName_Entry.insert(0, name)
        # redirect to appointment-booking screen
        tabs.select(4)

    else:
        messagebox.showerror(
            'Invalid entry', 'Please enter valid details')
    # clear form
    newUserName_Entry.delete(0, END)
    newUserPlace_Entry.delete(0, END)
    newUserAge_Entry.delete(0, END)
    newUserPhone_Entry.delete(0, END)


# screen label
newUser_Label = Label(newUser_Screen, text="New User",
                      font="comicsans 20 underline")
newUser_Label.place(relx=0.5, rely=0.25, anchor=CENTER)

newUserForm_Frame = Frame(newUser_Screen, borderwidth=5, relief=GROOVE)
newUserForm_Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# labels for input data
newUserName_Label = Label(newUserForm_Frame, text="Name", font="sans 14")
newUserPlace_Label = Label(newUserForm_Frame, text="Place", font="sans 14")
newUserAge_Label = Label(newUserForm_Frame, text="Age", font="sans 14")
newUserPhone_Label = Label(newUserForm_Frame, text="Phone", font="sans 14")

# Tkinter variables to hold user input
nameVar = StringVar()
placeVar = StringVar()
ageVar = StringVar()
phoneVar = StringVar()

# text fields
newUserName_Entry = Entry(
    newUserForm_Frame, font='sans 14', borderwidth=2, relief=SUNKEN, textvariable=nameVar)
newUserPlace_Entry = Entry(
    newUserForm_Frame, font='sans 14', borderwidth=2, relief=SUNKEN, textvariable=placeVar)
newUserAge_Entry = Entry(
    newUserForm_Frame, font='sans 14', borderwidth=2, relief=SUNKEN, textvariable=ageVar)
newUserPhone_Entry = Entry(
    newUserForm_Frame, font='sans 14', borderwidth=2, relief=SUNKEN, textvariable=phoneVar)

"""placing all labels and text-fields in grid geometry"""
newUserName_Label.grid(row=0, column=0, padx=10, pady=10)
newUserPlace_Label.grid(row=1, column=0, padx=10, pady=10)
newUserAge_Label.grid(row=2, column=0, padx=10, pady=10)
newUserPhone_Label.grid(row=3, column=0, padx=10, pady=10)

newUserName_Entry.grid(row=0, column=1, padx=10, pady=10)
newUserPlace_Entry.grid(row=1, column=1, padx=10, pady=10)
newUserAge_Entry.grid(row=2, column=1, padx=10, pady=10)
newUserPhone_Entry.grid(row=3, column=1, padx=10, pady=10)

# submit button
newUserSubmit_Frame = Frame(newUserForm_Frame)
newUserSubmit_Frame.grid(row=4, columnspan=2)

newUserSubmit_Button = Button(
    newUserSubmit_Frame, text="Submit", font="sans 14", command=handleNewUserSubmit)
newUserSubmit_Button.pack(pady=5)

# ====================================== NEW USER =========================================== #
# =================================== GENERATE TOKEN ======================================== #
"""fetches initial token number when the app is started"""
tokenCount = fns.getInitialTokenNumber()

"""generates new token number by increasing the previous token count by 1"""


def getTokenNumber():
    global tokenCount
    [dd, mm] = datetime.datetime.now().strftime('%d/%m').split('/')
    token = f"{dd}{mm}-{tokenCount}"
    tokenCount += 1
    messagebox.showinfo('Token number', f'Token number is {token}')
    return token


"""function to handle generate token submit"""


def genTokenSubmit():
    appId = genTokenRefNum_Var.get()
    if(appId):
        try:
            appId = int(appId)
            # checks whether appointment reference is existing
            p_id = fns.getPatientIdByAppId(appId)
            if p_id == None:
                messagebox.showinfo('Not found',
                                    'Appointment reference number does not exist.')
            else:
                # checks whether appointment completed/pending
                isAppointmentPending = fns.isAppointmentPending(appId)
                if isAppointmentPending == False:
                    messagebox.showinfo('Not found',
                                        'Appointment is already completed')
                else:
                    # saves token number in the db
                    tkn = getTokenNumber()
                    fns.saveToken(tkn)
                    # updates number of visits and status
                    fns.updateNumberOfVisits(p_id)
                    fns.updateAppointmentStatus(p_id, 'completed')
                    # clears form and redirects to home
                    genTokenRefNum_Entry.delete(0, END)
                    tabs.select(0)
        except ValueError:
            messagebox.showerror(
                'Invalid entry', 'Please enter a valid reference number')
    else:
        messagebox.showerror(
            'Invalid entry', 'Please enter a valid reference number')


# screen label
genToken_Label = Label(generateToken_Screen,
                       text='Generate Token', font='comicsans 20 underline')
genToken_Label.place(relx=0.5, rely=0.35, anchor=CENTER)

genTokenForm_Frame = Frame(generateToken_Screen, borderwidth=5, relief=GROOVE)
genTokenForm_Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Tkinter variable to get user input from entry widget
genTokenRefNum_Var = StringVar()

# reference number label and text-field
genTokenRefNum_Label = Label(
    genTokenForm_Frame, text='Reference number', font='lucida 15')
genTokenRefNum_Entry = Entry(
    genTokenForm_Frame, font='comicsans 14', textvariable=genTokenRefNum_Var)

# placing it in the UI
genTokenRefNum_Label.grid(row=0, column=0, padx=10, pady=10)
genTokenRefNum_Entry.grid(row=0, column=1, padx=10, pady=10)

# submit button
genTokenSubmit_Frame = Frame(genTokenForm_Frame)
genTokenSubmit_Frame.grid(row=1, columnspan=2)

genTokenSubmit_Button = Button(
    genTokenSubmit_Frame, text='Submit', font='helvetica 13', command=genTokenSubmit)
genTokenSubmit_Button.pack(pady=10)

# =================================== GENERATE TOKEN ======================================== #
# =================================== MANAGE DOCTORS ======================================== #

"""function to handle adding and updation of doctors"""


def handleDocSubmit(nm, dpt, sal, exp, win, origin, did="", docListId=""):
    if nm and dpt and sal and exp:
        if origin == 'add':
            newDoc = fns.addDoctor(nm, dpt, sal, exp)
            docList.insert("", END, values=newDoc)
            win.destroy()
        else:
            fns.updateDoctor(did, nm, dpt, sal, exp)
            docList.delete(docListId[0])
            docList.insert("", docListId[1], values=(did, nm, dpt, sal, exp))
            win.destroy()


"""function to display popup window for adding and updating"""


def showDoctorInputWindow(origin, name="", dept="", sal="", exp="", did="", docListId=""):
    # tkinter variables
    docNameVar = StringVar(value=name)
    deptVar = StringVar(value=dept)
    salVar = StringVar(value=sal)
    expVar = StringVar(value=exp)

    # popup window
    addDoc_Window = Toplevel(root)
    addDoc_Window.title(f"{origin.capitalize()} Doctor")
    addDoc_Window.geometry("700x400")
    addDoc_Window.focus_force()
    addDoc_Label = Label(addDoc_Window, text=f"{origin.capitalize()} Doctor",
                         font="comicsans 20 underline")
    addDoc_Label.place(relx=0.5, rely=0.1, anchor=CENTER)

    addDocForm_Frame = Frame(addDoc_Window, borderwidth=5, relief=GROOVE)
    addDocForm_Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    """labels for text-fields"""
    addDocName_Label = Label(addDocForm_Frame, text="Name", font="sans 14")
    addDocDept_Label = Label(
        addDocForm_Frame, text="Department", font="sans 14")
    addDocSal_Label = Label(addDocForm_Frame, text="Salary", font="sans 14")
    addDocExp_Label = Label(
        addDocForm_Frame, text="Experience", font="sans 14")

    """text-fields"""
    addDocName_Entry = Entry(
        addDocForm_Frame, font='sans 14', borderwidth=2, relief=SUNKEN, textvariable=docNameVar)
    addDocName_Entry.focus_force()
    addDocDept_Entry = Entry(
        addDocForm_Frame, font='sans 14', borderwidth=2, relief=SUNKEN, textvariable=deptVar)
    addDocSal_Entry = Entry(
        addDocForm_Frame, font='sans 14', borderwidth=2, relief=SUNKEN, textvariable=salVar)
    addDocExp_Entry = Entry(
        addDocForm_Frame, font='sans 14', borderwidth=2, relief=SUNKEN, textvariable=expVar)

    """placing all elements in grid"""
    addDocName_Label.grid(row=0, column=0, padx=10, pady=10)
    addDocDept_Label.grid(row=1, column=0, padx=10, pady=10)
    addDocSal_Label.grid(row=2, column=0, padx=10, pady=10)
    addDocExp_Label.grid(row=3, column=0, padx=10, pady=10)

    addDocName_Entry.grid(row=0, column=1, padx=10, pady=10)
    addDocDept_Entry.grid(row=1, column=1, padx=10, pady=10)
    addDocSal_Entry.grid(row=2, column=1, padx=10, pady=10)
    addDocExp_Entry.grid(row=3, column=1, padx=10, pady=10)

    """submit"""
    addDocSubmit_Frame = Frame(addDocForm_Frame)
    addDocSubmit_Frame.grid(row=4, columnspan=2)

    addDocSubmit_Button = Button(
        addDocSubmit_Frame, text="Submit", font="sans 14", command=lambda: handleDocSubmit(docNameVar.get(), deptVar.get(), salVar.get(), expVar.get(), addDoc_Window, origin, did, docListId))
    addDocSubmit_Button.pack(pady=5)


"""function to update UI after deleting doctor"""


def removeDoctor():
    if docList.selection():
        docListId = docList.selection()[0]
        docListIds = docList.get_children()
        ind = docListIds.index(docListId)
        tempDoctors = fns.getAllDoctors()
        res = messagebox.askyesno(
            'Delete doctor', f'Are you sure you want to delete {tempDoctors[ind][1]}')
        if res:
            fns.deleteDoctor(tempDoctors[ind][0])
            docList.delete(docListId)


"""function to update UI after updating doctor"""


def updateDoc():
    if docList.selection():
        docListId = docList.selection()[0]
        docListIds = docList.get_children()
        ind = docListIds.index(docListId)
        tempDoctors = fns.getAllDoctors()
        (did, name, dpt, sal, exp) = tempDoctors[ind]
        showDoctorInputWindow('update', name, dpt, sal,
                              exp, did=did, docListId=(docListId, ind))


actionButtons_Frame = Frame(manageDoctors_Screen)

# action buttons
Button(actionButtons_Frame, text="Add doctor", font='comicsans 11', width=20,
       command=lambda: showDoctorInputWindow('add')).pack(pady=10)
Button(actionButtons_Frame, text="Update doctor", font='comicsans 11', width=20,
       command=updateDoc).pack(pady=10)
Button(actionButtons_Frame, text="Delete doctor", font='comicsans 11', width=20,
       command=removeDoctor).pack(pady=10)

actionButtons_Frame.pack(side='left', fill=Y)

docColumns = ('sl', 'docName', 'deptName', 'sal', 'exp')

"""table to display doctors"""
docList = ttk.Treeview(manageDoctors_Screen,
                       columns=docColumns, show="headings")

docListStyle = ttk.Style()

docListStyle.configure("Treeview", font=('comicsans', 12), rowheight=35)
docListStyle.configure('Treeview.Heading', font=('comicsans', 11))

docColumnsDict = {
    'sl': 'Doctor ID',
    'docName': 'Doctor name',
    'deptName': 'Department',
    'sal': 'Salary',
    'exp': 'Experience'
}

# configuring headers
for column in docColumnsDict:
    docList.heading(column, text=docColumnsDict[column])

for i in range(1, 6):
    docList.column(f"#{i}", anchor=CENTER)


doctors = fns.getAllDoctors()
# inserting doctors to table
for doctor in doctors:
    docList.insert("", END, values=doctor)

docList.pack(expand=True, fill=BOTH)
# =================================== MANAGE DOCTORS ======================================== #
# =================================== MANAGE PATIENTS ======================================== #

patientButtons_Frame = Frame(managePatients_Screen)

"""function to update UI after deleting patient"""


def removePatient():
    if patientList.selection():
        patientListId = patientList.selection()[0]
        patientListIds = patientList.get_children()
        ind = patientListIds.index(patientListId)
        tempPatients = fns.getAllPatients()
        res = messagebox.askyesno(
            'Delete doctor', f'Are you sure you want to delete {tempPatients[ind][1]}')
        if res:
            fns.deletePatient(tempPatients[ind][0])
            patientList.delete(patientListId)


"""function to handle patient update"""


def handlePatientUpdateSubmit(pid, nm, age, phone, win, patListId):
    if nm and age and phone:
        updatedPatient = fns.updatePatient(pid, nm, age, phone)
        patientList.delete(patListId[0])
        patientList.insert("", patListId[1], values=updatedPatient)
        win.destroy()


"""function to update UI after updating patient"""


def updatePatient():
    if patientList.selection():
        patientListId = patientList.selection()[0]
        patientListIds = patientList.get_children()
        ind = patientListIds.index(patientListId)
        tempPatients = fns.getAllPatients()
        (pid, name, age, phone, visits) = tempPatients[ind]
        showPatientUpdateWindow(pid, name, age, phone, (patientListId, ind))


"""function to show popup window to update patient"""


def showPatientUpdateWindow(pid, name, age, phone, patListId):
    # values from text-fields
    patNameVar = StringVar(value=name)
    ageVar = StringVar(value=age)
    phoneVar = StringVar(value=phone)

    # popup window
    addPatient_Window = Toplevel(root)
    addPatient_Window.title(f"Update patient")
    addPatient_Window.geometry("700x400")
    addPatient_Window.focus_force()
    addPatient_Label = Label(addPatient_Window, text=f"Update patient",
                             font="comicsans 20 underline")
    addPatient_Label.place(relx=0.5, rely=0.1, anchor=CENTER)

    addPatientForm_Frame = Frame(
        addPatient_Window, borderwidth=5, relief=GROOVE)
    addPatientForm_Frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # labels
    addPatientName_Label = Label(
        addPatientForm_Frame, text="Name", font="sans 14")
    addPatientDept_Label = Label(
        addPatientForm_Frame, text="Age", font="sans 14")
    addPatientSal_Label = Label(
        addPatientForm_Frame, text="Phone", font="sans 14")

    # text-fields
    addPatientName_Entry = Entry(
        addPatientForm_Frame, font='sans 14', borderwidth=2, relief=SUNKEN, textvariable=patNameVar)
    addPatientName_Entry.focus_force()
    addPatientDept_Entry = Entry(
        addPatientForm_Frame, font='sans 14', borderwidth=2, relief=SUNKEN, textvariable=ageVar)
    addPatientSal_Entry = Entry(
        addPatientForm_Frame, font='sans 14', borderwidth=2, relief=SUNKEN, textvariable=phoneVar)

    """placing all elements in grid"""
    addPatientName_Label.grid(row=0, column=0, padx=10, pady=10)
    addPatientDept_Label.grid(row=1, column=0, padx=10, pady=10)
    addPatientSal_Label.grid(row=2, column=0, padx=10, pady=10)

    addPatientName_Entry.grid(row=0, column=1, padx=10, pady=10)
    addPatientDept_Entry.grid(row=1, column=1, padx=10, pady=10)
    addPatientSal_Entry.grid(row=2, column=1, padx=10, pady=10)

    # submit button
    addPatientSubmit_Frame = Frame(addPatientForm_Frame)
    addPatientSubmit_Frame.grid(row=4, columnspan=2)

    addPatientSubmit_Button = Button(
        addPatientSubmit_Frame, text="Submit", font="sans 14", command=lambda: handlePatientUpdateSubmit(pid, patNameVar.get(), ageVar.get(), phoneVar.get(),  addPatient_Window, patListId))
    addPatientSubmit_Button.pack(pady=5)


# action buttons
Button(patientButtons_Frame, text="Update patient", font='comicsans 11', width=20,
       command=updatePatient).pack(pady=10)
Button(patientButtons_Frame, text="Delete patient", font='comicsans 11', width=20,
       command=removePatient).pack(pady=10)

patientButtons_Frame.pack(side='left', fill=Y)

patientColumns = ('id', 'name', 'age', 'phone', 'visits')

# table to display patients
patientList = ttk.Treeview(managePatients_Screen,
                           columns=patientColumns, show='headings')

patientColumnsDict = {
    'id': 'Patient id',
    'name': 'Name',
    'age': "Age",
    'phone': 'Phone',
    'visits': 'Visits'
}

# configuring headers
for column in patientColumnsDict:
    patientList.heading(column, text=patientColumnsDict[column])
for i in range(1, 6):
    patientList.column(f"#{i}", anchor=CENTER)

"""function to fetch list of all patients and insert it into the table each time the screen is loaded"""


def populatePatients():
    for item in patientList.get_children():
        patientList.delete(item)
    patients = fns.getAllPatients()
    for patient in patients:
        patientList.insert("", END, values=patient)


patientList.pack(expand=True, fill=BOTH)


# =================================== MANAGE PATIENTS ======================================== #
# =================================== VIEW APPOINTMENTS ======================================== #

appointmentColumns = ('refno', 'docname', 'patname',
                      'appdate', 'time', 'status')

# table to display appointments
appointmentlist = ttk.Treeview(
    viewAppointments_Screen, columns=appointmentColumns, show="headings")


appointmentListDict = {
    'refno': 'Reference number',
    'docname': 'Doctor name',
    'patname': 'Patient name',
    'appdate': 'Appointment date',
    'time': 'Time',
    'status': 'Status'
}

# configuring headers
for column in appointmentListDict:
    appointmentlist.heading(column, text=appointmentListDict[column])
for i in range(1, 7):
    appointmentlist.column(f"#{i}", anchor=CENTER)

"""function to fetch list of all appointments and insert it into the table each time the screen is loaded"""


def populateAppointments():
    for item in appointmentlist.get_children():
        appointmentlist.delete(item)
    appointments = fns.getAllAppointments()
    for appointment in appointments:
        appointmentlist.insert("", END, values=appointment)


appointmentlist.pack(expand=True, fill=BOTH)


# =================================== VIEW APPOINTMENTS ======================================== #
"""function that is called each time a tab is changed"""


def handleTabChange(e):
    # temporarily hidden tab
    if tabs.index(CURRENT) != 4:
        tabs.hide(4)
        bookAppPatientId_Entry.delete(0, END)
        bookAppPatientName_Entry.delete(0, END)
        bookAppDoc_Var.set('')
        time_Var.set('9 a.m - 12 p.m')
        calendar.selection_clear()
    # populates data from the db
    if tabs.index(CURRENT) == 4:
        populateDoctors()
    if tabs.index(CURRENT) == 6:
        populatePatients()
    if tabs.index(CURRENT) == 7:
        populateAppointments()
    # clearing all the forms in the application
    exUserId_Entry.delete(0, END)
    newUserName_Entry.delete(0, END)
    newUserPlace_Entry.delete(0, END)
    newUserAge_Entry.delete(0, END)
    newUserPhone_Entry.delete(0, END)
    genTokenRefNum_Entry.delete(0, END)


tabs.bind('<<NotebookTabChanged>>', handleTabChange)


root.mainloop()  # the app keeps on listening for events
fns.closeDatabase()  # closes database
