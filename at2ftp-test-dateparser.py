### AT2FTP
### eigentlich: AT-PDFs-2-old.uhl-media.de
### V 1.55
### (c) Andy Uhl
### Dieses Programm überwacht einen Folder und überträgt modifiziertte und neue PDF-Dateien auf den FTP-Server, wenn diese dem Schema einer AT entsprechen. Zudem wird zum Programmstart das gesamte Zielverzeichnis mit dem Quellverzeichnis vergleich und fehlende ATs-PDFs übertragen.

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#from watchdog.events import LoggingEventHandler 
#import logging
from datetime import datetime, timedelta
import ftplib
import os
#from dateutil import parser
from datetime import datetime
import dateparser

global filepath, filename, um_atstart, um_atstop

um_sourcepath = "P:Dokument/3/" #hier holt man die Daten ab
#um_sourcepath = "C:/PythonProgrammeVilla/at2ftp-Datenuebertragung/testdaten/" #hier holt man die Daten ab
um_ftpuser = "gast"
um_ftpserver = "81.169.182.75"              # = "ftp.old.uhl-media.de"
um_ftppassword = "Willkommen#2015"
um_ftpdirectory = "ATs"
#um_ftpdirectory = "testAT"
um_atstart = 191700                         #AT von
um_atstop = 299999                          #AT bis
filename="/123456.txt"
filepath="c:/123456.txt"


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = datetime.now()

    def on_modified(self, event):
        print("\a")
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()
        print(str(datetime.now()))    
        print(f'Event type: {event.event_type}  path : {event.src_path}')   
        
        filepath = event.src_path
        slashpos = filepath.rfind("/")
        filename = filepath[slashpos +1:]

        print("Neuer Filepath: ",filepath, " erkannt.")
        #print("Neuer Filename: ",filename, " extrahiert.")

        if atnamecheck(filename) == True:
            time.sleep(3)
            if anftpsenden(filename, filepath) == False:
                print("\a\a\a### an FTP senden nicht möglich - Fehler ###")

    
def anftpsenden(filename,filepath):

    with ftplib.FTP(um_ftpserver) as ftp:
        try:
            ftp.login(um_ftpuser, um_ftppassword)
            ftp.cwd(um_ftpdirectory)  
            
            with open(filepath, 'rb') as fp:
                res = ftp.storbinary("STOR " + filename, fp)
                if not res.startswith('226 Transfer complete'):   
                    print('\a\a\aUpload failed')
                    return False
                else:
                    print("\a>>> OK: Datei wurde erfolgreich auf old.uhl-media.de/ATs übertragen.")
                    return True   
        except ftplib.all_errors as e:
            print('\a\a\aFTP error: #', e) 
            return(False)                                 


def atnamecheck(filename):

    try:
        um_rules = [int(filename[0:6]) in range(um_atstart, um_atstop), filename[len(filename)-4:] == ".pdf", len(filename) == 10]
        if all(um_rules):
            print(filename," ist eine AT-PDF.")
            return True
        else:
            print("Keine AT-PDF erkannt für: ",filename,"\n")
            return False
    except ValueError:
        print("Keine AT-PDF (Valuerror) erkannt für: ",filename,"\n")  
        return False


def ftpdirvergleich():

    #FTP Verzeichnis auslesen
    with ftplib.FTP(um_ftpserver) as ftp:
        try:
            ftp.login(um_ftpuser, um_ftppassword)
            ftp.cwd(um_ftpdirectory)  
            ftpfiles=[]
            ftpfilename=[]
            ftpfiledate=[]
            ftp.dir(ftpfiles.append)
            print("FTP-Verzeichnis auslesen...")

            for n in range(0,20):
                ftpfilename.append(ftpfiles[n][len(ftpfiles[n])-10:])
                tokens = ftpfiles[n].split(maxsplit = 9)
                time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
                time = dateparser.parse(time_str)
                #time = datetime.fromtimestamp(time_str)
                print(n, "dateparser: ",time) 
                ftpfiledate.append(time)
            ftp.quit()             
        except ftplib.all_errors as e:
            print('\a FTP error: ', e)

    #Quellverzeichnis auslesen
    print("Quellverzeichnis auslesen...")
    sourcedir = um_sourcepath
    sourcedate = []
    sourcefile = os.listdir(sourcedir) 
    
    for n in range(0,20):
        #zeit = time.parse(os.path.getmtime(sourcedir+sourcefile[n])).strftime('%Y-%m-%d %H:%M:%S')
        zeit = datetime.fromtimestamp(os.path.getmtime(sourcedir+sourcefile[n])).strftime('%Y-%m-%d %H:%M:%S')

        sourcedate.append(zeit)
        print("Sourcezeit = ", zeit)
        #print("Sourcefile # ",n, "<<< ",sourcefile[n], "-",sourcedate[n],"-")           

    # Verzeichnisse beim Start vergleichen und fehlende Daten in Zielverzeichnis auf FTP Server übertragen
    # zudem: Zeitvergleich der Quell-/FTP-Datei und ggf. Update der Datei
    enth = 0
    fehlt = 0
    upd = 0
    neu = 0

    print("Vergleich FTP- / Quellverzeichnis...")
  
    for n in range(0, 20):
        if sourcefile[n] in ftpfilename:
            #print("Bereits im FTP enthalten: ",sourcefile[n])
            enth +=1
            x = ftpfilename.index(sourcefile[n])
            #print("Zeitvergleich: \n S=",sourcefile[n], " = ", sourcedate[n]," \n F=", ftpfilename[x], " = ", ftpfiledate[x],":")
            delta = (sourcedate[n]) - (ftpfiledate[x])
            #print("Zeitdelta = ",delta, type(delta))
        else:
            #print("\n",sourcefile[n], " ist nicht im FTP enthalten.")
            fehlt +=1
            filename = sourcefile[n]
            filepath = um_sourcepath + sourcefile[n]
            print("\nNeu erzeugen: ",filepath)
            if atnamecheck(filename) == True:
                anftpsenden(filename,filepath)
                neu +=1
    print("Ergebnis des Verzeichnis-Vergleichs:")
    print("Enthalten waren bereits: ", enth)
    print("Es fehlten: ", fehlt)    
    print("Updates: ",upd)
    print("Neu erzeugt: ",neu)
    



if __name__ == "__main__":

    print(">>> at2ftp >>>\n")

    ftpdirvergleich()

    print("Starte Verzeichnisüberwachung...")


    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=um_sourcepath, recursive=False)

     # Set the format for logging info 
   # logging.basicConfig(level=logging.DEBUG, 
    #                    format='%(asctime)s - %(message)s', 
    #                    datefmt='%Y-%m-%d %H:%M:%S') 
    #log_event_handler = LoggingEventHandler()
    #log_observer = Observer()
    #log_observer.schedule(log_event_handler, path=um_sourcepath, recursive=True)
    #log_observer.start()                    

    observer.start()

    try:
        while True:
            time.sleep(10)
            #print('bin wach...:', str(datetime.now()))
    except KeyboardInterrupt:
        observer.stop()
       # log_observer.stop()
    observer.join(timeout=None)
    