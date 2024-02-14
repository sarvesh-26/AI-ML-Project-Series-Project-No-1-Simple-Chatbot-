import random
import json
import pickle
import numpy as np
import nltk

from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents_data = json.loads(open('intents.json').read())

word_list = pickle.load(open('words.pkl', 'rb'))
class_list = pickle.load(open('classes.pkl', 'rb'))
chat_model = load_model('chatbot_model.h5')

def preprocess_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def create_bag_of_words(sentence):
    sentence_words = preprocess_sentence(sentence)
    bag = [0] * len(word_list)
    for w in sentence_words:
        for i, word in enumerate(word_list):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_intent(sentence):
    bow = create_bag_of_words(sentence)
    res = chat_model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': class_list[r[0]], 'probability': str(r[1])})
    return return_list

def get_chatbot_response(intents_list, intents_data):
    tag = intents_list[0]['intent']
    list_of_intents = intents_data['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("Let's chat!")
print("How can I assist you today?")

while True:
    message = input("")
    predicted_intents = predict_intent(message)
    response = get_chatbot_response(predicted_intents, intents_data)
    print(response)
