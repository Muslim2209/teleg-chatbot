import random
import string
import warnings

import nltk
import telebot
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from variables import TOKEN
from actions import (add_to_unallowed,
                     check_to_bad,
                     DEBUG)

warnings.filterwarnings('ignore')
bot = telebot.TeleBot(TOKEN)

# nltk.download('popular', quiet=True)  # for downloading packages

# uncomment the following only the first time
# nltk.download('punkt') # first-time use only
# nltk.download('wordnet') # first-time use only


# Reading in the corpus
with open('chatbot.txt', 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()

# TOkenisation
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]


def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        robo_response = robo_response + "I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response


@bot.message_handler(content_types=['text'])
def message_handler(message):
    user_response = message.text
    user_response = user_response.lower()
    if user_response == 'thanks' or user_response == 'thank you':
        bot.send_message(message.chat.id, "You are welcome!")
    else:
        if greeting(user_response) is not None:
            bot.send_message(message.chat.id, greeting(user_response))
        else:
            bot.send_message(message.chat.id, response(user_response))
            sent_tokens.remove(user_response)


@bot.message_handler(content_types=['sticker', 'document', 'gif'])
def sticker_handler(message):
    if message.content_type == 'sticker':
        if check_to_bad(message.sticker.file_id):
            bot.send_message(message.chat.id, 'Uyatsiz narsala tashamela!')
        elif DEBUG:
            add_to_unallowed(message.sticker.file_id)
        else:
            bot.send_message(message.chat.id, message.sticker.emoji)
    if message.content_type == 'document':
        if check_to_bad(message.document.file_id):
            bot.send_message(message.chat.id, 'Koksal tashama, Koksal!')
        elif DEBUG:
            add_to_unallowed(message.document.file_id)
        else:
            bot.send_message(message.chat.id, message.from_user.username+'dan ajoyib GIF!')


if __name__ == '__main__':
    bot.polling(none_stop=True)
