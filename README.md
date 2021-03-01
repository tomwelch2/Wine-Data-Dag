# Wine-Data-Dag

![alt text](https://welpmagazine.com/wp-content/uploads/2020/11/image.jpg)

<h1>Wine-Data Airflow DAG</h2>
<br>
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


