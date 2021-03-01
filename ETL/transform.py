import pyspark.sql.functions as sql
import os
import boto3
import json
import redis
from pyspark.sql import SparkSession

#Retrieving AWS Credentials ---

ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.environ.get("AWS_DEFAULT_REGION")
BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
#Connecting to S3 ---

S3 = boto3.client(
            service_name = "s3",
            aws_access_key_id = ACCESS_KEY,
            aws_secret_access_key = SECRET_KEY,
            region_name = REGION_NAME
        )


#Pulling data from S3 ---

def pull_from_S3(filename: str, bucket: str):
    with open(filename, "wb") as f:
        S3.download_fileobj(bucket, filename, filename)

wine_csv_1 = pull_from_S3(filename = "wine_csv_1.csv", bucket = BUCKET_NAME)
wine_csv_2 = pull_from_S3(filename = "wine_csv_2.csv", bucket = BUCKET_NAME)
wine_json = pull_from_S3(filename = "wine_json.json", bucket = BUCKET_NAME)

#reading data into dataframes ---

with open("/usr/local/airflow/dags/ETL/schema.txt", "r") as f:
    SCHEMA = f.read()

spark = SparkSession.builder.appName("pipeline").getOrCreate()

wine_df_1 = spark.read.csv("wine_csv_1.csv", header = True, schema = SCHEMA)

wine_df_2 = spark.read.csv("wine_csv_2.csv", header = True, schema = SCHEMA)

wine_df_3 = spark.read.json("wine_json.json", schema = SCHEMA)

#Union Dataframes to create one large dataset ---

df = wine_df_1.union(wine_df_2, wine_df_3)

df = df.dropna() #Dropping rows with NULL values to create clean dataset

df = spark.sql("""SELECT country, description, points, price, province, region_1,
                  region_2, taster_name, taster_twitter_handle, title, variety, winery,
                  COUNT(*) OVER (PARTITION BY variety) AS num_wines_of_variety""")



df = df.rdd.map(lambda row: row.asDict()).collect()

df = json.dumps(df)

#Loading data into Redis ---

r = redis.Redis(host = "redis", port = 6379)

r.set("wine_data", df)
