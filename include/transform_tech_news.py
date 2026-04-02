import pandas as pd
import boto3
import os
from dotenv import load_dotenv  

# Load the keys from your .env file
load_dotenv()

def transform_and_upload():
    # 1. Load the local data
    # We use os.path to make sure it finds the file regardless of how you run the script
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'extracted_news.csv')
    
    if not os.path.exists(file_path):
        print(f"ERROR: Could not find {file_path}. Did you run the extraction script first?")
        return

    df = pd.read_csv(file_path)
    
    # 2. Simple Transformation
    df_clean = df.dropna()
    
    # 3. Connect to S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name='eu-north-1'  # Stockholm region
    )
    
    # 4. Upload to your bucket
    bucket_name = 'global-tech-news-bucket-882856017211'
    file_name = 'tech_news_transformed.csv'
    
    # Convert dataframe back to CSV string for the upload
    csv_buffer = df_clean.to_csv(index=False)
    
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer)
    print(f"--- SUCCESS: Uploaded to S3 bucket: {bucket_name} ---")

if __name__ == "__main__":
    transform_and_upload()