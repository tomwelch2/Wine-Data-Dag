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

An EC2 instance is required with a pre-configured MySQL server running with access allowed to all traffic (this can be done by changing the ```bind-address``` parameter in the file ```/etc/mysql/mysql.conf.d/mysqld.cnf``` to **0.0.0.0**). A FTP server is also required to allow for the SFTP transactions to take place, which can be done by running ```sudo apt install vsftpd``` and editing the ```/etc/vsftpd.conf``` file by adding 

```
pasv_enable=YES
pasv_max_port=2048
pasv_min_port=1024
pasv_addres *EC2 Public IPv4*
```

ensure that the EC2 instance allows traffic through the neccersary ports (**20-22**, **1024-2048** and **3306**) and that the inbound rules allow a connection from any IP address, which can be done both during and after creating of the EC2 server. 

Once you have edited the ```docker-compose.yml``` file to point towards your specific configuration, run ```docker-compose up --build``` to run the code and visit ```0.0.0.0:8080``` in your browser to view the Airflow UI where the DAG can be triggered and monitored.

<h1>Technologies Used</h1>

The ETL pipeline is orchastrated using Airflow, an easy to use workflow scheduler that uses DAGS to run events. Airflow supports custom operaters which can be written in Python, making its operation very flexible and means pipelines can have tailor-made operators that adapt to business logic and the individual requirements of clients. 

Pyspark was used as the processing framework used to join and clean the datasets in question, due to its ability to work with larger-than-memory datasets and its ability to run on a Hadoop cluster using YARN. Although the size of the data in this particular project is a lot less than what can fit in memory, it is a good demonstration of how a tool like Spark can be used to work with larger datasets which Pandas is not suitable to handle - plus its MySQL JDBC connectors mean that loading the data from the program to the DB is simple.

Redis was utilised as a messaging-service of sorts to allow data to be accessed by all the stages in the ETL pipeline, providing intermediary storage that is overwritten every time a stage is complete. RabbitMQ or even Kafka was considered here, but the size of the data paired with the fact that setting up a Redis instance with docker requires around 1/3 of the code required for Kafka meant that utilising these tools in this project would have been a waste. 

In terms of DB storage, MySQL was used as it is, in my opinion, the easiest database to work with that offers good functionality and little configuration out of the box to work in a setup like this. Postgres was also considered, but the volume of the data meant that once again this would have been wasted - despite Postgres' significantly fast write speeds. 





