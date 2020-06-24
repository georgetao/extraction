import sys
import os
import numpy
sys.path.append(os.path.abspath('models'))
import preprocess
from nltk import sent_tokenize
import fasttext

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html', len=0, pred=0, r=0)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    email = request.form['email_text']
    def preprocess_text(text):
        text = sent_tokenize(email)
        out = []
        for sentence in text:
            if type(sentence) == str:
                # clean text
                clean = preprocess.clean(sentence)
                # clean info
                clean = preprocess.clean_info(clean)

                out.append(clean)
            else:
                out.append("")
        return out
    # process text
    sentences = preprocess_text(email)

    # load fasttest model
    ft_model = fasttext.load_model("models/best_ft_model.bin")

    # classify sentences
    t = []

    for sentence in sentences:
        t.append({"sentence": sentence,
            "label": ft_model.predict(sentence)[0][0],
            "certainty": round(ft_model.predict(sentence)[1][0], 2)})
    
    #prediction = [sentence + ": " + ft_model.predict(sentence)[0][0] for sentence in sentences]
    reqs = [sentence for sentence in sentences if "1" in ft_model.predict(sentence)[0][0]]
    
    # output results
    return render_template('index.html', len=len(t), pred=t, r=reqs)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)