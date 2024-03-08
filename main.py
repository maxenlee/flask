import boto3
import os
from flask import Flask, request, jsonify
import pandas as pd
from textblob import TextBlob
import pickle
import io

def create_app():
    app = Flask(__name__)

    def pickle_blobber(series):
        # Convert series to TextBlob, process, and pickle
        word_pickle = series.apply(lambda x: TextBlob(x)).apply(lambda tb: ' '.join([word.singularize() for word in tb.words]))
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
        data = request.get_json()
        text_series = pd.Series(data['texts'])
        response_message = pickle_blobber(text_series)
        return jsonify({'message': response_message})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

