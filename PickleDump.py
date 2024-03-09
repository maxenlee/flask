import boto3
import os
import pandas as pd
import pickle
import io
from textblob import TextBlob
from tqdm import tqdm
from datetime import datetime

def process_and_upload_csv_in_chunks(url, chunksize=10000, folder_name='processed_chunks'):
    access_key = os.getenv('PICKLEJAR_ACCESS')
    secret_key = os.getenv('PICKLEJAR_SECRET')
    
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='nyc3',
                            endpoint_url='https://nyc3.digitaloceanspaces.com',
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key)
    bucket_name = 'picklejar'  # Replace with your actual bucket name
    
    # Optionally, include a timestamp in the folder name for unique folder creation each run
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    unique_folder_name = f"{folder_name}/{timestamp}"

    total_size = sum(1 for _ in pd.read_csv(url, chunksize=chunksize))
    progress_bar = tqdm(total=total_size, desc='Uploading Chunks')
    
    for i, chunk in enumerate(pd.read_csv(url, chunksize=chunksize)):
        processed_chunk = chunk['text'].apply(lambda x: ' '.join([word.singularize() for word in TextBlob(x).words]))
        
        pickled_data = pickle.dumps(processed_chunk)
        
        with io.BytesIO(pickled_data) as f:
            # Include the folder name in the object path
            object_name = f'{unique_folder_name}/word_pickle_part_{i}.p'
            
            client.upload_fileobj(f, bucket_name, object_name)
            progress_bar.update(1)
    
    progress_bar.close()
    return f"All chunks processed and uploaded successfully to {unique_folder_name}."

# Before running the function, ensure that 'PICKLEJAR_ACCESS' and 'PICKLEJAR_SECRET' are set in your environment variables.


# Note: Before running the function, ensure that 'PICKLEJAR_ACCESS' and 'PICKLEJAR_SECRET' are set in your environment variables.
# Example usage:
process_and_upload_csv_in_chunks(url='https://ddc-datascience.s3.amazonaws.com/Projects/Project.5-NLP/Data/NLP.csv')
