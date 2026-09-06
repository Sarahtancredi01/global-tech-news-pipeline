import json
import pandas as pd
import requests
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

RAW_DATA = '/tmp/raw_news.json'
CLEAN_DATA = '/tmp/tech_news.csv'
BUCKET = 'tech-news-data-lake'

# TASK 1: EXTRACT
def extract_news():
    ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    ids = requests.get(ids_url).json()[:20]
    
    details = []
    for s_id in ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
        details.append(requests.get(item_url).json())
    
    with open(RAW_DATA, 'w') as f:
        json.dump(details, f)

# TASK 2: TRANSFORM
def transform_news():
    with open(RAW_DATA, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)[['title', 'by', 'score', 'url', 'time']]
    df.columns = ['title', 'author', 'score', 'url', 'created_time']
    df['created_time'] = pd.to_datetime(df['created_time'], unit='s')

    # BONUS: Category Tagging
    def tag_it(title):
        t = str(title).upper()
        if 'AI' in t: return 'AI'
        if 'CLOUD' in t: return 'Cloud'
        if 'STARTUP' in t: return 'Startup'
        if 'SECURITY' in t: return 'Security'
        return 'General'
    df['category'] = df['title'].apply(tag_it)
    
    # BONUS: Trending Story Log
    top = df.loc[df['score'].idxmax()]
    print(f"🏆 Top Story: {top['title']} ({top['score']} points)")
    
    df.to_csv(CLEAN_DATA, index=False)

# TASK 3: LOAD TO S3
def load_news():
    hook = S3Hook(aws_conn_id='aws_default')
    now = datetime.now()
    # BONUS: Partitioned Storage
    s3_path = f"news/year={now.year}/month={now.strftime('%m')}/day={now.strftime('%d')}/tech_news.csv"
    
    hook.load_file(filename=CLEAN_DATA, key=s3_path, bucket_name=BUCKET, replace=True)

# DAG DEFINITION
with DAG('global_tech_news_pipeline', start_date=datetime(2026, 3, 1), schedule_interval='@daily', catchup=False) as dag:
    t1 = PythonOperator(task_id='extract', python_callable=extract_news)
    t2 = PythonOperator(task_id='transform', python_callable=transform_news)
    t3 = PythonOperator(task_id='load', python_callable=load_news)

    t1 >> t2 >> t3