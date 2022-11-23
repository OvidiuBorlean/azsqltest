import pymssql  
import os
import time
from datetime import datetime

def checkAzureSql(server, user, password, database):
  try:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    conn = pymssql.connect(server=server, user=user, password=password, database=database)
    cursor = conn.cursor()
    print("Successfull Connected to Azure SQL")
    conn.close()
    file1= open("azsqltest.log","a")
    content = dt_string + " " + "Successfull Connected to Azure SQL"
    file1.write(content)
    file1.write("\n")
    file1.close()
  except:
    print(dt_string + " " + "A MSSQLDriverException has been caught.")
    file1= open("azsqltest.log","a")
    content = dt_string + " " + "A MSSQLDriverException has been caught."
    file1.write(content)
    file1.write("\n")
    file1.close()
if __name__ == '__main__':
  print("Starting AzureSQL Connectivity Check:...")
  myHostname = os.getenv('SQLSERVER')
  myPGUser = os.getenv("SQLUSER")
  myPassword = os.environ.get('SQLPASS')
  myDB = os.environ.get('SQLDB')
  interval = os.environ.get('TIMEINTERVAL')
  while True:
    checkAzureSql(myHostname, myPGUser, myPassword, myDB)
    time.sleep(int(interval))
