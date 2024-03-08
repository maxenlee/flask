from flask import Flask, request, jsonify
import pandas as pd
import textblob
from textblob import TextBlob
import pickle
import nltk

nltk.download('omw-1.4')

app = Flask(__name__)


def pickle_blobber(series):
    # TextBlob(series)
    blobber = series.apply(TextBlob)
    blobber.apply(lambda x: x.words)

    # blobber.apply(lambda x: [x.singularize() for x in x.words])

    # word = blobber.apply(lambda tb: ' '.join())
    # with open('word_pickle.p', 'wb') as f:
    #     pickle.dump(word_pickle, f)
    return "Processed and pickled successfully."


@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    text_series = pd.Series(data['texts'])
    response_message = pickle_blobber(text_series)
    return jsonify({'message': response_message})


if __name__ == '__main__':
    app.run(debug=True)
