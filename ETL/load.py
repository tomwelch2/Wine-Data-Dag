import findspark
import json
import redis
import os
from pyspark.sql import SparkSession

"""Script takes data from Redis and loads it into Spark, where JDBC is used to move data to
   MySQL instance hosted on EC2"""


findspark.add_packages("mysql:mysql-connector-java:8.0.11") #Adding MySQL driver to Spark


#retrieving data from Redis ---

r = redis.Redis(host = "redis", port = 6379)

data = json.loads(r.get("wine_data").decode("utf8"))

#reading data into Spark ---

spark = SparkSession.builder.appName("pipeline").getOrCreate()

with open("/usr/local/airflow/dags/ETL/schema.txt", "r") as f:
    SCHEMA = f.read()

df = spark.createDataFrame(data, schema = SCHEMA)

#Writing data to MySQL ---

user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
db = os.environ.get("MYSQL_DB")
db_table = os.environ.get("MYSQL_DB_TABLE")
host = os.environ.get("MYSQL_HOST")

JDBC_URL = "jdbc:mysql://{0}:3306/{1}".format(host, db)

driver = "com.mysql.jdbc.Driver"

df.write.format("jdbc") \
        .option("url", JDBC_URL) \
        .option("driver", driver) \
        .option("password", password) \
        .option("user", user) \
        .option("dbtable", db_table).save()


