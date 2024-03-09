import boto3
import os
from flask import Flask, request, jsonify
import pandas as pd
from textblob import TextBlob
import pickle
import io

app = Flask(__name__)

def divide_chunks(data_list, chunk_size):
    """Yield successive chunk_size chunks from data_list."""
    for i in range(0, len(data_list), chunk_size):
        yield data_list[i:i + chunk_size]

def pickle_blobber(text_series):
    """Convert series to TextBlob, process, pickle, and upload to cloud storage."""
    word_pickle = text_series.apply(lambda x: TextBlob(x)).apply(lambda tb: ' '.join([word.singularize() for word in tb.words]))
    pickled_data = pickle.dumps(word_pickle)
    
    # Access the secret (e.g., API keys) from environment variables
    access_key = os.getenv('PICKLEJAR_ACCESS')
    secret_key = os.getenv('PICKLEJAR_SECRET')
    
    # Configure boto3 client
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='nyc3',  # Example region
                            endpoint_url='https://picklejar.nyc3.digitaloceanspaces.com',  # Example endpoint
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key)
    
    # Create an in-memory file
    with io.BytesIO(pickled_data) as f:
        # Upload to DigitalOcean Spaces
        client.upload_fileobj(f, 'your-bucket-name', 'word_pickle.p')
    
    return "Processed and pickled successfully, uploaded to Spaces."

@app.route('/process_text', methods=['POST'])
def process_text():
    """Process text by dividing into chunks and sending each to be pickled and uploaded."""
    data = request.get_json()
    large_text_list = data['texts']
    chunk_size = 100  # Adjust chunk_size based on your needs

    # Divide the large list into chunks and process each chunk
    for chunk in divide_chunks(large_text_list, chunk_size):
        text_series = pd.Series(chunk)
        response_message = pickle_blobber(text_series)
        # Here, you could also track the status of each chunk or implement additional logic
        
    return jsonify({'message': response_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)