# load model
# copy hàm của Thư qua
# viết hàm chatbot => answer

import re
import numpy as np
import pickle
import keras
import pandas as pd
from underthesea import word_tokenize 
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences

#Lấy ra các model
enc_model = keras.models.load_model("./enc_model.h5")
dec_model =  keras.models.load_model("./dec_model.h5")
tokenizer_word_index = pickle.load(open('tokenizer_word_index.sav','rb'))
maxlen_answers = pickle.load(open('maxlen_answers.sav','rb'))

maxlen_questions = 15

# hàm để xóa các ký tự đặc biệt
def clean_text(sent):
    return re.sub(r'[!“”"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]', '', sent)

# hàm để chuyển Word Segmentation cho tiếng Việt
def clean_and_word_segmentation(sent):
    return word_tokenize(clean_text(sent.lower()), format='text')

def str_to_tokens(sentence):
    #words = sentence.lower().split()
    words = clean_and_word_segmentation(sentence).split()
    tokens_list = list()
    for current_word in words:
        result = tokenizer_word_index[current_word]
        if result != '':
            tokens_list.append(result)
    return pad_sequences([tokens_list], maxlen=maxlen_questions,padding='post')

def chatbot(input):
    input_question = input

    if input_question == '':
        return 'Give for me your question'
    states_values = enc_model.predict(str_to_tokens(input_question))
    empty_target_seq = np.zeros((1,1))
    empty_target_seq[0,0] = tokenizer_word_index['<START>']
    stop_condition = False
    decoded_translation = ''
    while not stop_condition:
        dec_outputs, h, c = dec_model.predict([empty_target_seq]+states_values)
        sampled_word_index = np.argmax(dec_outputs[0,-1, :])
        sampled_word = None
        for word, index in tokenizer_word_index.items():
            if sampled_word_index == index:
                if word != '<END>':
                    decoded_translation += f'{word} '
                sampled_word = word

        if sampled_word == '<END>' or len(decoded_translation.split()) > maxlen_answers:
            stop_condition = True
        empty_target_seq = np.zeros((1,1))
        empty_target_seq[0,0] = sampled_word_index
        states_values = [h,c]
    print('User: ',input_question)
    print('Bot answer:', decoded_translation, '\n')
    return decoded_translation