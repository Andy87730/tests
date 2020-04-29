import datetime
import pyodbc
import re
import locale

locale.setlocale(locale.LC_ALL, 'german')

#dbtext = "Test2106Andy"


#zeit = datetime.datetime.now()
#dbtext = dbtext.replace("'","_")
#protokolltext = "a-man Schreibvorgang: " + str(zeit) + " = " + dbtext

#Protokolltext in neue DB schreiben
con = pyodbc.connect(r'DRIVER={SQL Server};Server=PAGINANET\SQLEXPRESS;database=paginanet_uhl;uid=sa;pwd=$sql2015!;')
cur = con.cursor()

#cur.execute("SELECT MAX(LfdNummer) FROM um_adressmanager")

#for row in cur:
#    protholelfdnr = int(row[0])

#protneuelfdnr = protholelfdnr + 1

#sqlprotanw = "INSERT INTO um_adressmanager (aman_protokolltext) VALUES ('TEST1939')"


#print("\n",protneuelfdnr,":", sqlprotanw)

sqlprotanw = "UPDATE dbo.PROGRAMM_Nummern SET Nummer = 23568 WHERE Art = 'Kunden'"
cur.execute(sqlprotanw)
con.commit

con.close