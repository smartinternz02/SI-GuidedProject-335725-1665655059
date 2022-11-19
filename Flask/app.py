from flask import Flask, render_template, request
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest
# from nltk. import punctuation

app = Flask(__name__)


@app.route("/")
def about():
    return render_template('home.html')


@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/summarize")
def home1():
    return render_template('summarize.html')


@app.route("/submit")
def home2():
    return render_template('submit.html')


@app.route("/summary", methods=['POST'])
def summary():
    stopWords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = request.form['text']
    print(doc)
    docs = nlp(doc)
    tokens = [i.text for i in docs]
    punctuation = '!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~\n'
    print(punctuation)
    word_frequencies = {}
    for word in docs:
        if word.text.lower() not in stopWords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    maxFrequency = max(word_frequencies.values())
    for i in word_frequencies.keys():
        word_frequencies[i] = word_frequencies[i] / maxFrequency
    sent_tokenz = [sent for sent in docs.sents]
    sentence_score = {}
    for sent in sent_tokenz:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_score.keys():
                    sentence_score[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_score[sent] += word_frequencies[word.text.lower()]
    select_len = int(len(sent_tokenz) * 0.3)
    summary = nlargest(select_len, sentence_score, sentence_score.get)
    summary = [word.text for word in summary]
    summary = " ".join(summary)
    return render_template('submit.html', predictionText=summary)


if __name__ == "__main__":
    app.run(debug=True)
