

from tkinter import *
# Ereignisbehandlung

def buttonVerschluesselnClick():
    klartext = textfeld1.get('1.0', 'end').strip()
    geheimtext = ''
    for zeichen in klartext:
        zahl = ord(zeichen)
        neuezahl = zahl + 3
        if neuezahl > ord('Z'):
            neuezahl = neuezahl - 26
        neuesZeichen = chr(neuezahl)
        geheimtext = geheimtext + neuesZeichen
    textfeld2.delete('1.0', 'end')
    textfeld2.insert('1.0', geheimtext)

def buttonEntschluesselnClick():
    geheimtext = textfeld2.get('1.0', 'end').strip()
    klartext = ''
    for zeichen in geheimtext:
        zahl = ord(zeichen)
        neuezahl = zahl - 3
        if neuezahl < ord('A'):
            neuezahl = neuezahl + 26
        neuesZeichen = chr(neuezahl)
        klartext = klartext + neuesZeichen
    textfeld1.delete('1.0', 'end')
    textfeld1.insert('1.0', klartext)

def buttonLoeschenQuelltextClick():
    textfeld1.delete('0.0', 'end')

def buttonLoeschenGeheimtextClick():
    textfeld2.delete('0.0', 'end')
        
# Fenster
tkFenster = Tk()
tkFenster.title('Textverarbeitung')
tkFenster.geometry('360x194')
# Textfelder
textfeld1 = Text(master=tkFenster, width=39, height=4, wrap='word')
textfeld1.place(x=8, y=8)
scrollbar1 = Scrollbar(master=tkFenster)
scrollbar1.place(x=342, y=8, width=10, height=68)
textfeld1.config(yscrollcommand=scrollbar1.set)
scrollbar1.config(command=textfeld1.yview)
textfeld2 = Text(master=tkFenster, width=39, height=4, wrap='word')
textfeld2.place(x=8, y=118)
scrollbar2 = Scrollbar(master=tkFenster)
scrollbar2.place(x=342, y=118, width=10, height=68)
textfeld2.config(yscrollcommand=scrollbar2.set)
scrollbar2.config(command=textfeld2.yview)
# Button
buttonLaden = Button(master=tkFenster, text='verschlüsseln',
                     command=buttonVerschluesselnClick)
buttonLaden.place(x=96, y=88, width=80, height=20)
buttonSpeichern = Button(master=tkFenster, text='entschlüsseln',
                         command=buttonEntschluesselnClick)
buttonSpeichern.place(x=184, y=88, width=80, height=20)
buttonLoeschenQuelltext = Button(master=tkFenster, text='löschen',
                                 command=buttonLoeschenQuelltextClick)
buttonLoeschenQuelltext.place(x=8, y=88, width=80, height=20)
buttonLoeschenGeheimtext = Button(master=tkFenster, text='löschen',
                                  command=buttonLoeschenGeheimtextClick)
buttonLoeschenGeheimtext.place(x=272, y=88, width=80, height=20)
# Aktivierung des Fensters
tkFenster.mainloop()
