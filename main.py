#imports
#nlp imports
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras import models
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
#flask imports
from flask import Flask, render_template, request
app = Flask(__name__)

class Backend():
    def __init__(self):
        #pre processing
        self.tokenizer = Tokenizer()
        #data = open('../../../../../Cooleg Extra/CSE4022/stories.txt', encoding='utf-8').read() #to fix
        ## TODO this will need to be adjusted for whichever dataset is needed, and the following lines would need to be fixed
        corpus = data.lower().split("\n")
        self.tokenizer.fit_on_texts(corpus)
        total_words = len(self.tokenizer.word_index) + 1
        self.new_model = models.load_model('saved_model/mainmodel')

    def process(self, seed_text, next_words):

        # seed_text = input("Input String: ")
        # next_words = int(input("Number of words: "))
        for _ in range(next_words):
            token_list = self.tokenizer.texts_to_sequences([seed_text])[0]
            token_list = pad_sequences([token_list], maxlen=87, padding='pre') #hard coded to 87, based on model    
            predicted = self.new_model.predict(token_list)
            output_word = ""
            for word, index in self.tokenizer.word_index.items():
                if index == np.argmax(predicted):
                    output_word = word
                    break
            seed_text += " " + output_word
        
        return seed_text


@app.route('/')
def main():
    return render_template('./index.html', input = "", output = "")

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        # print(dict(result))
        inputText = result["inputText"]
        if result["WordCount"] == "single":
            count = 1
        else:
            count = int(result["wordNumber"])
    global obj
    return render_template('./index.html', input = inputText, output = obj.process(inputText, count))
    # return render_template('./index.html', input = "", output = "")

obj = Backend()


if __name__ == '__main__':
    app.run()
