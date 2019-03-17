# # -*- coding: utf-8 -*-

import subprocess
from subprocess import Popen, PIPE
import tkinter as tk
from tkinter import ttk, scrolledtext, Entry
from tkinter.ttk import Combobox


win = tk.Tk()
win.title("Aegis")
win.minsize(width=1800, height=900)
win.maxsize(width=1800, height=900)
#win.configure(background="#eaeaea")
#reportcmd = 'python aegis.py --pot aegisec.pot --domain aegisec.me'
#rExtractcmd =
#lExratractcmd =
# domainEntered = tkinter.domInput
#potEntered = potInput




# Select File Label
ttk.Label(win, text="Remote Extraction").place(x=80, y=1)
ttk.Label(win, text="Username:").place(x=5, y=30)


# User selected file
rUser = tk.StringVar()
remoteUser = ttk.Entry(win, width=30, textvariable=rUser, )
remoteUser.place(x=5, y=50)

# Search Label
ttk.Label(win, text="Password:").place(x=5, y=75)

# Textbox Entry
rPass = tk.StringVar()
remotePass = ttk.Entry(win, width=30, textvariable=rPass, )
remotePass.place(x=5, y=95)

# Search Label
ttk.Label(win, text="Target IP:").place(x=5, y=120)

# Textbox Entry
rIP = tk.StringVar()
remoteIP = ttk.Entry(win, width=30, textvariable=rIP, )
remoteIP.place(x=5, y=140)

remoteExtract = ttk.Button(win, width=29, text="Extract")
remoteExtract.place(x=5, y=170)


def lExtractToScroll():
    userEntered = remoteUser.get()
    passEntered = remotePass.get()
    ipEntered = remoteIP.get()
    rExtractcmd = 'python aegis.py --username '+userEntered+' --password '+passEntered+' --target '+ipEntered
    stdout = Popen(rExtractcmd, shell=True, stdout=PIPE).stdout
    rExtractOut = stdout.read()
    scr.insert(tk.INSERT, rExtractOut)


# Search Limit Label
ttk.Label(win, text="Local Extraction:").place(x=70, y=210)

localExplanation = "1. Open a command prompt as admin on the DC\n" \
                   "2. Run ntdsutil'ac i ntds''ifm''create full c:/temp' q q\n" \
                   "3. Extract c:/temp/Active Directory/ntds.dit and c:/temp/registry/SYSTEM to your computer running Aegis"
localMessage = tk.Message(win, width=220, text=localExplanation).place(x=5, y=235)

# Search Label
ttk.Label(win, text="SYSTEM file path:").place(x=5, y=382)

# Textbox Entry
sysInput = tk.StringVar()
systemInput = ttk.Entry(win, width=30, textvariable=sysInput, )
systemInput.place(x=5, y=402)

# Search Label
ttk.Label(win, text="ntds.dit file path:").place(x=5, y=427)

# Textbox Entry
ntdsInput = tk.StringVar()
ntdsutilInput = ttk.Entry(win, width=30, textvariable=ntdsInput, )
ntdsutilInput.place(x=5, y=447)

localExtract = ttk.Button(win, width=29, text="Extract", command=lambda : lExtractToScroll())
localExtract.place(x=5, y=477)

def lExtractToScroll():
    sysEntered = systemInput.get()
    ntdsEntered = ntdsutilInput.get()
    lExtractcmd = 'python aegis.py --system '+sysEntered+' --ntds '+ntdsEntered+'.dit'
    stdout = Popen(lExtractcmd, shell=True, stdout=PIPE).stdout
    lExtractOut = stdout.read()
    scr.insert(tk.INSERT, lExtractOut)

ttk.Label(win, text="Active Directory Evaluation").place(x=40, y=522)

# Search Label
ttk.Label(win, text="Pot filename:").place(x=5, y=547)

# Textbox Entry
potInput = tk.StringVar()
potFileInput = ttk.Entry(win, width=30, textvariable=potInput )
potFileInput.place(x=5, y=567)

# Search Label
ttk.Label(win, text="Domain name:").place(x=5, y=592)

# Textbox Entry
domInput = tk.StringVar()
domainInput = ttk.Entry(win, width=30, textvariable=domInput )
domainInput.place(x=5, y=612)
# domainInput.focus()



# Using a scrolled Text control
scrolW = 168
scrolH = 52
scr = scrolledtext.ScrolledText(win, width=(scrolW), height=(scrolH), font=('Calibri', 10, 'bold'), wrap=tk.WORD,  background="#f0f0f0")
scr.place(x=260, y=1)




def reportToScroll():
    potEntered = potFileInput.get()
    domainEntered = domainInput.get()
    reportcmd = 'python aegis.py --pot ' + potEntered + '.pot --domain ' + domainEntered
    stdout = Popen(reportcmd, shell=True, stdout=PIPE).stdout
    reportOut = stdout.read()
    scr.insert(tk.INSERT, reportOut)

def toPassCloud():
    potEntered = potFileInput.get()
    domainEntered = domainInput.get()
    reportcmd = 'python aegis.py --pot ' + potEntered + '.pot --domain ' + domainEntered +' --output password_cloud'
    stdout = Popen(reportcmd, shell=True, stdout=PIPE).stdout
    reportOut = stdout.read()
    scr.insert(tk.INSERT, reportOut)

def ClearText():
    scr.delete(1.0, tk.END)


# Show Normal Map Button
outputExtract = ttk.Button(win, width=29, text="Generate Report", command=lambda: reportToScroll())
outputExtract.place(x=5, y=647)

outputExtract = ttk.Button(win, width=29, text="Generate Password Cloud", command=lambda: toPassCloud())
outputExtract.place(x=5, y=682)

ttk.Label(win, text="Email Compromise Check").place(x=40, y=722)

# Search Label
ttk.Label(win, text="Email:").place(x=5, y=757)

# Textbox Entry
emInput = tk.StringVar()
emailInput = ttk.Entry(win, width=30, textvariable=emInput)
emailInput.place(x=5, y=777)
# emailInput.focus()

outputEmail = ttk.Button(win, width=29, text="Check Email")
outputEmail.place(x=5, y=812)

# Clear Console Button
clearButton = ttk.Button(win, width=30, text="Clear Console ", command=lambda : ClearText())
clearButton.place(x=5, y=862)

# Place cursor into name Entry
remotePass.focus()

# Start GUI
win.mainloop()
