# Azure MSSQL Python test

## Objective 

Testing connectivity from AKS clusters to Azure Micrsoft SQL Server Endpoint can be a cumbersome task as we need to download and install different tools to work with respective Database. In this example, we will use a simple python script that use the pymssql official library to execute a connection on the provided endpoint with the username, password and database name provided as environment variables.

## Prerequisites

We will use a nginx based Pod where will install the following components:

Python3
Python3-pip
pymssql PIP Library

## Installation

We can use a standard nginx Pod or a preconfigured one as described in the Source Code section
```
kubectl run nginx --image=nginx
kubectl exec -it nginx -- bash

apt update -y

apt install python3 -y

apt install python3-pip

pip install pymssql

mkdir /app
cd /app

cat << EOF > ./azuresqltest.py
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
EOF
```
Adding the Environment Variables that holds our SQL endpoint, username, password and database name along with the time interval in second:

```
export SQLSERVER="yourslqname.database.windows.net"
export SQLUSER="yourskluser@yoursqlname.database.windows.net"
export SQLPASS="yoursqlpassword"
export SQLDB="yousql_db_name"
export TIMEINTERVAL="5"
```

Run your script with the following command:

**python3 ./azuresqltest.py**

If successful connection, it will output the following:

```
Starting AzureSQL Connectivity Check: ... 
Successful Connected to Azure SQL
```

Otherwise, it will throw an error like this:

```
Starting AzureSQL Connectivity Check:...
10/11/2022 14:50:53 A MSSQLDriverException has been caught.
```
It will also log the requests in a local file on Pod, azsqltest.log. For data persistency please mount an emptyDir and share the script's folder with the underlying Node.
