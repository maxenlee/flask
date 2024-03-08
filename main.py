from flask import Flask, request, jsonify
import pandas as pd
import textblob
from textblob import TextBlob
import pickle
import nltk

nltk.download('omw-1.4')

def create_app():
    app = Flask(__name__)

    def pickle_blobber(series):
        word_pickle = series.apply(lambda x: TextBlob(x)).apply(lambda tb: ' '.join([word.singularize() for word in tb.words]))
        with open('word_pickle.p', 'wb') as f:
            pickle.dump(word_pickle, f)
        return "Processed and pickled successfully."

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
