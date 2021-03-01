# Wine-Data-Dag

![alt text](https://thecraftycask.com/wp-content/uploads/2018/07/crafty-cask-craft-wine-banner-e1543284316865.jpg)

<h1>Wine-Data Airflow DAG</h1>
Mini Big-Data project that uses Airflow, SFTP, MySQL, Redis and AWS to perform a simple ETL process involving moving files 
from an SFTP server set up on EC2, transforming/cleaning the data with PySpark and loading the finished product into a MySQL
instance also hosted on EC2.

<h1>Repository Structure</h1>

```
├── docker-compose.yml
├── ETL
│   ├── airflowkey.pem
│   ├── DAG.py
│   ├── load.py
│   ├── __pycache__
│   │   ├── DAG.cpython-37.pyc
│   │   ├── SFTPToS3Operator.cpython-37.pyc
│   │   └── SFTPToS3Operator.cpython-38.pyc
│   ├── schema.txt
│   ├── SFTPToS3Operator.py
│   └── transform.py
├── __pycache__
│   └── DAG.cpython-38.pyc
├── requirements.txt
└── Tests
    ├── __pycache__
    │   └── test.cpython-38.pyc
    └── test.py
```

Above you can see the layout of the repository, containing a ```docker-compose.yml``` file, a ```requirements.txt``` 
file and a folder with the ETL steps and the custom SFTPToS3 operator. The ```docker-compose.yml``` file
is where all the environment variables (AWS Access Key, MySQL Password etc) can be found and will need to be 
changed to suit individual configurations. 

<h1>Running the code</h1>
An EC2 instance is required with a pre-configured MySQL server running with access allowed to all traffic (this can be done by changing the ```bind-address``` parameter in the file ```/etc/mysql/mysql.conf.d/mysqld.cnf``` to **0.0.0.0**). A FTP server is also required to allow for the SFTP transactions to take place, which can be done by running ```sudo apt-install vsftpd``` and editing the ```/etc/vsftpd.conf``` file by adding 
```
pasv_enable=YES
pasv_max_port=2048
pasv_min_port=1024
pasv_addres *EC2 Public IPv4*
```
ensure that the EC2 instance allows traffic through the neccersary ports (**20-22**, **1024-2048** and **3306**) and that the inbound rules allow a connection from any IP address, which can be done both during and after creating of the EC2 server.









