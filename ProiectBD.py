import tkinter as tk  
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import pyodbc
import ctypes
import datetime as dt

base = tk.Tk()  
  
width = base.winfo_screenwidth()
height = base.winfo_screenheight()
base.geometry("%dx%d" % (width, height))

# CONEXIUNE 

conexiune = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=CLAUDIU-PC\\SQLEXPRESS;"
    "Database=AplicatieBD;"
    "Trusted_Conection=yes;"
)

# FUNCTIA INREGISTARE

def formatEmailIncorect(email):
    at = -1
    dot = -1
    for i in range (len(email)):
        if email[i] == '@':
            at = i
        elif email[i] == '.':
            dot = i
    if(at == -1 and dot == -1):
        return 0
    elif(at > dot):
        return 0
    else:
        return 1
    
def usernameExistent(username):
    cursor = conexiune.cursor()
    verificare = cursor.execute(
        "select * from Login where Username = ?",
        (username.get())
    )
    if (verificare.fetchone()):
        return 0
    else:
        return 1
    

def inregistrare():
    if ((len(nume1.get()) != 0) and (len(prenume1.get()) != 0) and (len(email1.get()) != 0) and (len(nrTelefon1.get()) != 0) and 
    (len(parola1.get()) != 0) and (len(confirmareParola1.get()) != 0)):
        if (formatEmailIncorect(email1.get()) == 1):
            if parola1.get() == confirmareParola1.get():
                if usernameExistent(username1) == 1:
                    messagebox.showinfo("Register", "Felicitări! Contul a fost creat cu succes!")
                    cursor = conexiune.cursor()

                    cursor.execute(
                        "insert into Operator(Nume,Prenume,Email,NumarDeTelefon) values(?,?,?,?);",
                        (nume1.get(), prenume1.get(), email1.get(), nrTelefon1.get())
                    )

                    cursor.execute(     
                        "insert into Login(Username, Password) values(?,?);",
                        (username1.get(), parola1.get())
                    )
                    conexiune.commit()  
                    for widget in base.winfo_children():
                        if isinstance(widget, tk.Entry):
                            widget.delete(0,'end')
                else:
                    messagebox.showerror("ERROR","Inregistrare ESUATĂ. Username existent!")
            else:
                messagebox.showerror("ERROR","Inregistrare ESUATĂ. Parolele nu corespund!")
        else:
            messagebox.showerror("ERROR","Inregistrare ESUATĂ. FORMAT EMAIL INCORECT!")
    else:
        messagebox.showerror("ERROR", "Inregistrare ESUATĂ. CEL PUȚIN UN CÂMP ESTE NECOMPLETAT!")

# FUNCTIA CLEAR

def clear():
    for widget in base.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0,'end')



# Functii DESIGN

def primaPagina():
    for widget in base.winfo_children():
        widget.destroy()
    
    base.title('Prima Pagina') 
    base.config(bg= "#D3F0EF") 

    label0 = tk.Label(base, text="SERVICIUL 112 - Siguranța ta este preocuparea noastră", font=("Times", 24, "italic"), bg= "#D3F0EF")  
    label0.place(relx=0.5,rely=0.1, anchor='center')  

    buton1 = tk.Button(base, text='AM DEJA UN CONT - LOGIN', height=4, width=60, bg="red",fg='blue', command=loginOperator)
    buton2 = tk.Button(base, text='NU AM INCA UN CONT - REGISTER', height=4, width=60, bg="black",fg='white', command=creareContOperator) 
        
    buton1.place(relx=0.5,rely=0.4,anchor='center') 
    buton2.place(relx=0.5,rely=0.5,anchor='center') 

    destroyButton = tk.Button(base, text="Close Program", width=20,height=2,bg='brown',fg='white',command=closeProgram)
    destroyButton.pack()
    destroyButton.place(anchor='center',relx=0.5,rely=0.88)

    ramaStanga = tk.Frame(base)
    ramaStanga.pack()
    ramaStanga.place(anchor='center',relx=0.2, rely=0.5)

    ramaDreapta = tk.Frame(base)
    ramaDreapta.pack()
    ramaDreapta.place(anchor='center', relx=0.8, rely=0.5)

    imgStg = Image.open("C:\\Users\\cbora\\OneDrive\\Desktop\\ambulanta.jpg")
    resized1 = imgStg.resize((420, 320), Image.Resampling.LANCZOS)
    imgStanga = ImageTk.PhotoImage(resized1)


    imgDr = Image.open("C:\\Users\\cbora\\OneDrive\\Desktop\\112.jpg")
    resized2 = imgDr.resize((420, 320), Image.Resampling.LANCZOS)
    imgDreapta = ImageTk.PhotoImage(resized2)

    label1 = tk.Label(ramaStanga, image = imgStanga).pack()
    label2 = tk.Label(ramaDreapta, image = imgDreapta).pack()

    label1.image = imgStanga # type: ignore
    label2.image = imgDreapta # type: ignore


def creareContOperator():
    for widget in base.winfo_children():
        widget.destroy()

    global nume1, prenume1, email1, nrTelefon1, username1, parola1, confirmareParola1

    base.title('Creare Cont Operator Apeluri') 
    base.config(bg= "#D3F0EF") 

    label0 = tk.Label(base, text="Creare Cont Operator Apeluri", font=("Times", 24, "italic"), bg= "#D3F0EF")  
    label0.place(relx=0.5,rely=0.1, anchor='center')

    label1 = tk.Label(base, text="Nume",bg = "#D3F0EF")
    label1.pack()
    label1.place(anchor='center',relx=0.4,rely=0.3)

    nume1 = tk.Entry(base, width=30)
    nume1.pack()
    nume1.place(anchor='center',relx=0.5, rely = 0.3)

    label2 = tk.Label(base, text="Prenume",bg = "#D3F0EF")
    label2.pack()
    label2.place(anchor='center',relx=0.4,rely=0.35)

    prenume1 = tk.Entry(base, width=30)
    prenume1.pack()
    prenume1.place(anchor='center',relx=0.5, rely = 0.35)

    label3 = tk.Label(base, text="Email",bg = "#D3F0EF")
    label3.pack()
    label3.place(anchor='center',relx=0.4,rely=0.4)

    email1 = tk.Entry(base, width=30)
    email1.pack()
    email1.place(anchor='center',relx=0.5, rely = 0.4)

    label4 = tk.Label(base, text="Număr de telefon",bg = "#D3F0EF")
    label4.pack()
    label4.place(anchor='center',relx=0.4,rely=0.45)

    nrTelefon1 = tk.Entry(base, width=30)
    nrTelefon1.pack()
    nrTelefon1.place(anchor='center',relx=0.5, rely = 0.45)

    label5 = tk.Label(base, text="Username",bg = "#D3F0EF")
    label5.pack()
    label5.place(anchor='center',relx=0.4,rely=0.5)

    username1 = tk.Entry(base, width=30)
    username1.pack()
    username1.place(anchor='center',relx=0.5, rely = 0.5)

    label6 = tk.Label(base, text="Parolă",bg = "#D3F0EF")
    label6.pack()
    label6.place(anchor='center',relx=0.4,rely=0.55)

    parola1 = tk.Entry(base, show='*', width=30)
    parola1.pack()
    parola1.place(anchor='center',relx=0.5, rely = 0.55)

    label7 = tk.Label(base, text="Confirmare parolă",bg = "#D3F0EF")
    label7.pack()
    label7.place(anchor='center',relx=0.4,rely=0.6)

    confirmareParola1 = tk.Entry(base, show='*', width=30)
    confirmareParola1.pack()
    confirmareParola1.place(anchor='center',relx=0.5, rely = 0.6)

    submitButton = tk.Button(base, text = "SUBMIT REGISTER", width=20,height=2,bg='brown',fg='white',command=inregistrare)
    submitButton.pack()
    submitButton.place(anchor='center',relx=0.4,rely=0.67)

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=primaPagina, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.5, rely = 0.8,anchor='center')

    clearButton = tk.Button(base, text="Clear", width=20,height=2,bg='brown',fg='white',command=clear)
    clearButton.pack()
    clearButton.place(anchor='center',relx=0.6,rely=0.67)

    destroyButton = tk.Button(base, text="Close Program", width=20,height=2,bg='brown',fg='white',command=closeProgram)
    destroyButton.pack()
    destroyButton.place(anchor='center',relx=0.5,rely=0.88)

#-------------------------------------------------------------------------------------------------------------------------------


def loginOperator():
    for widget in base.winfo_children():
        widget.destroy()
    
    global username2, password2, numeUtilizator, parolaUtilizator

    numeUtilizator = tk.StringVar()
    parolaUtilizator = tk.StringVar()

    base.title('Login Operator 112') 
    base.config(bg= "#D3F0EF") 

    label0 = tk.Label(base, text='LOGIN OPERATOR 112', font=("Times", 24, "italic"), bg= "#D3F0EF")
    label0.place(relx=0.5,rely=0.1, anchor='center')  

    label1 = tk.Label(base, text="Username",bg = "#D3F0EF")
    label1.pack()
    label1.place(anchor='center',relx=0.4,rely=0.5)

    label2 = tk.Label(base, text="Password",bg = "#D3F0EF")
    label2.pack()
    label2.place(anchor='center',relx=0.4,rely=0.6)

    username2 = tk.Entry(base, width=30, textvariable=numeUtilizator)
    username2.pack()
    username2.place(anchor='center',relx=0.5, rely = 0.5)

    password2 = tk.Entry(base, width=30,show='*',textvariable=parolaUtilizator)
    password2.pack()
    password2.place(anchor='center',relx=0.5, rely = 0.6)

    backButton0 = tk.Button(base, text="Înapoi",width=30, height=3, command=primaPagina, fg='white',bg='black')
    backButton0.pack()
    backButton0.place(relx = 0.5, rely = 0.8,anchor='center')

    submitButton = tk.Button(base, text = "LOGIN", width=20,height=2,bg='brown',fg='white',command=dupaLogin)
    submitButton.pack()
    submitButton.place(anchor='center',relx=0.4,rely=0.7)
    
    clearButton = tk.Button(base, text="Clear", width=20,height=2,bg='brown',fg='white',command=clear)
    clearButton.pack()
    clearButton.place(anchor='center',relx=0.6,rely=0.7)

    destroyButton = tk.Button(base, text="Close Program", width=20,height=2,bg='brown',fg='white',command=closeProgram)
    destroyButton.pack()
    destroyButton.place(anchor='center',relx=0.5,rely=0.88)

    rama = tk.Frame(base)
    rama.pack()
    rama.place(anchor='center', relx=0.5, rely=0.3)
    
    img = Image.open("C:\\Users\\cbora\\OneDrive\\Desktop\\login.png")
    resized = img.resize((330, 150), Image.Resampling.LANCZOS)
    img1 = ImageTk.PhotoImage(resized)

    label1 = tk.Label(rama, image = img1).pack()
    label1.image = img1 # type: ignore


def dupaLogin():

    cursor = conexiune.cursor()
    verificare = cursor.execute(
        "select * from Login where Username = ? and Password = ?;",
        (numeUtilizator.get(), parolaUtilizator.get())
    )
    if (verificare.fetchone()):

        for widget in base.winfo_children():
            widget.destroy()
        
        base.title('Pagina Operator 112') 
        base.config(bg= "#D3F0EF")

        label0 = tk.Label(base, text='Bine ati venit', font=("Times", 24, "italic"), bg= "#D3F0EF")
        label0.place(relx=0.47,rely=0.1, anchor='center')

        label00 = tk.Label(base,textvariable=numeUtilizator, font=("Times", 24, "italic"), bg= "#D3F0EF")
        label00.place(relx=0.53,rely=0.1, anchor='w')

        vizualizareApeluri = tk.Button(base, text="Vizualizare Apeluri", width=23, height=3, fg='white',bg='black',command=vizApel)
        vizualizareApeluri.pack()
        vizualizareApeluri.place(relx=0.27, rely=0.3,anchor='center')

        vizualizareLocatii = tk.Button(base, text="Vizualizare Locatii", width=23, height=3, fg='white',bg='black',command=vizLocatie)
        vizualizareLocatii.pack()
        vizualizareLocatii.place(relx=0.42, rely=0.3,anchor='center')

        vizualizareInterventii = tk.Button(base, text="Vizualizare Interventii", width=23, height=3, fg='white',bg='black',command=vizInterventie)
        vizualizareInterventii.pack()
        vizualizareInterventii.place(relx=0.57, rely=0.3,anchor='center')

        vizualizareServicii = tk.Button(base, text="Vizualizare Servicii", width=23, height=3, fg='white',bg='black',command=vizServicii)
        vizualizareServicii.pack()
        vizualizareServicii.place(relx=0.72, rely=0.3,anchor='center')

        adaugareApel = tk.Button(base, text="Adăugare apel baza de date",width=30, height=3, fg='white',bg='black', command=adaugaApel)
        adaugareApel.pack()
        adaugareApel.place(relx = 0.3, rely = 0.4,anchor='center')

        adaugareLocatie = tk.Button(base, text="Adăugare locație baza de date",width=30, height=3, fg='white',bg='black',command=adaugaLocatie)
        adaugareLocatie.pack()
        adaugareLocatie.place(relx = 0.5, rely = 0.4,anchor='center')

        adaugareInterventie = tk.Button(base, text="Adăugare intervenție baza de date",width=30, height=3, fg='white',bg='black',command=adaugaInterventie)
        adaugareInterventie.pack()
        adaugareInterventie.place(relx = 0.7, rely = 0.4,anchor='center')

        updateApel = tk.Button(base, text="Modificare apel existent",width=30, height=3, fg='white',bg='black', command=modificaApel)
        updateApel.pack()
        updateApel.place(relx = 0.3, rely = 0.5,anchor='center')

        updateLocatie = tk.Button(base, text="Modificare locatie existentă", width=30, height=3, fg='white', bg='black',command=modificaLocatie)
        updateLocatie.pack()
        updateLocatie.place(relx = 0.5, rely = 0.5, anchor='center')
        
        updateInterventie = tk.Button(base, text="Modificare interventie existentă", width=30, height=3, fg='white', bg='black',command=modificaInterventie)
        updateInterventie.pack()
        updateInterventie.place(relx = 0.7, rely = 0.5, anchor='center')

        stergeApel = tk.Button(base, text="Stergere apel",width=30, height=3, fg='white',bg='black', command=deleteApel)
        stergeApel.pack()
        stergeApel.place(relx = 0.3, rely = 0.6,anchor='center')

        stergeLocatie = tk.Button(base, text="Stergere locatie", width=30, height=3, fg='white', bg='black',command=deleteLocatie)
        stergeLocatie.pack()
        stergeLocatie.place(relx = 0.5, rely = 0.6, anchor='center')

        stergeInterventie = tk.Button(base, text="Stergere interventie", width=30, height=3, fg='white', bg='black',command=deleteInterventie)
        stergeInterventie.pack()
        stergeInterventie.place(relx = 0.7, rely = 0.6, anchor='center')

        statistici = tk.Button(base, text="Statistici", width=30, height=3, fg='white', bg='black',command=statisticaSimpla1)
        statistici.pack()
        statistici.place(relx = 0.5, rely = 0.2, anchor='center')
        
        backButton = tk.Button(base, text="LOGOUT",width=30, height=3, command=loginOperator, fg='white',bg='brown')
        backButton.pack()
        backButton.place(relx = 0.5, rely = 0.75,anchor='center')

        destroyButton = tk.Button(base, text="Close Program", width=20,height=2,bg='brown',fg='white',command=closeProgram)
        destroyButton.pack()
        destroyButton.place(anchor='center',relx=0.5,rely=0.88)

    else:
        messagebox.showerror("ERROR", "Autentificare eșuată! Username sau parolă incorecte!")

#-------------------------------------------------------------------------------------------------

def adaugaApel():
    for widget in base.winfo_children():
        widget.destroy()
        
    base.title('Apel 112') 
    base.config(bg= "#D3F0EF")

    global operatorID, interventieID, durataApelMinute, durataApelSecunde, numeApelant, prenumeApelant, numarTelefon

    label00 = tk.Label(base, text='Adăugare apel 112', font=("Times", 24, "italic"), bg= "#D3F0EF")
    label00.place(relx=0.5,rely=0.1, anchor='center')

    label0 = tk.Label(base, text="ID-ul d-voastra",bg = "#D3F0EF")
    label0.pack()
    label0.place(anchor='center',relx=0.4,rely=0.35)
    
    operatorID = tk.Entry(base, width=30)
    operatorID.pack()
    operatorID.place(anchor='center',relx=0.5, rely = 0.35)

    label1 = tk.Label(base, text="ID-ul interventiei",bg = "#D3F0EF")
    label1.pack()
    label1.place(anchor='center',relx=0.4,rely=0.4)
    
    interventieID = tk.Entry(base, width=30)
    interventieID.pack()
    interventieID.place(anchor='center',relx=0.5, rely = 0.4)
    
    label2 = tk.Label(base, text="Durată apel",bg = "#D3F0EF")
    label2.pack()
    label2.place(anchor='center',relx=0.4,rely=0.45)
    
    durataApelMinute = ttk.Combobox(base, width=10)
    durataApelMinute.pack()
    durataApelMinute['values']=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
    33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59)
    durataApelMinute.set('Minute')
    durataApelMinute.place(anchor='center',relx=0.47, rely = 0.45)
    
    durataApelSecunde = ttk.Combobox(base, width=10)
    durataApelSecunde.pack()
    durataApelSecunde['values']=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
    33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59)
    durataApelSecunde.set('Secunde')
    durataApelSecunde.place(anchor='center',relx=0.53, rely = 0.45)

    label3 = tk.Label(base, text="Nume apelant",bg = "#D3F0EF")
    label3.pack()
    label3.place(anchor='center',relx=0.4,rely=0.5)

    numeApelant = tk.Entry(base, width=30)
    numeApelant.pack()
    numeApelant.place(anchor='center',relx=0.5, rely = 0.5)

    label4 = tk.Label(base, text="Prenume apelant",bg = "#D3F0EF")
    label4.pack()
    label4.place(anchor='center',relx=0.4,rely=0.55)

    prenumeApelant = tk.Entry(base, width=30)
    prenumeApelant.pack()
    prenumeApelant.place(anchor='center',relx=0.5, rely = 0.55)

    label5 = tk.Label(base, text="Număr de telefon",bg = "#D3F0EF")
    label5.pack()
    label5.place(anchor='center',relx=0.4,rely=0.6)

    numarTelefon = tk.Entry(base, width=30)
    numarTelefon.pack()
    numarTelefon.place(anchor='center',relx=0.5, rely = 0.6)

    submitButton = tk.Button(base, text = "SUBMIT REGISTER", width=20,height=2,bg='brown',fg='white',command=adaugareApelBazaDeDate)
    submitButton.pack()
    submitButton.place(anchor='center',relx=0.4,rely=0.67)

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.5, rely = 0.8,anchor='center')

    clearButton = tk.Button(base, text="Clear", width=20,height=2,bg='brown',fg='white',command=clear)
    clearButton.pack()
    clearButton.place(anchor='center',relx=0.6,rely=0.67)

    destroyButton = tk.Button(base, text="Close Program", width=20,height=2,bg='brown',fg='white',command=closeProgram)
    destroyButton.pack()
    destroyButton.place(anchor='center',relx=0.5,rely=0.88)

def adaugareApelBazaDeDate():

    var1 = int(durataApelMinute.get())
    var2 = int(durataApelSecunde.get())
    durataApel = dt.time(0, var1, var2) 
    var3 = tk.StringVar()
    var3 = str(durataApel)
    
    cursor1 = conexiune.cursor()
    check = cursor1.execute(
        "select * from Operator where OperatorID = ?;",
        (operatorID.get())
    )
    if(check.fetchone()):
        check2 = cursor1.execute(
        "select * from Interventie where InterventieID = ?;",
        (interventieID.get())
        )
        if(check2.fetchone()):
            messagebox.showinfo("SUCCES", "Apel adăugat cu succes!")

            cursor = conexiune.cursor()
            cursor.execute(
                "insert into Apel(OperatorID,InterventieID, DurataApel,NumeApelant,PrenumeApelant,NumarDeTelefon) values(?,?,?,?,?,?);",
                (operatorID.get(), interventieID.get(), var3, numeApelant.get(), prenumeApelant.get(), numarTelefon.get())
            )
            conexiune.commit()  

            for widget in base.winfo_children():
                if isinstance(widget, tk.Entry):
                    widget.delete(0,'end')
        else:
            messagebox.showwarning("WARNING", "ID-ul interventiei este inexistent!")
    else:
        messagebox.showwarning("WARNING", "ID-ul operatorului este inexistent!")
#----------------------------------------------------------------------------------------------

def adaugaLocatie():
    for widget in base.winfo_children():
        widget.destroy()
        
    base.title('Locație') 
    base.config(bg= "#D3F0EF")

    global longOra, longMinute, longSecunde, latOra, latMinute, latSecunde

    label0 = tk.Label(base, text='Locație Intervenție', font=("Times", 24, "italic"), bg= "#D3F0EF")
    label0.place(relx=0.5,rely=0.1, anchor='center')

    label1 = tk.Label(base, text="Longitudine Oră",bg = "#D3F0EF")
    label1.pack()
    label1.place(anchor='center',relx=0.4,rely=0.4)
    
    longOra = tk.Entry(base, width=30)
    longOra.pack()
    longOra.place(anchor='center',relx=0.5, rely = 0.4)
    
    label2 = tk.Label(base, text="Longitudine Minute",bg = "#D3F0EF")
    label2.pack()
    label2.place(anchor='center',relx=0.4,rely=0.45)

    longMinute = tk.Entry(base, width=30)
    longMinute.pack()
    longMinute.place(anchor='center',relx=0.5, rely = 0.45)

    label3 = tk.Label(base, text="Longitudine Secunde",bg = "#D3F0EF")
    label3.pack()
    label3.place(anchor='center',relx=0.4,rely=0.5)
    
    longSecunde = tk.Entry(base, width=30)
    longSecunde.pack()
    longSecunde.place(anchor='center',relx=0.5, rely = 0.5)
    
    label4 = tk.Label(base, text="Latitudine Oră",bg = "#D3F0EF")
    label4.pack()
    label4.place(anchor='center',relx=0.4,rely=0.55)

    latOra = tk.Entry(base, width=30)
    latOra.pack()
    latOra.place(anchor='center',relx=0.5, rely = 0.55)

    label5 = tk.Label(base, text="Latitudine Minute",bg = "#D3F0EF")
    label5.pack()
    label5.place(anchor='center',relx=0.4,rely=0.6)
    
    latMinute = tk.Entry(base, width=30)
    latMinute.pack()
    latMinute.place(anchor='center',relx=0.5, rely = 0.6)
    
    label6 = tk.Label(base, text="Latitudine Secunde",bg = "#D3F0EF")
    label6.pack()
    label6.place(anchor='center',relx=0.4,rely=0.65)

    latSecunde = tk.Entry(base, width=30)
    latSecunde.pack()
    latSecunde.place(anchor='center',relx=0.5, rely = 0.65)

    submitButton = tk.Button(base, text = "SUBMIT REGISTER", width=20,height=2,bg='brown',fg='white',command=adaugareLocatieBazaDeDate)
    submitButton.pack()
    submitButton.place(anchor='center',relx=0.4,rely=0.7)

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.5, rely = 0.8,anchor='center')

    clearButton = tk.Button(base, text="Clear", width=20,height=2,bg='brown',fg='white',command=clear)
    clearButton.pack()
    clearButton.place(anchor='center',relx=0.6,rely=0.7)

    destroyButton = tk.Button(base, text="Close Program", width=20,height=2,bg='brown',fg='white',command=closeProgram)
    destroyButton.pack()
    destroyButton.place(anchor='center',relx=0.5,rely=0.88)


def adaugareLocatieBazaDeDate():

    if(int(longOra.get()) > 180 or int(longOra.get()) < -180):
        messagebox.showwarning("WARNING", "LONGITUDINE ORA INCORECTĂ")
    elif(int(longMinute.get()) > 180 or int(longMinute.get()) < -180):
        messagebox.showwarning("WARNING", "LONGITUDINE MINUTE INCORECTE")
    elif(int(longSecunde.get()) > 180 or int(longSecunde.get()) < -180):
        messagebox.showwarning("WARNING", "LONGITUDINE SECUNDE INCORECTE")
    elif(int(latOra.get()) > 90 or int(latOra.get()) < -90):
        messagebox.showwarning("WARNING", "LATITUDINE ORA INCORECTĂ")
    elif(int(latMinute.get()) > 90 or int(latMinute.get()) < -90):
        messagebox.showwarning("WARNING", "LATITUDINE MINUTE INCORECTE")
    elif(int(latSecunde.get()) > 90 or int(latSecunde.get()) < -90):
        messagebox.showwarning("WARNING", "LATITUDINE SECUNDE INCORECTE")
    else:
        messagebox.showinfo("SUCCES", "LOCAȚIA A FOST ÎNREGISTRATĂ CU SUCCES")
        cursor = conexiune.cursor()
        cursor.execute(
            "insert into Locatie(LongitudineOra,LongitudineMinute,LongitudineSecunde,LatitudineOra,LatitudineMinute,LatitudineSecunde) values(?,?,?,?,?,?);",
            (longOra.get(), longMinute.get(), longSecunde.get(), latOra.get(), latMinute.get(), latSecunde.get())
        )
        conexiune.commit()
        for widget in base.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0,'end')
#----------------------------------------------------------------------------------------------

def adaugaInterventie():
    for widget in base.winfo_children():
        widget.destroy()
        
    base.title('Intervenție') 
    base.config(bg= "#D3F0EF")

    global zi, luna, an, ora, minut, tip

    label0 = tk.Label(base, text='Intervenție 112', font=("Times", 24, "italic"), bg= "#D3F0EF")
    label0.place(relx=0.5,rely=0.1, anchor='center')
    
    label1 = tk.Label(base, text="Data Intervenție",bg = "#D3F0EF")
    label1.pack()
    label1.place(anchor='center',relx=0.4,rely=0.5)

    zi = ttk.Combobox(base, width=6)
    zi.pack()
    zi['values']=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
    zi.set('Zi')
    zi.place(anchor='center',relx=0.46, rely = 0.5)

    luna = ttk.Combobox(base, width=6)
    luna.pack()
    luna['values']=(1,2,3,4,5,6,7,8,9,10,11,12)
    luna.set('Lună')
    luna.place(anchor='center',relx=0.5, rely = 0.5)

    an = ttk.Combobox(base, width=6)
    an.pack()
    an['values']=(2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023)
    an.set('An')
    an.place(anchor='center',relx=0.54, rely = 0.5)
    
    label2 = tk.Label(base, text="Oră Intervenție",bg = "#D3F0EF")
    label2.pack()
    label2.place(anchor='center',relx=0.4,rely=0.55)

    ora = ttk.Combobox(base, width=11)
    ora.pack()
    ora['values']=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23)
    ora.set('Oră')
    ora.place(anchor='center',relx=0.47, rely = 0.55)

    minut = ttk.Combobox(base, width=11)
    minut.pack()
    minut['values']=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,
    40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59)
    minut.set('Minut')
    minut.place(anchor='center',relx=0.53, rely = 0.55)

    label3 = tk.Label(base, text="Tip Intervenție",bg = "#D3F0EF")
    label3.pack()
    label3.place(anchor='center',relx=0.4,rely=0.6)
    
    tip = ttk.Combobox(base, width=30)
    tip.pack()
    tip['values']=("Incheiată", "Anulată", "În desfasurare")
    tip.place(anchor='center',relx=0.5, rely = 0.6)

    submitButton = tk.Button(base, text = "SUBMIT REGISTER", width=20,height=2,bg='brown',fg='white',command=adaugareInterventieBazaDeDate)
    submitButton.pack()
    submitButton.place(anchor='center',relx=0.4,rely=0.7)

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.5, rely = 0.8,anchor='center')

    clearButton = tk.Button(base, text="Clear", width=20,height=2,bg='brown',fg='white',command=clear)
    clearButton.pack()
    clearButton.place(anchor='center',relx=0.6,rely=0.7)

    destroyButton = tk.Button(base, text="Close Program", width=20,height=2,bg='brown',fg='white',command=closeProgram)
    destroyButton.pack()
    destroyButton.place(anchor='center',relx=0.5,rely=0.88)

def adaugareInterventieBazaDeDate():
    var1 = int(zi.get())
    var2 = int(luna.get())
    var3 = int(an.get())
    dataInterventie = dt.date(var3, var2, var1) 
    var4 = tk.StringVar()
    var4 = str(dataInterventie)

    var5 = int(ora.get())
    var6 = int(minut.get())
    oraInterventie = dt.time(var5, var6)
    var7 = tk.StringVar()
    var7 = str(oraInterventie)

    cursor = conexiune.cursor()
    cursor.execute(
        "insert into Interventie(Data,Ora,Tip) values(?,?,?);",
        (var4, var7, tip.get())
    )
    conexiune.commit()
    for widget in base.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0,'end')
#----------------------------------------------------------------------------------------------

def vizApel():
    for widget in base.winfo_children():
        widget.destroy()
         
    base.title('Apeluri') 
    base.config(bg= "#D3F0EF")

    global cautareComboApel, cautareApel

    cursor = conexiune.cursor()
    cursor.execute(
        "select DurataApel, NumeApelant, PrenumeApelant, NumarDeTelefon from Apel"
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)
    
    tv.heading(1,text="Durata Apel")
    tv.heading(2,text="Nume Apelant")
    tv.heading(3,text="Prenume Apelant")
    tv.heading(4,text="Numar de telefon")

    vizualizareApeluri = tk.Button(base, text="Refresh", width=23, height=3, fg='white',bg='green',command=vizApel)
    vizualizareApeluri.pack()
    vizualizareApeluri.place(relx=0.27, rely=0.8,anchor='center')

    vizualizareLocatii = tk.Button(base, text="Vizualizare Locatii", width=23, height=3, fg='white',bg='black',command=vizLocatie)
    vizualizareLocatii.pack()
    vizualizareLocatii.place(relx=0.42, rely=0.8,anchor='center')

    vizualizareInterventii = tk.Button(base, text="Vizualizare Interventii", width=23, height=3, fg='white',bg='black',command=vizInterventie)
    vizualizareInterventii.pack()
    vizualizareInterventii.place(relx=0.57, rely=0.8,anchor='center')

    vizualizareServicii = tk.Button(base, text="Vizualizare Servicii", width=23, height=3, fg='white',bg='black',command=vizServicii)
    vizualizareServicii.pack()
    vizualizareServicii.place(relx=0.72, rely=0.8,anchor='center')

    cautareComboApel = ttk.Combobox(base, width=15)
    cautareComboApel.pack()
    cautareComboApel['values']=("Durata Apel", "Nume Apelant", "Prenume Apelant", "Numar de Telefon")
    cautareComboApel.place(relx=0.53, rely=0.5,anchor='center')
    
    cautareApel = tk.Button(base, text="Cautare", width=23, height=3, fg='white',bg='black',command=cautareApelBazaDeDate)
    cautareApel.pack()
    cautareApel.place(relx=0.42, rely=0.5,anchor='center')

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.5, rely = 0.7,anchor='center')


    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3]))  


def cautareApelBazaDeDate():
    global searchEntryApel, searchFrameApel, searchButtonApel
    
    if(cautareComboApel.get() == "Durata Apel"):
        cautareComboApel.destroy()
        cautareApel.destroy()

        searchFrameApel = tk.LabelFrame(base, text="Cautare dupa durata apel")
        searchFrameApel.pack(padx=10, pady=10)

        searchEntryApel = tk.Entry(searchFrameApel, font=("Helvetica"))
        searchEntryApel.pack(pady=20, padx=20)

        searchButtonApel = tk.Button(base, text="Cautare",command=cautareApelDupaDurata)
        searchButtonApel.pack(padx=20, pady=20)

    elif(cautareComboApel.get() == "Nume Apelant"):
        cautareComboApel.destroy()
        cautareApel.destroy()
        
        searchFrameApel = tk.LabelFrame(base, text="Cautare dupa nume apelant")
        searchFrameApel.pack(padx=10, pady=10)

        searchEntryApel = tk.Entry(searchFrameApel, font=("Helvetica"))
        searchEntryApel.pack(pady=20, padx=20)

        searchButtonApel = tk.Button(base, text="Cautare",command=cautareApelDupaNumeApelant)
        searchButtonApel.pack(padx=20, pady=20)

    elif(cautareComboApel.get() == "Prenume Apelant"):
        cautareComboApel.destroy()
        cautareApel.destroy()

        searchFrameApel = tk.LabelFrame(base, text="Cautare dupa prenume apelant")
        searchFrameApel.pack(padx=10, pady=10)

        searchEntryApel = tk.Entry(searchFrameApel, font=("Helvetica"))
        searchEntryApel.pack(pady=20, padx=20)

        searchButtonApel = tk.Button(base, text="Cautare",command=cautareApelDupaPrenumeApelant)
        searchButtonApel.pack(padx=20, pady=20)

    elif(cautareComboApel.get() == "Numar de Telefon"):
        cautareComboApel.destroy()
        cautareApel.destroy()

        searchFrameApel = tk.LabelFrame(base, text="Cautare dupa numar de telefon")
        searchFrameApel.pack(padx=10, pady=10)

        searchEntryApel = tk.Entry(searchFrameApel, font=("Helvetica"))
        searchEntryApel.pack(padx=20, pady=20)

        searchButtonApel = tk.Button(base, text="Cautare",command=cautareApelDupaNrTel)
        searchButtonApel.pack(padx=20, pady=20)
    else:
        messagebox.showwarning("WARNING", "Trebuie sa selectati un criteriu de cautare!")


def cautareApelDupaDurata():
    lookupRecordApel = searchEntryApel.get()

    searchFrameApel.destroy()
    searchButtonApel.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select DurataApel, NumeApelant, PrenumeApelant, NumarDeTelefon from Apel where DurataApel = ?;",
        (lookupRecordApel)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Durata Apel")
    tv.heading(2,text="Nume Apelant")
    tv.heading(3,text="Prenume Apelant")
    tv.heading(4,text="Numar de Telefon")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3])) 

def cautareApelDupaNumeApelant():
    lookupRecordApel = searchEntryApel.get()

    searchFrameApel.destroy()
    searchButtonApel.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select DurataApel, NumeApelant, PrenumeApelant, NumarDeTelefon from Apel where NumeApelant = ?;",
        (lookupRecordApel)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Durata Apel")
    tv.heading(2,text="Nume Apelant")
    tv.heading(3,text="Prenume Apelant")
    tv.heading(4,text="Numar de Telefon")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3])) 

def cautareApelDupaPrenumeApelant():
    lookupRecordApel = searchEntryApel.get()

    searchFrameApel.destroy()
    searchButtonApel.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select DurataApel, NumeApelant, PrenumeApelant, NumarDeTelefon from Apel where PrenumeApelant = ?;",
        (lookupRecordApel)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Durata Apel")
    tv.heading(2,text="Nume Apelant")
    tv.heading(3,text="Prenume Apelant")
    tv.heading(4,text="Numar de Telefon")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3])) 

def cautareApelDupaNrTel():
    lookupRecordApel = searchEntryApel.get()

    searchFrameApel.destroy()
    searchButtonApel.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select DurataApel, NumeApelant, PrenumeApelant, NumarDeTelefon from Apel where NumarDeTelefon = ?;",
        (lookupRecordApel)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Durata Apel")
    tv.heading(2,text="Nume Apelant")
    tv.heading(3,text="Prenume Apelant")
    tv.heading(4,text="Numar de Telefon")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3])) 
#-------------------------------------------------------------------------

def vizServicii():
    for widget in base.winfo_children():
        widget.destroy()
         
    base.title('Servicii 112') 
    base.config(bg= "#D3F0EF")

    global cautareComboServiciu, cautareServiciu

    cursor = conexiune.cursor()
    cursor.execute(
        "select NumeServiciu, NumarVehicule, NumarOameni from Serviciu112"
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Nume Serviciu 112")
    tv.heading(2,text="Numar Vehicule")
    tv.heading(3,text="Numar Oameni angajati")

    vizualizareApeluri = tk.Button(base, text="Vizualizare Apeluri", width=23, height=3, fg='white',bg='black',command=vizApel)
    vizualizareApeluri.pack()
    vizualizareApeluri.place(relx=0.27, rely=0.8,anchor='center')

    vizualizareLocatii = tk.Button(base, text="Vizualizare Locatii", width=23, height=3, fg='white',bg='black',command=vizLocatie)
    vizualizareLocatii.pack()
    vizualizareLocatii.place(relx=0.42, rely=0.8,anchor='center')

    vizualizareInterventii = tk.Button(base, text="Vizualizare Interventii", width=23, height=3, fg='white',bg='black',command=vizInterventie)
    vizualizareInterventii.pack()
    vizualizareInterventii.place(relx=0.57, rely=0.8,anchor='center')

    vizualizareServicii = tk.Button(base, text="Refresh", width=23, height=3, fg='white',bg='green',command=vizServicii)
    vizualizareServicii.pack()
    vizualizareServicii.place(relx=0.72, rely=0.8,anchor='center')

    cautareComboServiciu = ttk.Combobox(base, width=15)
    cautareComboServiciu.pack()
    cautareComboServiciu['values']=("Nume Serviciu", "Numar Vehicule", "Numar Oameni")
    cautareComboServiciu.place(relx=0.53, rely=0.5,anchor='center')
    
    cautareServiciu = tk.Button(base, text="Cautare", width=23, height=3, fg='white',bg='black',command=cautareServiciuBazaDeDate)
    cautareServiciu.pack()
    cautareServiciu.place(relx=0.42, rely=0.5,anchor='center')

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.5, rely = 0.7,anchor='center')

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2]))  

def cautareServiciuBazaDeDate():
    global searchEntryServiciu, searchFrameServiciu, searchButtonServiciu
    
    if(cautareComboServiciu.get() == "Nume Serviciu"):
        cautareComboServiciu.destroy()
        cautareServiciu.destroy()

        searchFrameServiciu = tk.LabelFrame(base, text="Cautare dupa nume")
        searchFrameServiciu.pack(padx=10, pady=10)

        searchEntryServiciu = tk.Entry(searchFrameServiciu, font=("Helvetica"))
        searchEntryServiciu.pack(pady=20, padx=20)

        searchButtonServiciu = tk.Button(base, text="Cautare",command=cautareServiciuDupaNume)
        searchButtonServiciu.pack(padx=20, pady=20)

    elif(cautareComboServiciu.get() == "Numar Vehicule"):
        cautareComboServiciu.destroy()
        cautareServiciu.destroy()
        
        searchFrameServiciu = tk.LabelFrame(base, text="Cautare dupa numar vehicule")
        searchFrameServiciu.pack(padx=10, pady=10)

        searchEntryServiciu = tk.Entry(searchFrameServiciu, font=("Helvetica"))
        searchEntryServiciu.pack(pady=20, padx=20)

        searchButtonServiciu = tk.Button(base, text="Cautare",command=cautareServiciuDupaVehicule)
        searchButtonServiciu.pack(padx=20, pady=20)

    elif(cautareComboServiciu.get() == "Numar Oameni"):
        cautareComboServiciu.destroy()
        cautareServiciu.destroy()

        searchFrameServiciu = tk.LabelFrame(base, text="Cautare dupa numar oameni")
        searchFrameServiciu.pack(padx=10, pady=10)

        searchEntryServiciu = tk.Entry(searchFrameServiciu, font=("Helvetica"))
        searchEntryServiciu.pack(pady=20, padx=20)

        searchButtonServiciu = tk.Button(base, text="Cautare",command=cautareServiciuDupaOameni)
        searchButtonServiciu.pack(padx=20, pady=20)
    else:
        messagebox.showwarning("WARNING", "Trebuie sa selectati un criteriu de cautare!")


def cautareServiciuDupaNume():
    lookupRecordServiciu = searchEntryServiciu.get()

    searchFrameServiciu.destroy()
    searchButtonServiciu.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select NumeServiciu, NumarVehicule, NumarOameni from Serviciu112 where NumeServiciu = ?;",
        (lookupRecordServiciu)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Nume Serviciu 112")
    tv.heading(2,text="Numar Vehicule")
    tv.heading(3,text="Numar Oameni angajati")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2]))  

def cautareServiciuDupaVehicule():
    lookupRecordServiciu = searchEntryServiciu.get()

    searchFrameServiciu.destroy()
    searchButtonServiciu.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select NumeServiciu, NumarVehicule, NumarOameni from Serviciu112 where Numarvehicule = ?;",
        (lookupRecordServiciu)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Nume Serviciu 112")
    tv.heading(2,text="Numar Vehicule")
    tv.heading(3,text="Numar Oameni angajati")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2]))

def cautareServiciuDupaOameni():
    lookupRecordServiciu = searchEntryServiciu.get()

    searchFrameServiciu.destroy()
    searchButtonServiciu.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select NumeServiciu, NumarVehicule, NumarOameni from Serviciu112 where NumarOameni = ?;",
        (lookupRecordServiciu)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Nume Serviciu 112")
    tv.heading(2,text="Numar Vehicule")
    tv.heading(3,text="Numar Oameni angajati")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2]))    

#----------------------------------------------------------------------------------------------

def vizInterventie():
    for widget in base.winfo_children():
        widget.destroy()
         
    base.title('Interventii') 
    base.config(bg= "#D3F0EF")

    global cautareComboInterventie, cautareInterventie

    cursor = conexiune.cursor()
    cursor.execute(
        "select Data, Ora, Tip from Interventie"
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Data Interventiei")
    tv.heading(2,text="Ora Interventiei")
    tv.heading(3,text="Tipul")

    vizualizareApeluri = tk.Button(base, text="Vizualizare Apeluri", width=23, height=3, fg='white',bg='black',command=vizApel)
    vizualizareApeluri.pack()
    vizualizareApeluri.place(relx=0.27, rely=0.8,anchor='center')

    vizualizareLocatii = tk.Button(base, text="Vizualizare Locatii", width=23, height=3, fg='white',bg='black',command=vizLocatie)
    vizualizareLocatii.pack()
    vizualizareLocatii.place(relx=0.42, rely=0.8,anchor='center')

    vizualizareInterventii = tk.Button(base, text="Refresh", width=23, height=3, fg='white',bg='green',command=vizInterventie)
    vizualizareInterventii.pack()
    vizualizareInterventii.place(relx=0.57, rely=0.8,anchor='center')

    vizualizareServicii = tk.Button(base, text="Vizualizare Servicii", width=23, height=3, fg='white',bg='black',command=vizServicii)
    vizualizareServicii.pack()
    vizualizareServicii.place(relx=0.72, rely=0.8,anchor='center')

    cautareComboInterventie = ttk.Combobox(base, width=15)
    cautareComboInterventie.pack()
    cautareComboInterventie['values']=("Data Interventie", "Ora Interventie", "Tip Interventie")
    cautareComboInterventie.place(relx=0.53, rely=0.5,anchor='center')
    
    cautareInterventie = tk.Button(base, text="Cautare", width=23, height=3, fg='white',bg='black',command=cautareInterventieBazaDeDate)
    cautareInterventie.pack()
    cautareInterventie.place(relx=0.42, rely=0.5,anchor='center')

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.5, rely = 0.7,anchor='center')

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2]))  


def cautareInterventieBazaDeDate():
    global searchEntryInterventie, searchFrameInterventie, searchButtonInterventie
    
    if(cautareComboInterventie.get() == "Data Interventie"):
        cautareComboInterventie.destroy()
        cautareInterventie.destroy()

        searchFrameInterventie = tk.LabelFrame(base, text="Cautare dupa data")
        searchFrameInterventie.pack(padx=10, pady=10)

        searchEntryInterventie = tk.Entry(searchFrameInterventie, font=("Helvetica"))
        searchEntryInterventie.pack(pady=20, padx=20)

        searchButtonInterventie = tk.Button(base, text="Cautare",command=cautareInterventieDupaData)
        searchButtonInterventie.pack(padx=20, pady=20)

    elif(cautareComboInterventie.get() == "Ora Interventie"):
        cautareComboInterventie.destroy()
        cautareInterventie.destroy()
        
        searchFrameInterventie = tk.LabelFrame(base, text="Cautare dupa ora")
        searchFrameInterventie.pack(padx=10, pady=10)

        searchEntryInterventie = tk.Entry(searchFrameInterventie, font=("Helvetica"))
        searchEntryInterventie.pack(pady=20, padx=20)

        searchButtonInterventie = tk.Button(base, text="Cautare",command=cautareInterventieDupaOra)
        searchButtonInterventie.pack(padx=20, pady=20)

    elif(cautareComboInterventie.get() == "Tip Interventie"):
        cautareComboInterventie.destroy()
        cautareInterventie.destroy()

        searchFrameInterventie = tk.LabelFrame(base, text="Cautare dupa tip")
        searchFrameInterventie.pack(padx=10, pady=10)

        searchEntryInterventie = tk.Entry(searchFrameInterventie, font=("Helvetica"))
        searchEntryInterventie.pack(pady=20, padx=20)

        searchButtonInterventie = tk.Button(base, text="Cautare",command=cautareInterventieDupaTip)
        searchButtonInterventie.pack(padx=20, pady=20)
    else:
        messagebox.showwarning("WARNING", "Trebuie sa selectati un criteriu de cautare!")


def cautareInterventieDupaData():
    lookupRecordInterventie = searchEntryInterventie.get()

    searchFrameInterventie.destroy()
    searchButtonInterventie.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select Data, Ora, Tip from Interventie where Data = ?;",
        (lookupRecordInterventie)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Data interventie")
    tv.heading(2,text="Ora interventie")
    tv.heading(3,text="Tip interventie")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2]))  

def cautareInterventieDupaOra():
    lookupRecordInterventie = searchEntryInterventie.get()

    searchFrameInterventie.destroy()
    searchButtonInterventie.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select Data, Ora, Tip from Interventie where Ora = ?;",
        (lookupRecordInterventie)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Data interventie")
    tv.heading(2,text="Ora interventie")
    tv.heading(3,text="Tip interventie")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2]))

def cautareInterventieDupaTip():
    lookupRecordInterventie = searchEntryInterventie.get()

    searchFrameInterventie.destroy()
    searchButtonInterventie.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select Data, Ora, Tip from Interventie where Tip = ?;",
        (lookupRecordInterventie)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Data interventie")
    tv.heading(2,text="Ora interventie")
    tv.heading(3,text="Tip interventie")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2]))      
#----------------------------------------------------------------------------------------------

def vizLocatie():
    for widget in base.winfo_children():
        widget.destroy()
         
    base.title('Locatii') 
    base.config(bg= "#D3F0EF")

    global cautareComboLocatie, cautareLocatie

    cursor = conexiune.cursor()
    cursor.execute(
        "select LongitudineOra, LongitudineMinute, LongitudineSecunde, LatitudineOra, LatitudineMinute, LatitudineSecunde from Locatie"
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4','5','6'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Longitudine Ora")
    tv.heading(2,text="Longitudine Minute")
    tv.heading(3,text="Longitudine Secunde")
    tv.heading(4,text="Latitudine Ora")
    tv.heading(5,text="Latitudine Minute")
    tv.heading(6,text="Latitudine Secunde")

    vizualizareApeluri = tk.Button(base, text="Vizualizare Apeluri", width=23, height=3, fg='white',bg='black',command=vizApel)
    vizualizareApeluri.pack()
    vizualizareApeluri.place(relx=0.27, rely=0.8,anchor='center')

    vizualizareLocatii = tk.Button(base, text="Refresh", width=23, height=3, fg='white',bg='green',command=vizLocatie)
    vizualizareLocatii.pack()
    vizualizareLocatii.place(relx=0.42, rely=0.8,anchor='center')

    vizualizareInterventii = tk.Button(base, text="Vizualizare Interventii", width=23, height=3, fg='white',bg='black',command=vizInterventie)
    vizualizareInterventii.pack()
    vizualizareInterventii.place(relx=0.57, rely=0.8,anchor='center')

    vizualizareServicii = tk.Button(base, text="Vizualizare Servicii", width=23, height=3, fg='white',bg='black',command=vizServicii)
    vizualizareServicii.pack()
    vizualizareServicii.place(relx=0.72, rely=0.8,anchor='center')

    cautareComboLocatie = ttk.Combobox(base, width=15)
    cautareComboLocatie.pack()
    cautareComboLocatie['values']=("Longitudine Ora", "Longitudine Minute", "Longitudine Secunde", "Latitudine Ora", "Latitudine Minute", "Latitudine Secunde")
    cautareComboLocatie.place(relx=0.53, rely=0.5,anchor='center')
    
    cautareLocatie = tk.Button(base, text="Cautare", width=23, height=3, fg='white',bg='black',command=cautareLocatieBazaDeDate)
    cautareLocatie.pack()
    cautareLocatie.place(relx=0.42, rely=0.5,anchor='center')

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.5, rely = 0.7,anchor='center')

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3], i[4], i[5]))  


def cautareLocatieBazaDeDate():
    global searchEntryLocatie, searchFrameLocatie, searchButtonLocatie
    
    if(cautareComboLocatie.get() == "Longitudine Ora"):
        cautareComboLocatie.destroy()
        cautareLocatie.destroy()

        searchFrameLocatie = tk.LabelFrame(base, text="Cautare dupa longitudine ora")
        searchFrameLocatie.pack(padx=10, pady=10)

        searchEntryLocatie = tk.Entry(searchFrameLocatie, font=("Helvetica"))
        searchEntryLocatie.pack(pady=20, padx=20)

        searchButtonLocatie = tk.Button(base, text="Cautare",command=cautareLocatieDupaLongOra)
        searchButtonLocatie.pack(padx=20, pady=20)

    elif(cautareComboLocatie.get() == "Longitudine Minute"):
        cautareComboLocatie.destroy()
        cautareLocatie.destroy()
        
        searchFrameLocatie = tk.LabelFrame(base, text="Cautare dupa longitudine minute")
        searchFrameLocatie.pack(padx=10, pady=10)

        searchEntryLocatie = tk.Entry(searchFrameLocatie, font=("Helvetica"))
        searchEntryLocatie.pack(pady=20, padx=20)

        searchButtonLocatie = tk.Button(base, text="Cautare",command=cautareLocatieDupaLongMin)
        searchButtonLocatie.pack(padx=20, pady=20)

    elif(cautareComboLocatie.get() == "Longitudine Secunde"):
        cautareComboLocatie.destroy()
        cautareLocatie.destroy()

        searchFrameLocatie = tk.LabelFrame(base, text="Cautare dupa longitudine secunde")
        searchFrameLocatie.pack(padx=10, pady=10)

        searchEntryLocatie = tk.Entry(searchFrameLocatie, font=("Helvetica"))
        searchEntryLocatie.pack(pady=20, padx=20)

        searchButtonLocatie = tk.Button(base, text="Cautare",command=cautareLocatieDupaLongSec)
        searchButtonLocatie.pack(padx=20, pady=20)

    elif(cautareComboLocatie.get() == "Latitudine Ora"):
        cautareComboLocatie.destroy()
        cautareLocatie.destroy()

        searchFrameLocatie = tk.LabelFrame(base, text="Cautare dupa latitudine ora")
        searchFrameLocatie.pack(padx=10, pady=10)

        searchEntryLocatie = tk.Entry(searchFrameLocatie, font=("Helvetica"))
        searchEntryLocatie.pack(pady=20, padx=20)

        searchButtonLocatie = tk.Button(base, text="Cautare",command=cautareLocatieDupaLatOra)
        searchButtonLocatie.pack(padx=20, pady=20)

    elif(cautareComboLocatie.get() == "Latitudine Minute"):
        cautareComboLocatie.destroy()
        cautareLocatie.destroy()

        searchFrameLocatie = tk.LabelFrame(base, text="Cautare dupa latitudine minute")
        searchFrameLocatie.pack(padx=10, pady=10)

        searchEntryLocatie = tk.Entry(searchFrameLocatie, font=("Helvetica"))
        searchEntryLocatie.pack(pady=20, padx=20)

        searchButtonLocatie = tk.Button(base, text="Cautare",command=cautareLocatieDupaLatMin)
        searchButtonLocatie.pack(padx=20, pady=20)

    elif(cautareComboLocatie.get() == "Latitudine Secunde"):
        cautareComboLocatie.destroy()
        cautareLocatie.destroy()

        searchFrameLocatie = tk.LabelFrame(base, text="Cautare dupa latitudine secunde")
        searchFrameLocatie.pack(padx=10, pady=10)

        searchEntryLocatie = tk.Entry(searchFrameLocatie, font=("Helvetica"))
        searchEntryLocatie.pack(pady=20, padx=20)

        searchButtonLocatie = tk.Button(base, text="Cautare",command=cautareLocatieDupaLatSec)
        searchButtonLocatie.pack(padx=20, pady=20)
    else:
        messagebox.showwarning("WARNING", "Trebuie sa selectati un criteriu de cautare!")

def cautareLocatieDupaLongOra():
    lookupRecordLocatie = searchEntryLocatie.get()

    searchFrameLocatie.destroy()
    searchButtonLocatie.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select LongitudineOra, LongitudineMinute, LongitudineSecunde, LatitudineOra, LatitudineMinute, LatitudineSecunde from Locatie where LongitudineOra = ?;",
        (lookupRecordLocatie)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4','5','6'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Longitudine Ora")
    tv.heading(2,text="Longitudine Minute")
    tv.heading(3,text="Longitudine Secunde")
    tv.heading(4,text="Latitudine Ora")
    tv.heading(5,text="Latitudine Minute")
    tv.heading(6,text="Latitudine Secunde")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3], i[4], i[5])) 

def cautareLocatieDupaLongMin():
    lookupRecordLocatie = searchEntryLocatie.get()

    searchFrameLocatie.destroy()
    searchButtonLocatie.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select LongitudineOra, LongitudineMinute, LongitudineSecunde, LatitudineOra, LatitudineMinute, LatitudineSecunde from Locatie where LongitudineMinute = ?;",
        (lookupRecordLocatie)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4','5','6'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Longitudine Ora")
    tv.heading(2,text="Longitudine Minute")
    tv.heading(3,text="Longitudine Secunde")
    tv.heading(4,text="Latitudine Ora")
    tv.heading(5,text="Latitudine Minute")
    tv.heading(6,text="Latitudine Secunde")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3], i[4], i[5])) 

def cautareLocatieDupaLongSec():
    lookupRecordLocatie = searchEntryLocatie.get()

    searchFrameLocatie.destroy()
    searchButtonLocatie.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select LongitudineOra, LongitudineMinute, LongitudineSecunde, LatitudineOra, LatitudineMinute, LatitudineSecunde from Locatie where LongitudineSecunde = ?;",
        (lookupRecordLocatie)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4','5','6'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Longitudine Ora")
    tv.heading(2,text="Longitudine Minute")
    tv.heading(3,text="Longitudine Secunde")
    tv.heading(4,text="Latitudine Ora")
    tv.heading(5,text="Latitudine Minute")
    tv.heading(6,text="Latitudine Secunde")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3], i[4], i[5])) 

def cautareLocatieDupaLatOra():
    lookupRecordLocatie = searchEntryLocatie.get()

    searchFrameLocatie.destroy()
    searchButtonLocatie.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select LongitudineOra, LongitudineMinute, LongitudineSecunde, LatitudineOra, LatitudineMinute, LatitudineSecunde from Locatie where LatitudineOra = ?;",
        (lookupRecordLocatie)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4','5','6'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Longitudine Ora")
    tv.heading(2,text="Longitudine Minute")
    tv.heading(3,text="Longitudine Secunde")
    tv.heading(4,text="Latitudine Ora")
    tv.heading(5,text="Latitudine Minute")
    tv.heading(6,text="Latitudine Secunde")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3], i[4], i[5])) 

def cautareLocatieDupaLatMin():
    lookupRecordLocatie = searchEntryLocatie.get()

    searchFrameLocatie.destroy()
    searchButtonLocatie.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select LongitudineOra, LongitudineMinute, LongitudineSecunde, LatitudineOra, LatitudineMinute, LatitudineSecunde from Locatie where LatitudineMinute = ?;",
        (lookupRecordLocatie)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4','5','6'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Longitudine Ora")
    tv.heading(2,text="Longitudine Minute")
    tv.heading(3,text="Longitudine Secunde")
    tv.heading(4,text="Latitudine Ora")
    tv.heading(5,text="Latitudine Minute")
    tv.heading(6,text="Latitudine Secunde")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3], i[4], i[5])) 

def cautareLocatieDupaLatSec():
    lookupRecordLocatie = searchEntryLocatie.get()

    searchFrameLocatie.destroy()
    searchButtonLocatie.destroy()

    cursor = conexiune.cursor()
    cursor.execute(
        "select LongitudineOra, LongitudineMinute, LongitudineSecunde, LatitudineOra, LatitudineMinute, LatitudineSecunde from Locatie where LatitudineSecunde = ?;",
        (lookupRecordLocatie)
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=20)

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4','5','6'), show='headings', height=5, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Longitudine Ora")
    tv.heading(2,text="Longitudine Minute")
    tv.heading(3,text="Longitudine Secunde")
    tv.heading(4,text="Latitudine Ora")
    tv.heading(5,text="Latitudine Minute")
    tv.heading(6,text="Latitudine Secunde")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3], i[4], i[5])) 
#----------------------------------------------------------------------------------------------

# UPDATE APEL

def modificaApel():
    for widget in base.winfo_children():
        widget.destroy()

    global durataApelVeche, durataApelNoua, numeApelantVechi, numeApelantNou, prenumeApelantVechi, prenumeApelantNou, numarDeTelefonVechi, numarDeTelefonNou


    label1 = tk.Label(base, text="VALORI VECHI", font=("Times", 16), bg = "#D3F0EF")
    label1.pack()
    label1.place(anchor='center',relx=0.3,rely=0.3)

    label2 = tk.Label(base, text="VALORI NOI",font=("Times", 16), bg = "#D3F0EF")
    label2.pack()
    label2.place(anchor='center',relx=0.75,rely=0.3)

    label3 = tk.Label(base, text="Durata apel", bg = "#D3F0EF")
    label3.pack()
    label3.place(anchor='center',relx=0.2,rely=0.4)

    durataApelVeche = tk.Entry(base, width=30)
    durataApelVeche.pack()
    durataApelVeche.place(anchor='center',relx=0.3, rely = 0.4)

    label4 = tk.Label(base, text="Nume apelant", bg = "#D3F0EF")
    label4.pack()
    label4.place(anchor='center',relx=0.2,rely=0.5)

    numeApelantVechi = tk.Entry(base, width=30)
    numeApelantVechi.pack()
    numeApelantVechi.place(anchor='center',relx=0.3, rely = 0.5)

    label5 = tk.Label(base, text="Prenume apelant", bg = "#D3F0EF")
    label5.pack()
    label5.place(anchor='center',relx=0.2,rely=0.6)

    prenumeApelantVechi = tk.Entry(base, width=30)
    prenumeApelantVechi.pack()
    prenumeApelantVechi.place(anchor='center',relx=0.3, rely = 0.6)

    label6 = tk.Label(base, text="Numar de telefon", bg = "#D3F0EF")
    label6.pack()
    label6.place(anchor='center',relx=0.2,rely=0.7)

    numarDeTelefonVechi = tk.Entry(base, width=30)
    numarDeTelefonVechi.pack()
    numarDeTelefonVechi.place(anchor='center',relx=0.3, rely = 0.7)

    label7 = tk.Label(base, text="Durata apel", bg = "#D3F0EF")
    label7.pack()
    label7.place(anchor='center',relx=0.65,rely=0.4)

    durataApelNoua = tk.Entry(base, width=30)
    durataApelNoua.pack()
    durataApelNoua.place(anchor='center',relx=0.75, rely = 0.4)

    label8 = tk.Label(base, text="Nume apelant", bg = "#D3F0EF")
    label8.pack()
    label8.place(anchor='center',relx=0.65,rely=0.5)

    numeApelantNou = tk.Entry(base, width=30)
    numeApelantNou.pack()
    numeApelantNou.place(anchor='center',relx=0.75, rely = 0.5)

    label9 = tk.Label(base, text="Prenume apelant", bg = "#D3F0EF")
    label9.pack()
    label9.place(anchor='center',relx=0.65,rely=0.6)

    prenumeApelantNou = tk.Entry(base, width=30)
    prenumeApelantNou.pack()
    prenumeApelantNou.place(anchor='center',relx=0.75, rely = 0.6)

    label10 = tk.Label(base, text="Numar de telefon", bg = "#D3F0EF")
    label10.pack()
    label10.place(anchor='center',relx=0.65,rely=0.7)

    numarDeTelefonNou = tk.Entry(base, width=30)
    numarDeTelefonNou.pack()
    numarDeTelefonNou.place(anchor='center',relx=0.75, rely = 0.7)

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.6, rely = 0.83,anchor='center')

    submitButton = tk.Button(base, text = "MODIFICA BAZA DE DATE", width=30,height=3,bg='brown',fg='white',command=modificaApelBazaDeDate)
    submitButton.pack()
    submitButton.place(anchor='center',relx=0.4,rely=0.83)
 

def modificaApelBazaDeDate(): 
    ok = tk.BooleanVar()

    var1 = durataApelNoua.get()
    var2 = numeApelantNou.get()
    var3 = prenumeApelantNou.get()
    var4 = numarDeTelefonNou.get()

    var5 = durataApelVeche.get()
    var6 = numeApelantVechi.get()
    var7 = prenumeApelantVechi.get()
    var8 = numarDeTelefonVechi.get()

    
    cursor = conexiune.cursor()
    cursor.execute(
        "select DurataApel, NumeApelant, PrenumeApelant, NumarDeTelefon from Apel",
    )
    variabileApel = cursor.fetchall()
    conexiune.commit()   
    

    for i in range(11):
        if(durataApelVeche.get() == variabileApel[i][0].strip()):
            if(numeApelantVechi.get() == ""):
                var6 = variabileApel[i][1]
            if(numeApelantVechi.get() != variabileApel[i][1].strip() and numeApelantVechi.get() != ""):
                ok = False
                break
            if(prenumeApelantVechi.get() == ""):
                var7 = variabileApel[i][2]
            if(prenumeApelantVechi.get() != variabileApel[i][2].strip() and prenumeApelantVechi.get() != ""):
                ok = False
                break
            if(numarDeTelefonVechi.get() == ""):
                var8 = variabileApel[i][3]
            if(numarDeTelefonVechi.get() != variabileApel[i][3].strip() and numarDeTelefonVechi.get() != ""):
                ok = False
                break

        if(durataApelNoua.get() == ""):
            var1 = var5
        if(numeApelantNou.get() == ""):
            var2 = var6
        if(prenumeApelantNou.get() == ""): 
            var3 = var7
        if(numarDeTelefonNou.get() == ""):
            var4 = var8  
        cursor = conexiune.cursor()
        cursor.execute(
        "update Apel SET DurataApel = ?, NumeApelant = ?, PrenumeApelant = ?, NumarDeTelefon = ? WHERE DurataApel = ? AND NumeApelant = ? AND PrenumeApelant = ? AND NumarDeTelefon = ?;",
            (var1, var2, var3, var4, var5, var6, var7, var8)
        )
        conexiune.commit()

    for i in range(11):
        if(numeApelantVechi.get() == variabileApel[i][1].strip()):
            if(durataApelVeche.get() == ""):
                var5 = variabileApel[i][0]
            if(durataApelVeche.get() != variabileApel[i][0].strip() and durataApelVeche.get() != ""):
                ok = False
                break
            if(prenumeApelantVechi.get() == ""):
                var7 = variabileApel[i][2]
            if(prenumeApelantVechi.get() != variabileApel[i][2].strip() and prenumeApelantVechi.get() != ""):
                ok = False
                break
            if(numarDeTelefonVechi.get() == ""):
                var8 = variabileApel[i][3]
            if(numarDeTelefonVechi.get() != variabileApel[i][3].strip() and numarDeTelefonVechi.get() != ""):
                ok = False
                break

        if(durataApelNoua.get() == ""):
            var1 = var5
        if(numeApelantNou.get() == ""):
            var2 = var6
        if(prenumeApelantNou.get() == ""): 
            var3 = var7
        if(numarDeTelefonNou.get() == ""):
            var4 = var8  
        cursor = conexiune.cursor()
        cursor.execute(
        "update Apel SET DurataApel = ?, NumeApelant = ?, PrenumeApelant = ?, NumarDeTelefon = ? WHERE DurataApel = ? AND NumeApelant = ? AND PrenumeApelant = ? AND NumarDeTelefon = ?;",
            (var1, var2, var3, var4, var5, var6, var7, var8)
        )
        conexiune.commit()
 
    for i in range(10):
        if(prenumeApelantVechi.get() == variabileApel[i][2].strip()):
            if(durataApelVeche.get() == ""):
                var5 = variabileApel[i][0]
            if(durataApelVeche.get() != variabileApel[i][0].strip() and durataApelVeche.get() != ""):
                ok = False
                break
            if(numeApelantVechi.get() == ""):
                var6 = variabileApel[i][1]
            if(numeApelantVechi.get() != variabileApel[i][1].strip() and numeApelantVechi.get() != ""):
                ok = False
                break
            if(numarDeTelefonVechi.get() == ""):
                var8 = variabileApel[i][3]
            if(numarDeTelefonVechi.get() != variabileApel[i][3].strip() and numarDeTelefonVechi.get() != ""):
                ok = False
                break

        if(durataApelNoua.get() == ""):
            var1 = var5
        if(numeApelantNou.get() == ""):
            var2 = var6
        if(prenumeApelantNou.get() == ""): 
            var3 = var7
        if(numarDeTelefonNou.get() == ""):
            var4 = var8  
        cursor = conexiune.cursor()
        cursor.execute(
        "update Apel SET DurataApel = ?, NumeApelant = ?, PrenumeApelant = ?, NumarDeTelefon = ? WHERE DurataApel = ? AND NumeApelant = ? AND PrenumeApelant = ? AND NumarDeTelefon = ?;",
            (var1, var2, var3, var4, var5, var6, var7, var8)
        )
        conexiune.commit()

    for i in range(10):
        if(numarDeTelefonVechi.get() == variabileApel[i][3].strip()):
            if(durataApelVeche.get() == ""):
                var5 = variabileApel[i][0]
            if(durataApelVeche.get() != variabileApel[i][0].strip() and durataApelVeche.get() != ""):
                ok = False
                break
            if(numeApelantVechi.get() == ""):
                var6 = variabileApel[i][1]
            if(numeApelantVechi.get() != variabileApel[i][1].strip() and numeApelantVechi.get() != ""):
                ok = False
                break
            if(prenumeApelantVechi.get() == ""):
                var7 = variabileApel[i][2]
            if(prenumeApelantVechi.get() != variabileApel[i][2].strip() and prenumeApelantVechi.get()):
                ok = False 
                break
        
        if(durataApelNoua.get() == ""):
            var1 = var5
        if(numeApelantNou.get() == ""):
            var2 = var6
        if(prenumeApelantNou.get() == ""): 
            var3 = var7
        if(numarDeTelefonNou.get() == ""):
            var4 = var8  
        cursor = conexiune.cursor()
        cursor.execute(
        "update Apel SET DurataApel = ?, NumeApelant = ?, PrenumeApelant = ?, NumarDeTelefon = ? WHERE DurataApel = ? AND NumeApelant = ? AND PrenumeApelant = ? AND NumarDeTelefon = ?;",
            (var1, var2, var3, var4, var5, var6, var7, var8)
        )
        conexiune.commit() 

    if(ok == False):
        messagebox.showerror("ERROR", "DATE INCORECTE INTRODUSE!")
    else:
        messagebox.showinfo("SUCCES", "Apel modificat cu succes!")
    for widget in base.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0,'end')

#---------------------------------------------------------------------------------------------

# UPDATE LOCATIE

def modificaLocatie():
    for widget in base.winfo_children():
        widget.destroy()

    global longitudineOraVeche, longitudineOraNoua, longitudineMinuteVeche, longitudineMinuteNoua, longitudineSecundeVeche, longitudineSecundeNoua
    global latitudineOraVeche, latitudineOraNoua, latitudineMinuteVeche, latitudineMinuteNoua, latitudineSecundeVeche, latitudineSecundeNoua

    label1 = tk.Label(base, text="VALORI VECHI", font=("Times", 16), bg = "#D3F0EF")
    label1.pack()
    label1.place(anchor='center',relx=0.3,rely=0.3)

    label2 = tk.Label(base, text="VALORI NOI",font=("Times", 16), bg = "#D3F0EF")
    label2.pack()
    label2.place(anchor='center',relx=0.75,rely=0.3)

    label3 = tk.Label(base, text="Longitudine Ora", bg = "#D3F0EF")
    label3.pack()
    label3.place(anchor='center',relx=0.2,rely=0.35)

    longitudineOraVeche = tk.Entry(base, width=30)
    longitudineOraVeche.pack()
    longitudineOraVeche.place(anchor='center',relx=0.3, rely = 0.35)

    label4 = tk.Label(base, text="Longitudine Minute", bg = "#D3F0EF")
    label4.pack()
    label4.place(anchor='center',relx=0.2,rely=0.4)

    longitudineMinuteVeche = tk.Entry(base, width=30)
    longitudineMinuteVeche.pack()
    longitudineMinuteVeche.place(anchor='center',relx=0.3, rely = 0.4)

    label5 = tk.Label(base, text="Longitudine Secunde", bg = "#D3F0EF")
    label5.pack()
    label5.place(anchor='center',relx=0.2,rely=0.45)

    longitudineSecundeVeche = tk.Entry(base, width=30)
    longitudineSecundeVeche.pack()
    longitudineSecundeVeche.place(anchor='center',relx=0.3, rely = 0.45)

    label6 = tk.Label(base, text="Latitudine Ora", bg = "#D3F0EF")
    label6.pack()
    label6.place(anchor='center',relx=0.2,rely=0.5)

    latitudineOraVeche = tk.Entry(base, width=30)
    latitudineOraVeche.pack()
    latitudineOraVeche.place(anchor='center',relx=0.3, rely = 0.5)

    label7 = tk.Label(base, text="Latitudine Minute", bg = "#D3F0EF")
    label7.pack()
    label7.place(anchor='center',relx=0.2,rely=0.55)

    latitudineMinuteVeche = tk.Entry(base, width=30)
    latitudineMinuteVeche.pack()
    latitudineMinuteVeche.place(anchor='center',relx=0.3, rely = 0.55)

    label8 = tk.Label(base, text="Latitudine Secunde", bg = "#D3F0EF")
    label8.pack()
    label8.place(anchor='center',relx=0.2,rely=0.6)

    latitudineSecundeVeche = tk.Entry(base, width=30)
    latitudineSecundeVeche.pack()
    latitudineSecundeVeche.place(anchor='center',relx=0.3, rely = 0.6)

    label9 = tk.Label(base, text="Longitudine Ora", bg = "#D3F0EF")
    label9.pack()
    label9.place(anchor='center',relx=0.65,rely=0.35)

    longitudineOraNoua = tk.Entry(base, width=30)
    longitudineOraNoua.pack()
    longitudineOraNoua.place(anchor='center',relx=0.75, rely = 0.35)

    label10 = tk.Label(base, text="Longitudine Minute", bg = "#D3F0EF")
    label10.pack()
    label10.place(anchor='center',relx=0.65,rely=0.4)

    longitudineMinuteNoua = tk.Entry(base, width=30)
    longitudineMinuteNoua.pack()
    longitudineMinuteNoua.place(anchor='center',relx=0.75, rely = 0.4)

    label10 = tk.Label(base, text="Longitudine Secunde", bg = "#D3F0EF")
    label10.pack()
    label10.place(anchor='center',relx=0.65,rely=0.45)

    longitudineSecundeNoua = tk.Entry(base, width=30)
    longitudineSecundeNoua.pack()
    longitudineSecundeNoua.place(anchor='center',relx=0.75, rely = 0.45)

    label11 = tk.Label(base, text="Latitudine Ora", bg = "#D3F0EF")
    label11.pack()
    label11.place(anchor='center',relx=0.65,rely=0.5)

    latitudineOraNoua = tk.Entry(base, width=30)
    latitudineOraNoua.pack()
    latitudineOraNoua.place(anchor='center',relx=0.75, rely = 0.5)

    label12 = tk.Label(base, text="Latitudine Minute", bg = "#D3F0EF")
    label12.pack()
    label12.place(anchor='center',relx=0.65,rely=0.55)

    latitudineMinuteNoua = tk.Entry(base, width=30)
    latitudineMinuteNoua.pack()
    latitudineMinuteNoua.place(anchor='center',relx=0.75, rely = 0.55)

    label13 = tk.Label(base, text="Latitudine Secunde", bg = "#D3F0EF")
    label13.pack()
    label13.place(anchor='center',relx=0.65,rely=0.6)

    latitudineSecundeNoua = tk.Entry(base, width=30)
    latitudineSecundeNoua.pack()
    latitudineSecundeNoua.place(anchor='center',relx=0.75, rely = 0.6)

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.6, rely = 0.83,anchor='center')

    submitButton = tk.Button(base, text = "MODIFICA BAZA DE DATE", width=30,height=3,bg='brown',fg='white',command=modificareLocatieBazaDeDate)
    submitButton.pack()
    submitButton.place(anchor='center',relx=0.4,rely=0.83)

def modificareLocatieBazaDeDate():
    conexiune.commit() 

    ok = tk.BooleanVar()

    var1 = longitudineOraNoua.get()
    var2 = longitudineMinuteNoua.get()
    var3 = longitudineSecundeNoua.get()
    var4 = latitudineOraNoua.get()
    var5 = latitudineMinuteNoua.get()
    var6 = latitudineSecundeNoua.get()

    var7 = longitudineOraVeche.get()
    var8 = longitudineMinuteVeche.get()
    var9 = longitudineSecundeVeche.get()
    var10 = latitudineOraVeche.get()
    var11 = latitudineMinuteVeche.get()
    var12 = latitudineSecundeVeche.get()

    
    cursor = conexiune.cursor()
    cursor.execute(
        "select LongitudineOra, LongitudineMinute, LongitudineSecunde, LatitudineOra, LatitudineMinute, LatitudineSecunde from Locatie",
    )
    variabileLocatie = cursor.fetchall()
    conexiune.commit()   

    for i in range(10):
        if(longitudineOraVeche.get() == str(variabileLocatie[i][0])):
            if(longitudineMinuteVeche.get() == ""):
                var8 = variabileLocatie[i][1]
            if(longitudineMinuteVeche.get() != str(variabileLocatie[i][1]) and longitudineMinuteVeche.get() != ""):
                ok = False
                break
            if(longitudineSecundeVeche.get() == ""):
                var9 = variabileLocatie[i][2]
            if(longitudineSecundeVeche.get() != str(variabileLocatie[i][2]) and longitudineSecundeVeche.get() != ""):
                ok = False
                break
            if(latitudineOraVeche.get() == ""):
                var10 = variabileLocatie[i][3]
            if(latitudineOraVeche.get() != str(variabileLocatie[i][3]) and latitudineOraVeche.get() != ""):
                ok = False
                break
            if(latitudineMinuteVeche.get() == ""):
                var11 = variabileLocatie[i][4]
            if(latitudineMinuteVeche.get() != str(variabileLocatie[i][4]) and latitudineMinuteVeche.get() != ""):
                ok = False
                break
            if(latitudineSecundeVeche.get() == ""):
                var12 = variabileLocatie[i][5]
            if(latitudineSecundeVeche.get() != str(variabileLocatie[i][5]) and latitudineSecundeVeche.get() != ""):
                ok = False
                break

        if(longitudineOraNoua.get() == ""):
            var1 = var7
        if(longitudineMinuteNoua.get() == ""):
            var2 = var8
        if(longitudineSecundeNoua.get() == ""): 
            var3 = var9
        if(latitudineOraNoua.get() == ""):
            var4 = var10  
        if(latitudineMinuteNoua.get() == ""): 
            var5 = var11
        if(latitudineSecundeNoua.get() == ""):
            var6 = var12

        cursor = conexiune.cursor()
        cursor.execute(
        "update Locatie SET LongitudineOra = ?, LongitudineMinute = ?, LongitudineSecunde = ?, LatitudineOra = ?, LatitudineMinute = ?, LatitudineSecunde = ? WHERE LongitudineOra = ? AND LongitudineMinute = ? AND LongitudineSecunde = ? AND LatitudineOra = ? AND LatitudineMinute = ? AND LatitudineSecunde = ?;",
            (var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12)
        )
        conexiune.commit()

        
    for i in range(10):
        if(longitudineMinuteVeche.get() == str(variabileLocatie[i][1])):
            if(longitudineOraVeche.get() == ""):
                var7 = variabileLocatie[i][0]
            if(longitudineOraVeche.get() != str(variabileLocatie[i][0]) and longitudineOraVeche.get() != ""):
                ok = False
                break
            if(longitudineSecundeVeche.get() == ""):
                var9 = variabileLocatie[i][2]
            if(longitudineSecundeVeche.get() != str(variabileLocatie[i][2]) and longitudineSecundeVeche.get() != ""):
                ok = False
                break
            if(latitudineOraVeche.get() == ""):
                var10 = variabileLocatie[i][3]
            if(latitudineOraVeche.get() != str(variabileLocatie[i][3]) and latitudineOraVeche.get() != ""):
                ok = False
                break
            if(latitudineMinuteVeche.get() == ""):
                var11 = variabileLocatie[i][4]
            if(latitudineMinuteVeche.get() != str(variabileLocatie[i][4]) and latitudineMinuteVeche.get() != ""):
                ok = False
                break
            if(latitudineSecundeVeche.get() == ""):
                var12 = variabileLocatie[i][5]
            if(latitudineSecundeVeche.get() != str(variabileLocatie[i][5]) and latitudineSecundeVeche.get() != ""):
                ok = False
                break

        if(longitudineOraNoua.get() == ""):
            var1 = var7
        if(longitudineMinuteNoua.get() == ""):
            var2 = var8
        if(longitudineSecundeNoua.get() == ""): 
            var3 = var9
        if(latitudineOraNoua.get() == ""):
            var4 = var10  
        if(latitudineMinuteNoua.get() == ""): 
            var5 = var11
        if(latitudineSecundeNoua.get() == ""):
            var6 = var12

        cursor = conexiune.cursor()
        cursor.execute(
        "update Locatie SET LongitudineOra = ?, LongitudineMinute = ?, LongitudineSecunde = ?, LatitudineOra = ?, LatitudineMinute = ?, LatitudineSecunde = ? WHERE LongitudineOra = ? AND LongitudineMinute = ? AND LongitudineSecunde = ? AND LatitudineOra = ? AND LatitudineMinute = ? AND LatitudineSecunde = ?;",
            (var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12)
        )
        conexiune.commit()

        
    for i in range(10):
        if(longitudineSecundeVeche.get() == str(variabileLocatie[i][2])):
            if(longitudineOraVeche.get() == ""):
                var7 = variabileLocatie[i][0]
            if(longitudineOraVeche.get() != str(variabileLocatie[i][0]) and longitudineOraVeche.get() != ""):
                ok = False
                break
            if(longitudineMinuteVeche.get() == ""):
                var8 = variabileLocatie[i][1]
            if(longitudineMinuteVeche.get() != str(variabileLocatie[i][1]) and longitudineMinuteVeche.get() != ""):
                ok = False
                break
            if(latitudineOraVeche.get() == ""):
                var10 = variabileLocatie[i][3]
            if(latitudineOraVeche.get() != str(variabileLocatie[i][3]) and latitudineOraVeche.get() != ""):
                ok = False
                break
            if(latitudineMinuteVeche.get() == ""):
                var11 = variabileLocatie[i][4]
            if(latitudineMinuteVeche.get() != str(variabileLocatie[i][4]) and latitudineMinuteVeche.get() != ""):
                ok = False
                break
            if(latitudineSecundeVeche.get() == ""):
                var12 = variabileLocatie[i][5]
            if(latitudineSecundeVeche.get() != str(variabileLocatie[i][5]) and latitudineSecundeVeche.get() != ""):
                ok = False
                break

        if(longitudineOraNoua.get() == ""):
            var1 = var7
        if(longitudineMinuteNoua.get() == ""):
            var2 = var8
        if(longitudineSecundeNoua.get() == ""): 
            var3 = var9
        if(latitudineOraNoua.get() == ""):
            var4 = var10  
        if(latitudineMinuteNoua.get() == ""): 
            var5 = var11
        if(latitudineSecundeNoua.get() == ""):
            var6 = var12

        cursor = conexiune.cursor()
        cursor.execute(
        "update Locatie SET LongitudineOra = ?, LongitudineMinute = ?, LongitudineSecunde = ?, LatitudineOra = ?, LatitudineMinute = ?, LatitudineSecunde = ? WHERE LongitudineOra = ? AND LongitudineMinute = ? AND LongitudineSecunde = ? AND LatitudineOra = ? AND LatitudineMinute = ? AND LatitudineSecunde = ?;",
            (var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12)
        )
        conexiune.commit()

        
    for i in range(10):
        if(latitudineOraVeche.get() == str(variabileLocatie[i][3])):
   
            if(longitudineOraVeche.get() == ""):
                var7 = variabileLocatie[i][0]
            if(longitudineOraVeche.get() != str(variabileLocatie[i][0]) and longitudineOraVeche.get() != ""):
                ok = False
                break
            if(longitudineMinuteVeche.get() == ""):
                var8 = variabileLocatie[i][1]
            if(longitudineMinuteVeche.get() != str(variabileLocatie[i][1]) and longitudineMinuteVeche.get() != ""):
                ok = False
                break
            if(longitudineSecundeVeche.get() == ""):
                var9 = variabileLocatie[i][2]
            if(longitudineSecundeVeche.get() != str(variabileLocatie[i][2]) and longitudineSecundeVeche.get() != ""):
                ok = False
                break
            if(latitudineMinuteVeche.get() == ""):
                var11 = variabileLocatie[i][4]
            if(latitudineMinuteVeche.get() != str(variabileLocatie[i][4]) and latitudineMinuteVeche.get() != ""):
                ok = False
                break
            if(latitudineSecundeVeche.get() == ""):
                var12 = variabileLocatie[i][5]
            if(latitudineSecundeVeche.get() != str(variabileLocatie[i][5]) and latitudineSecundeVeche.get() != ""):
                ok = False
                break

        if(longitudineOraNoua.get() == ""):
            var1 = var7
        if(longitudineMinuteNoua.get() == ""):
            var2 = var8
        if(longitudineSecundeNoua.get() == ""): 
            var3 = var9
        if(latitudineOraNoua.get() == ""):
            var4 = var10  
        if(latitudineMinuteNoua.get() == ""): 
            var5 = var11
        if(latitudineSecundeNoua.get() == ""):
            var6 = var12

        cursor = conexiune.cursor()
        cursor.execute(
        "update Locatie SET LongitudineOra = ?, LongitudineMinute = ?, LongitudineSecunde = ?, LatitudineOra = ?, LatitudineMinute = ?, LatitudineSecunde = ? WHERE LongitudineOra = ? AND LongitudineMinute = ? AND LongitudineSecunde = ? AND LatitudineOra = ? AND LatitudineMinute = ? AND LatitudineSecunde = ?;",
            (var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12)
        )
        conexiune.commit()

        
    for i in range(10):
        if(latitudineMinuteVeche.get() == str(variabileLocatie[i][4])):
      
            if(longitudineOraVeche.get() == ""):
                var7 = variabileLocatie[i][0]
            if(longitudineOraVeche.get() != str(variabileLocatie[i][0]) and longitudineOraVeche.get() != ""):
                ok = False
                break
            if(longitudineMinuteVeche.get() == ""):
                var8 = variabileLocatie[i][1]
            if(longitudineMinuteVeche.get() != str(variabileLocatie[i][1]) and longitudineMinuteVeche.get() != ""):
                ok = False
                break
            if(longitudineSecundeVeche.get() == ""):
                var9 = variabileLocatie[i][2]
            if(longitudineSecundeVeche.get() != str(variabileLocatie[i][2]) and longitudineSecundeVeche.get() != ""):
                ok = False
                break
            if(latitudineOraVeche.get() == ""):
                var10 = variabileLocatie[i][3]
            if(latitudineOraVeche.get() != str(variabileLocatie[i][3]) and latitudineOraVeche.get() != ""):
                ok = False
                break
            if(latitudineSecundeVeche.get() == ""):
                var12 = variabileLocatie[i][5]
            if(latitudineSecundeVeche.get() != str(variabileLocatie[i][5])  and latitudineSecundeVeche.get() != ""):
                ok = False
                break

        if(longitudineOraNoua.get() == ""):
            var1 = var7
        if(longitudineMinuteNoua.get() == ""):
            var2 = var8
        if(longitudineSecundeNoua.get() == ""): 
            var3 = var9
        if(latitudineOraNoua.get() == ""):
            var4 = var10  
        if(latitudineMinuteNoua.get() == ""): 
            var5 = var11
        if(latitudineSecundeNoua.get() == ""):
            var6 = var12

        cursor = conexiune.cursor()
        cursor.execute(
        "update Locatie SET LongitudineOra = ?, LongitudineMinute = ?, LongitudineSecunde = ?, LatitudineOra = ?, LatitudineMinute = ?, LatitudineSecunde = ? WHERE LongitudineOra = ? AND LongitudineMinute = ? AND LongitudineSecunde = ? AND LatitudineOra = ? AND LatitudineMinute = ? AND LatitudineSecunde = ?;",
            (var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12)
        )
        conexiune.commit()

    for i in range(10):
        if(latitudineSecundeVeche.get() == str(variabileLocatie[i][5])):
      
            if(longitudineOraVeche.get() == ""):
                var7 = variabileLocatie[i][0]
            if(longitudineOraVeche.get() != str(variabileLocatie[i][0]) and longitudineOraVeche.get() != ""):
                ok = False
                break
            if(longitudineMinuteVeche.get() == ""):
                var8 = variabileLocatie[i][1]
            if(longitudineMinuteVeche.get() != str(variabileLocatie[i][1]) and longitudineMinuteVeche.get() != ""):
                ok = False
                break
            if(longitudineSecundeVeche.get() == ""):
                var9 = variabileLocatie[i][2]
            if(longitudineSecundeVeche.get() != str(variabileLocatie[i][2]) and longitudineSecundeVeche.get() != ""):
                ok = False
                break
            if(latitudineOraVeche.get() == ""):
                var10 = variabileLocatie[i][3]
            if(latitudineOraVeche.get() != str(variabileLocatie[i][3]) and latitudineOraVeche.get() != ""):
                ok = False
                break
            if(latitudineMinuteVeche.get() == ""):
                var11 = variabileLocatie[i][4]
            if(latitudineMinuteVeche.get() != variabileLocatie[i][4] and latitudineMinuteVeche.get() != ""):
                ok = False
                break

        if(longitudineOraNoua.get() == ""):
            var1 = var7
        if(longitudineMinuteNoua.get() == ""):
            var2 = var8
        if(longitudineSecundeNoua.get() == ""): 
            var3 = var9
        if(latitudineOraNoua.get() == ""):
            var4 = var10  
        if(latitudineMinuteNoua.get() == ""): 
            var5 = var11
        if(latitudineSecundeNoua.get() == ""):
            var6 = var12

        cursor = conexiune.cursor()
        cursor.execute(
        "update Locatie SET LongitudineOra = ?, LongitudineMinute = ?, LongitudineSecunde = ?, LatitudineOra = ?, LatitudineMinute = ?, LatitudineSecunde = ? WHERE LongitudineOra = ? AND LongitudineMinute = ? AND LongitudineSecunde = ? AND LatitudineOra = ? AND LatitudineMinute = ? AND LatitudineSecunde = ?;",
            (var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12)
        )
        conexiune.commit()
    
    if(ok == False):
        messagebox.showerror("ERROR", "DATE INCORECTE INTRODUSE!")
    else:
        messagebox.showinfo("SUCCES", "Locatie modificata cu succes!") 
    for widget in base.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0,'end')

#---------------------------------------------------------------------------------------------------------------------------

# UPDATE INTERVENTIE

def modificaInterventie():
    for widget in base.winfo_children():
        widget.destroy()

    global dataVeche, dataNoua, oraVeche, oraNoua, tipVechi, tipNou

    label1 = tk.Label(base, text="VALORI VECHI", font=("Times", 16), bg = "#D3F0EF")
    label1.pack()
    label1.place(anchor='center',relx=0.3,rely=0.3)

    label2 = tk.Label(base, text="VALORI NOI",font=("Times", 16), bg = "#D3F0EF")
    label2.pack()
    label2.place(anchor='center',relx=0.75,rely=0.3)

    label3 = tk.Label(base, text="Data", bg = "#D3F0EF")
    label3.pack()
    label3.place(anchor='center',relx=0.2,rely=0.4)

    dataVeche = tk.Entry(base, width=30)
    dataVeche.pack()
    dataVeche.place(anchor='center',relx=0.3, rely = 0.4)

    label4 = tk.Label(base, text="Ora", bg = "#D3F0EF")
    label4.pack()
    label4.place(anchor='center',relx=0.2,rely=0.5)

    oraVeche = tk.Entry(base, width=30)
    oraVeche.pack()
    oraVeche.place(anchor='center',relx=0.3, rely = 0.5)

    label5 = tk.Label(base, text="Tip", bg = "#D3F0EF")
    label5.pack()
    label5.place(anchor='center',relx=0.2,rely=0.6)

    tipVechi = tk.Entry(base, width=30)
    tipVechi.pack()
    tipVechi.place(anchor='center',relx=0.3, rely = 0.6)

    label6 = tk.Label(base, text="Data", bg = "#D3F0EF")
    label6.pack()
    label6.place(anchor='center',relx=0.65,rely=0.4)

    dataNoua = tk.Entry(base, width=30)
    dataNoua.pack()
    dataNoua.place(anchor='center',relx=0.75, rely = 0.4)

    label7 = tk.Label(base, text="Ora", bg = "#D3F0EF")
    label7.pack()
    label7.place(anchor='center',relx=0.65,rely=0.5)

    oraNoua = tk.Entry(base, width=30)
    oraNoua.pack()
    oraNoua.place(anchor='center',relx=0.75, rely = 0.5)

    label8 = tk.Label(base, text="Tip", bg = "#D3F0EF")
    label8.pack()
    label8.place(anchor='center',relx=0.65,rely=0.6)

    tipNou = tk.Entry(base, width=30)
    tipNou.pack()
    tipNou.place(anchor='center',relx=0.75, rely = 0.6)

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.6, rely = 0.83,anchor='center')

    submitButton = tk.Button(base, text = "MODIFICA BAZA DE DATE", width=30,height=3,bg='brown',fg='white',command=modificareInterventieBazaDeDate)
    submitButton.pack()
    submitButton.place(anchor='center',relx=0.4,rely=0.83)

def modificareInterventieBazaDeDate():
    
    ok = tk.BooleanVar()

    var1 = dataNoua.get()
    var2 = oraNoua.get()
    var3 = tipNou.get()

    var4 = dataVeche.get()
    var5 = oraVeche.get()
    var6 = tipVechi.get()
  
    cursor = conexiune.cursor()
    cursor.execute(
        "select Data, Ora, Tip from Interventie",
    )
    variabileInterventie = cursor.fetchall()
    conexiune.commit()  

    for i in range(9):
        if(dataVeche.get() == variabileInterventie[i][0].strip()):
            if(oraVeche.get() == ""):
                var5 = variabileInterventie[i][1]
            if(oraVeche.get() != variabileInterventie[i][1].strip() and oraVeche.get() != ""):
                ok = False
                break
            if(tipVechi.get() == ""):
                var6 = variabileInterventie[i][2]
            if(tipVechi.get() != variabileInterventie[i][2].strip() and tipVechi.get() != ""):
                ok = False
                break

        if(dataNoua.get() == ""):
            var1 = var4
        if(oraNoua.get() == ""):
            var2 = var5
        if(tipNou.get() == ""): 
            var3 = var6 

        cursor = conexiune.cursor()
        cursor.execute(
        "update Interventie SET Data = ?, Ora = ?, Tip = ? WHERE Data = ? AND Ora = ? AND Tip = ?;",
            (var1, var2, var3, var4, var5, var6)
        )
        conexiune.commit() 

    for i in range(9):
        if(oraVeche.get() == variabileInterventie[i][1].strip()):
            if(dataVeche.get() == ""):
                var4 = variabileInterventie[i][0]
            if(dataVeche.get() != variabileInterventie[i][0].strip() and dataVeche.get() != ""):
                ok = False
                break
            if(tipVechi.get() == ""):
                var6 = variabileInterventie[i][2]
            if(tipVechi.get() != variabileInterventie[i][2].strip() and tipVechi.get() != ""):
                ok = False
                break

        if(dataNoua.get() == ""):
            var1 = var4
        if(oraNoua.get() == ""):
            var2 = var5
        if(tipNou.get() == ""): 
            var3 = var6 

        cursor = conexiune.cursor()
        cursor.execute(
        "update Interventie SET Data = ?, Ora = ?, Tip = ? WHERE Data = ? AND Ora = ? AND Tip = ?;",
            (var1, var2, var3, var4, var5, var6)
        )
        conexiune.commit() 

    for i in range(9):
        if(tipVechi.get() == variabileInterventie[i][2].strip()):
            if(dataVeche.get() == ""):
                var4 = variabileInterventie[i][0]
            if(dataVeche.get() != variabileInterventie[i][0].strip() and dataVeche.get() != ""):
                ok = False
                break
            if(oraVeche.get() == ""):
                var5 = variabileInterventie[i][1]
            if(oraVeche.get() != variabileInterventie[i][1].strip() and oraVeche.get() != ""):
                ok = False
                break

        if(dataNoua.get() == ""):
            var1 = var4
        if(oraNoua.get() == ""):
            var2 = var5
        if(tipNou.get() == ""): 
            var3 = var6 

        cursor = conexiune.cursor()
        cursor.execute(
        "update Interventie SET Data = ?, Ora = ?, Tip = ? WHERE Data = ? AND Ora = ? AND Tip = ?;",
            (var1, var2, var3, var4, var5, var6)
        )
        conexiune.commit() 

    if(ok == False):
        messagebox.showerror("ERROR", "DATE INCORECTE INTRODUSE!")
    else:
        messagebox.showinfo("SUCCES", "Interventie modificata cu succes!") 
    for widget in base.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0,'end')
#----------------------------------------------------------------------------------------------

# DELETE APEL

def deleteApel():
    for widget in base.winfo_children():
        widget.destroy()

    global numeApelantSters, prenumeApelantSters

    label0 = tk.Label(base, text="STERGERE DIN TABELUL APEL", font=("Times", 18), bg = "#D3F0EF")
    label0.pack()
    label0.place(anchor='center',relx=0.5,rely=0.2)

    label1 = tk.Label(base, text="Introduceti numele apelantului de sters", font=("Times", 14), bg = "#D3F0EF")
    label1.pack()
    label1.place(anchor='center',relx=0.42,rely=0.45)

    numeApelantSters = tk.Entry(base, width=30)
    numeApelantSters.pack()
    numeApelantSters.place(anchor='center',relx=0.59, rely = 0.45)

    label2 = tk.Label(base, text="Introduceti prenumele apelantului de sters", font=("Times", 14), bg = "#D3F0EF")
    label2.pack()
    label2.place(anchor='center',relx=0.42,rely=0.55)

    prenumeApelantSters = tk.Entry(base, width=30)
    prenumeApelantSters.pack()
    prenumeApelantSters.place(anchor='center',relx=0.59, rely = 0.55)

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.6, rely = 0.83,anchor='center')

    submitButton = tk.Button(base, text = "STERGERE BAZA DE DATE", width=30,height=3,bg='brown',fg='white',command=deleteApelBazaDeDate)
    submitButton.pack()
    submitButton.place(anchor='center',relx=0.4,rely=0.83)

def deleteApelBazaDeDate():
    
    if(numeApelantSters.get() == "" or prenumeApelantSters.get() == ""):
        messagebox.showerror("ERROR", "Campurile nu pot fi goale!")
    else:
        cursor1 = conexiune.cursor()
        verificare = cursor1.execute(
            "SELECT * from Apel WHERE NumeApelant = ? AND PrenumeApelant = ?;",
            (numeApelantSters.get(), prenumeApelantSters.get())
        )

        if(verificare.fetchone()):
            cursor = conexiune.cursor()
            cursor.execute(
                "delete from Apel WHERE NumeApelant = ? AND PrenumeApelant = ?;",
                (numeApelantSters.get(), prenumeApelantSters.get())
            )
            conexiune.commit()
            messagebox.showinfo("SUCCESS", "STERGEREA DIN TABELUL APEL A FOST EFECTUATA!")
        else:
            messagebox.showerror("ERROR", "Campurile introduse nu exista in tabel!")
    for widget in base.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0,'end')
#----------------------------------------------------------------------------------------------

# DELETE LOCATIE

def deleteLocatie():
    for widget in base.winfo_children():
        widget.destroy()

    global longitudineOraStearsa

    label0 = tk.Label(base, text="STERGERE DIN TABELUL LOCATIE", font=("Times", 18), bg = "#D3F0EF")
    label0.pack()
    label0.place(anchor='center',relx=0.5,rely=0.2)

    label1 = tk.Label(base, text="Introduceti longitudinea ora de sters", font=("Times", 14), bg = "#D3F0EF")
    label1.pack()
    label1.place(anchor='center',relx=0.43,rely=0.5)

    longitudineOraStearsa = tk.Entry(base, width=30)
    longitudineOraStearsa.pack()
    longitudineOraStearsa.place(anchor='center',relx=0.59, rely = 0.5)

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.6, rely = 0.83,anchor='center')

    submitButton = tk.Button(base, text = "STERGERE BAZA DE DATE", width=30,height=3,bg='brown',fg='white',command=deleteLocatieBazaDeDate)
    submitButton.pack()
    submitButton.place(anchor='center',relx=0.4,rely=0.83)


def deleteLocatieBazaDeDate():
    

    if(longitudineOraStearsa.get() == ""):
        messagebox.showerror("ERROR", "Campurile nu pot fi goale!")

    else:
        cursor1 = conexiune.cursor()
        verificare = cursor1.execute(
            "SELECT * from Locatie WHERE LongitudineOra = ?;",
            (longitudineOraStearsa.get())
        )

        if(verificare.fetchone()):

            cursor = conexiune.cursor()
            cursor.execute(
                "delete from Locatie WHERE LongitudineOra = ?;",
                (longitudineOraStearsa.get())
            )
            conexiune.commit()
            messagebox.showinfo("SUCCESS", "STERGEREA DIN TABELUL LOCATIE A FOST EFECTUATA!")
        else:
            messagebox.showerror("ERROR", "Campurile introduse nu exista in tabel!")
   
    for widget in base.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0,'end')
#----------------------------------------------------------------------------------------------

# DELETE INTERVENTIE

def deleteInterventie():
    for widget in base.winfo_children():
        widget.destroy()

    global dataStearsa, oraStearsa

    label0 = tk.Label(base, text="STERGERE DIN TABELUL INTERVENTIE", font=("Times", 18), bg = "#D3F0EF")
    label0.pack()
    label0.place(anchor='center',relx=0.5,rely=0.2)

    label1 = tk.Label(base, text="Introduceti data de sters", font=("Times", 14), bg = "#D3F0EF")
    label1.pack()
    label1.place(anchor='center',relx=0.42,rely=0.45)

    dataStearsa = tk.Entry(base, width=30)
    dataStearsa.pack()
    dataStearsa.place(anchor='center',relx=0.56, rely = 0.45)

    label2 = tk.Label(base, text="Introduceti ora de sters", font=("Times", 14), bg = "#D3F0EF")
    label2.pack()
    label2.place(anchor='center',relx=0.42,rely=0.55)

    oraStearsa = tk.Entry(base, width=30)
    oraStearsa.pack()
    oraStearsa.place(anchor='center',relx=0.56, rely = 0.55)

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.6, rely = 0.83,anchor='center')

    submitButton = tk.Button(base, text = "STERGERE BAZA DE DATE", width=30,height=3,bg='brown',fg='white',command=deleteInterventieBazaDeDate)
    submitButton.pack()
    submitButton.place(anchor='center',relx=0.4,rely=0.83)


def deleteInterventieBazaDeDate():
    
    if(dataStearsa.get() == "" or oraStearsa.get == ""):
        messagebox.showerror("ERROR", "Campurile nu pot fi goale!")
    else:
        cursor1 = conexiune.cursor()
        verificare = cursor1.execute(
            "SELECT * from Interventie WHERE Data = ? AND Ora = ?;",
            (dataStearsa.get(), oraStearsa.get())
        )

        if(verificare.fetchone()):

            cursor = conexiune.cursor()
            cursor.execute(
                "delete from Interventie WHERE Data = ? AND Ora = ?;",
                (dataStearsa.get(), oraStearsa.get())
            )
            conexiune.commit()
            messagebox.showinfo("SUCCESS", "STERGEREA DIN TABELUL INTERVENTIE A FOST EFECTUATA!")
        else:
            messagebox.showerror("ERROR", "Campurile introduse nu exista in tabel!")

    for widget in base.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0,'end')
#----------------------------------------------------------------------------------------------

def statisticaSimpla1():
    for widget in base.winfo_children():
        widget.destroy()
    
    label00 = tk.Label(base, text='Numele si prenumele tuturor operatorilor care au avut apeluri mai lungi de 5 minute, precum si durata apelului respectiv', font=("Times", 18, "italic"), bg= "#D3F0EF")
    label00.place(relx=0.5,rely=0.1, anchor='center')

    cursor = conexiune.cursor()
    cursor.execute(
        """SELECT O.Nume, O.Prenume, A.DurataApel
        FROM Operator O INNER JOIN Apel A ON (O.OperatorID = A.OperatorID) AND A.DurataApel > '00:05:00' ;""",
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=10)
    frm.place(rely=0.5,relx = 0.5,anchor='center')

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3'), show='headings', height=4, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Nume")
    tv.heading(2,text="Prenume")
    tv.heading(3,text="Durata Apel")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2]))

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=dupaLogin, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.4, rely = 0.85,anchor='center')

    nextButton = tk.Button(base, text = "Statistica urmatoare", width=30,height=3,bg='brown',fg='white',command=statisticaSimpla2)
    nextButton.pack()
    nextButton.place(anchor='center',relx=0.6,rely=0.85)

def statisticaSimpla2():
    for widget in base.winfo_children():
        widget.destroy()
    
    label0 = tk.Label(base, text='Interventiile care au avut loc la o longitudine cu ora mai mare de 20 si minutele mai mici de 45', font=("Times", 20, "italic"), bg= "#D3F0EF")
    label0.place(relx=0.5,rely=0.1, anchor='center')

    cursor = conexiune.cursor()
    cursor.execute(
        """SELECT distinct I.Data, I.Ora, I.Tip 
        FROM Interventie I INNER JOIN  Locatie_Serviciu_Interventie LSI ON (LSI.InterventieID = I.InterventieID) INNER JOIN Locatie L ON (L.LocatieID  = LSI.LocatieID) 
        WHERE L.LongitudineOra > 20 AND L.LongitudineMinute < 45;""",
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=40)
    frm.place(rely=0.5,relx = 0.5,anchor='center')

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3'), show='headings', height=4, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Data")
    tv.heading(2,text="Ora")
    tv.heading(3,text="Tip")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2]))

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=statisticaSimpla1, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.4, rely = 0.85,anchor='center')

    nextButton = tk.Button(base, text = "Statistica urmatoare", width=30,height=3,bg='brown',fg='white',command=statisticaSimpla3)
    nextButton.pack()
    nextButton.place(anchor='center',relx=0.6,rely=0.85)


def statisticaSimpla3():
    for widget in base.winfo_children():
        widget.destroy()

    label00 = tk.Label(base, text='Locatiile la care a fost solicitat serviciul SMURD', font=("Times", 20, "italic"), bg= "#D3F0EF")
    label00.place(relx=0.5,rely=0.1, anchor='center')

    cursor = conexiune.cursor()
    cursor.execute(
        """SELECT distinct L.LongitudineOra, L.LongitudineMinute, L.LongitudineSecunde, L.LatitudineOra, L.LatitudineMinute, L.LatitudineSecunde 
        FROM Locatie L INNER JOIN  Locatie_Serviciu_Interventie LSI ON (L.LocatieID = LSI.LocatieID) INNER JOIN Serviciu112 S ON (LSI.ServiciuID = S.ServiciuID) 
        WHERE S.NumeServiciu = 'SMURD';""",
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=10)
    frm.place(rely=0.5,relx = 0.5,anchor='center')

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4','5','6'), show='headings', height=4, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Longitudine Ora")
    tv.heading(2,text="Longitudine Minute")
    tv.heading(3,text="Longitudine Secunde")
    tv.heading(4,text="Latitudine Ora")
    tv.heading(5,text="Latitudine Minute")
    tv.heading(6,text="Latitudine Secunde")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3], i[4], i[5]))

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=statisticaSimpla2, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.4, rely = 0.85,anchor='center')

    nextButton = tk.Button(base, text = "Statistica urmatoare", width=30,height=3,bg='brown',fg='white',command=statisticaSimpla4)
    nextButton.pack()
    nextButton.place(anchor='center',relx=0.6,rely=0.85)

def statisticaSimpla4():
    for widget in base.winfo_children():
        widget.destroy()

    global statisticaCombo
    
    label00 = tk.Label(base, text='Numele si prenumele apelantilor care au fost preluati de un operator pe nume ', font=("Times", 20, "italic"), bg= "#D3F0EF")
    label00.place(relx=0.5,rely=0.1, anchor='center')

    statisticaCombo = ttk.Combobox(base, width=15, height=4)
    statisticaCombo.pack()
    statisticaCombo['values']=("Popescu", "Boraciu", "Popa", "Stanescu", "Draghici", "Iancu", "Urzica", "Marcu")
    statisticaCombo.set("Popescu")
    statisticaCombo.place(relx=0.83, rely=0.1,anchor='center')

    buton = tk.Button(base, text = "Afisati", width=30,height=3,bg='black',fg='white',command=afisareStatisticaSimpla4)
    buton.pack()
    buton.place(anchor='center',relx=0.5,rely=0.2)

def afisareStatisticaSimpla4():

    cursor = conexiune.cursor()
    cursor.execute(
        "SELECT A.NumeApelant, A.PrenumeApelant FROM Apel A INNER JOIN Operator O ON (A.OperatorID = O.OperatorID) WHERE O.Nume = ?;",
        (statisticaCombo.get())
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=10)
    frm.place(rely=0.5,relx = 0.5,anchor='center')

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2'), show='headings', height=4, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Nume")
    tv.heading(2,text="Prenume")


    for i in rows:
        tv.insert('','end', values=(i[0], i[1]))

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=statisticaSimpla3, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.4, rely = 0.85,anchor='center')

    nextButton = tk.Button(base, text = "Statistica urmatoare", width=30,height=3,bg='brown',fg='white',command=statisticaSimpla5)
    nextButton.pack()
    nextButton.place(anchor='center',relx=0.6,rely=0.85)

def statisticaSimpla5():
    for widget in base.winfo_children():
        widget.destroy()

    label00 = tk.Label(base, text='Toate apelurile mai lungi de 3 minute a caror interventie a avut loc inainte de 1 ianuarie 2019', font=("Times", 20, "italic"), bg= "#D3F0EF")
    label00.place(relx=0.5,rely=0.1, anchor='center')

    cursor = conexiune.cursor()
    cursor.execute(
        """SELECT A.DurataApel, A.NumeApelant, A.PrenumeApelant, A.NumarDeTelefon 
        FROM Apel A INNER JOIN Interventie I ON (A.InterventieID = I.InterventieID) WHERE A.DurataApel > '00:03:00' AND I.Data < '2019-01-01';""",
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=10)
    frm.place(rely=0.5,relx = 0.5,anchor='center')

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4'), show='headings', height=4, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Durata Apel")
    tv.heading(2,text="Nume")
    tv.heading(3,text="Prenume")
    tv.heading(4,text="Numar de Telefon") 

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3]))

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=statisticaSimpla4, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.4, rely = 0.85,anchor='center')

    nextButton = tk.Button(base, text = "Statistica urmatoare", width=30,height=3,bg='brown',fg='white',command=statisticaSimpla6)
    nextButton.pack()
    nextButton.place(anchor='center',relx=0.6,rely=0.85)

def statisticaSimpla6():
    for widget in base.winfo_children():
        widget.destroy()

    label00 = tk.Label(base, text='Toti operatorii care au avut apeluri mai mari de 6 minute sau care au preluat un apelant pe nume Ionescu', font=("Times", 20, "italic"), bg= "#D3F0EF")
    label00.place(relx=0.5,rely=0.1, anchor='center')

    cursor = conexiune.cursor()
    cursor.execute(
        """SELECT O.Nume, O.Prenume, O.Email, O.NumarDeTelefon
        FROM Operator O INNER JOIN Apel A ON (O.OperatorID = A.OperatorID) WHERE A.DurataApel > '00:06:00' OR A.NumeApelant = 'Ionescu';""",
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=10)
    frm.place(rely=0.5,relx = 0.5,anchor='center')

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4'), show='headings', height=4, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Nume")
    tv.heading(2,text="Preume")
    tv.heading(3,text="Email")
    tv.heading(4,text="Numar de Telefon") 

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3]))

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=statisticaSimpla5, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.4, rely = 0.85,anchor='center')

    longText = """Statistica urmatoare
    Urmeaza niste statistici mai interesante"""

    nextButton = tk.Button(base, text = longText, width=33,height=3,bg='brown',fg='white',command=statisticaComplexa1)
    nextButton.pack()
    nextButton.place(anchor='center',relx=0.6,rely=0.85)

def statisticaComplexa1():
    for widget in base.winfo_children():
        widget.destroy()

    label00 = tk.Label(base, text='Operatorii care au avut apeluri mai scurte decat minimul duratei apelului operatorului pe nume Popescu Andrei', font=("Times", 20, "italic"), bg= "#D3F0EF")
    label00.place(relx=0.5,rely=0.1, anchor='center')

    cursor = conexiune.cursor()
    cursor.execute(
        """ select distinct O.Nume, O.Prenume 
            from Operator O inner join Apel A on (A.OperatorID = O.OperatorID) 
            where A.DurataApel < (select MIN(A.DurataApel)  
					             from Apel A inner join Operator O on (A.OperatorID = O.OperatorID) and O.Nume = 'Popescu' and O.Prenume = 'Andrei')        
            group by O.OperatorID, O.Nume, O.Prenume ;""",
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=10)
    frm.place(rely=0.5,relx = 0.5,anchor='center')

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2'), show='headings', height=4, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Nume")
    tv.heading(2,text="Preume")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1]))

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=statisticaSimpla6, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.4, rely = 0.85,anchor='center')

    nextButton = tk.Button(base, text = "Statistica urmatoare", width=30,height=3,bg='brown',fg='white',command=statisticaComplexa2)
    nextButton.pack()
    nextButton.place(anchor='center',relx=0.6,rely=0.85)

def statisticaComplexa2():
    for widget in base.winfo_children():
        widget.destroy()

    label00 = tk.Label(base, text='Interventiile care au avut loc la locatii in care latitudinea secunde este mai mare decat media latitudielor secunde pe toate locatiile', font=("Times", 16, "italic"), bg= "#D3F0EF")
    label00.place(relx=0.5,rely=0.1, anchor='center')

    cursor = conexiune.cursor()
    cursor.execute(
        """select distinct I.Data, I.Ora, I.Tip
        from Interventie I, Locatie_Serviciu_Interventie LSI, Locatie L where I.InterventieID = LSI.InterventieID and LSI.LocatieID = L.LocatieID
        group by I.Data, I.Ora, I.Tip, L.LatitudineSecunde
        having L.LatitudineSecunde > (select AVG(L2.LatitudineSecunde) from Locatie L2)  ;""",
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=10)
    frm.place(rely=0.5,relx = 0.5,anchor='center')

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3'), show='headings', height=4, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Data")
    tv.heading(2,text="Ora")
    tv.heading(3,text="Tip")

    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2]))

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=statisticaComplexa1, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.4, rely = 0.85,anchor='center')

    nextButton = tk.Button(base, text = "Statistica urmatoare", width=30,height=3,bg='brown',fg='white',command=statisticaComplexa3)
    nextButton.pack()
    nextButton.place(anchor='center',relx=0.6,rely=0.85)    

def statisticaComplexa3():
    for widget in base.winfo_children():
        widget.destroy()

    global statisticaCombo2

    label00 = tk.Label(base, text='Apelantii si operatorul ce i-a preluat pentru care durata apelului este mai mica decat durata primului apel din                ', font=("Times", 18, "italic"), bg= "#D3F0EF")
    label00.place(relx=0.5,rely=0.1, anchor='center')

    statisticaCombo2 = ttk.Combobox(base, width=15, height=4)
    statisticaCombo2.pack()
    statisticaCombo2['values']=("2018", "2019", "2020", "2021", "2022", "2023")
    statisticaCombo2.set("2023")
    statisticaCombo2.place(relx=0.87, rely=0.1,anchor='center')

    buton = tk.Button(base, text = "Afisati", width=30,height=3,bg='black',fg='white',command=afisareStatisticaComplexa3)
    buton.pack()
    buton.place(anchor='center',relx=0.5,rely=0.2)

def afisareStatisticaComplexa3():

    cursor = conexiune.cursor()
    cursor.execute(
        """select distinct A.NumeApelant, A.PrenumeApelant, O.Nume, O.Prenume
        from Apel A inner join Operator O on (A.OperatorID = O.OperatorID)
        where A.DurataApel < (select TOP 1 A2.DurataApel
				        	from Apel A2 inner join Interventie I on (A2.InterventieID = I.InterventieID)
					        where YEAR(I.Data) = ?);""",
        (statisticaCombo2.get())
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=10)
    frm.place(rely=0.5,relx = 0.5,anchor='center')

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2','3','4'), show='headings', height=4, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Nume Apelant")
    tv.heading(2,text="Prenume Apelant")
    tv.heading(3,text="Nume Operator")
    tv.heading(4,text="Prenume Operator")


    for i in rows:
        tv.insert('','end', values=(i[0], i[1], i[2], i[3]))

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=statisticaComplexa2, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.4, rely = 0.85,anchor='center')

    nextButton = tk.Button(base, text = "Statistica urmatoare", width=30,height=3,bg='brown',fg='white',command=statisticaComplexa4)
    nextButton.pack()
    nextButton.place(anchor='center',relx=0.6,rely=0.85) 

def statisticaComplexa4():
    for widget in base.winfo_children():
        widget.destroy()

    label00 = tk.Label(base, text='Numele si prenumele operatorilor ordonati dupa numarul de telefon al primului apelant in ordine alfabetica cu care au vorbit.', font=("Times", 20, "italic"), bg= "#D3F0EF")
    label00.place(relx=0.5,rely=0.1, anchor='center')

    cursor = conexiune.cursor()
    cursor.execute(
        """select o.Nume, o.Prenume
        from Operator O
        order by (select TOP 1 a.NumarDeTelefon from apel a, operator o2 where a.OperatorID = o2.OperatorID
			order by a.NumeApelant asc);""",
    )
    rows = cursor.fetchall()

    frm = tk.Frame(base)
    frm.pack(pady=10)
    frm.place(rely=0.5,relx = 0.5,anchor='center')

    scrollBar = tk.Scrollbar(frm)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tv = ttk.Treeview(frm, columns=('1','2'), show='headings', height=4, yscrollcommand=scrollBar.set)
    tv.pack()

    scrollBar.config(command=tv.yview)

    tv.heading(1,text="Nume")
    tv.heading(2,text="Prenume")


    for i in rows:
        tv.insert('','end', values=(i[0], i[1]))

    backButton = tk.Button(base, text="Înapoi",width=30, height=3, command=statisticaComplexa3, fg='white',bg='black')
    backButton.pack()
    backButton.place(relx = 0.4, rely = 0.85,anchor='center')   
#----------------------------------------------------------------------------------------------

base.after(0, primaPagina)

def closeProgram():
    conexiune.close()
    base.destroy()
    
base.mainloop()  