import os
import sys
from operator import itemgetter
from time import sleep

import nltk
import random
import string
from colorama import init, Fore
from gtts import gTTS
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer

init()

# from engine import Engine
name = ''
list_query = []
dict_collections = {}

dict_collections['mt'] = 'mountain'
dict_collections['mountain'] = 'mountain'
dict_collections['mountains'] = 'mountain'
dict_collections['city'] = 'cities'
dict_collections['cities'] = 'cities'
dict_collections['state'] = 'state'
dict_collections['st'] = 'state'
dict_collections['lake'] = 'lake'
dict_collections['river'] = 'river'
dict_collections['rivers'] = 'river'
goodbyes = [
    "Thank you for talking with me.",
    "Good-bye.",
    "Thank you, that will be $150.  Have a good day!"]
choices = ["I see. ," + name,
           "Very interesting. " + name,
           "...Let me think " + name,
           ".....Gimme a second " + name,
           "Lemme find it out for you " + name]

alternative = ["Sorry, could not found this. " + name,
               "I dont have answer to this question. " + name,
               "Well, this is out of my range. " + name,
               "Sorry " + name + "! Could not find the exact location.",
               name + ",Don't you think California is a better place to search for.",
               "Not Found. " + name + " Please ask for something else.",
               "Not a cool place, please search for any other place."]

db = ''
corpus = []
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
similarity = {}
refined_corpus = {}
myscreen = ''


def print_color(words):
    words = Fore.RED + words + Fore.RESET
    for char in words:
        sleep(0.05)
        sys.stdout.write(char)
        sys.stdout.flush()


def speak(audioString, notprint):
    if notprint:
        print_color("\t\t\t\t" + audioString + '\n')
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3 >/dev/null 2>&1")


def ask(sentence):
    tts = gTTS(text=sentence, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3 >/dev/null 2>&1")
    name = raw_input("\t\t\t\t" + sentence + '\n' + '\t\t\t\t>>>>>')
    return name


def setup():
    global db, myscreen
    server = 'ds049436.mlab.com:49436'
    port = 41939
    db_name = 'nlp_team'
    username = 'nlp'
    password = 'nlp'

    # connect to server
    conn = MongoClient(server, port)

    # Get the database
    db = conn[db_name]

    # Have to authenticate to get access
    db.authenticate(username, password)


def question_processing(ques):
    global corpus, name, list_query
    list_query = []
    # corpus=[]
    speak(random.choice(choices) + ' ' + name, False)
    # Step1: Generate all tokens
    tokens = nltk.word_tokenize(ques)
    # Step2: Part of Speech tagging of the question
    pos_tags = nltk.pos_tag(tokens)
    # Step3: Named Entity Recoginition of the POS Tags
    pos_tree = nltk.ne_chunk(pos_tags)

    # filter all query words
    for i in pos_tags:
        if i[1] == 'NNP' or i[1] == 'NN' or i[1] == 'JJ' or i[1] == 'JJS' or i[1] == 'NNS' or i[1] == 'VBZ' or i[
            1] == 'RBS':
            list_query.append(i[0])
    # list_query)

    collection_name = []

    # Get the Matching List of Collection(DBs) where the answer could be.
    for i in list_query:
        if dict_collections.get(i.lower()):
            collection_name.append(dict_collections[i.lower()])

    # print(collection_name)

    # Aggerate all the Documents from the list of Collections
    db.cursor = db.questions.find()
    corpus = []
    for i in db.cursor:
        for t in collection_name:
            if t in i:
                corpus.append(i[t])

                # print("corpus--->", corpus)


# Using Porter Stemmer for Stemming Tokens

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


# remove punctuation, lowercase, stem

def normalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punctuation_map))


# find the cosine Similarity between text1 and text2
def cosine_sim(text1, text2):
    # Convert a collection of raw documents to a matrix of TF-IDF features.
    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]


def find_similartiy():
    global list_query
    refined_corpus.clear()

    # refine the corpus for all the matched query words
    for text in corpus:
        for document in text:
            l = [item.lower() for item in document.split()]
            list_query = [item.lower() for item in list_query]
            t = len(set(l) & set(list_query))
            if t > 0:
                refined_corpus[document] = t
    # sort them by maximum count
    sorted(refined_corpus.items(), key=itemgetter(1), reverse=True)

    if not bool(refined_corpus):
        speak(random.choice(alternative), True)
        return
    # find the maximum match count
    max_count = max(refined_corpus.items(), key=itemgetter(1))[1]

    count = 0
    similarity.clear()
    for document in refined_corpus:
        l = refined_corpus[document]
        if l == max_count:
            count += 1
        similarity[document] = cosine_sim(document, str(list_query)) * l

    # print(sorted(similarity.items(), key=itemgetter(1), reverse=True))

    listx = []
    listy = []
    keys = []

    for key, value in sorted(similarity.items(), key=itemgetter(1), reverse=True):
        keys.append(key)
        listx.append(value)
        listy.append(1)
    # print keys
    if max_count > 1:
        sayVal = str(keys[:count][0])
        # print("FINAL RESULT---->", sayVal)
        speak(sayVal, True)
    else:
        # print("FINAL RESULT::: else---->", keys[0])
        speak(keys[0], True)
    return


def main():
    os.system('clear')
    global list_query, name
    print_color("\t\t\t\t\t\t\t\tLexis\n")
    for i in range(8):
        print("\t\t\t\t" + '=' * 72)
    print("\t\t\t\t" + '=' * 72)
    setup()
    speak('My name is Lexis !', True)
    name = ask('What is your Name?')
    speak('Hello ' + name + ' !', True)
    speak('I am the bot that helps you with all your queries related to Geography!', True)
    speak("Talk to me by typing plain English.", True)
    speak('Ask me about Cities', True)
    speak('Or States', True)
    speak('Or Rivers', True)
    speak('Or Mountains in USA', True)
    print("\t\t\t\t" + '=' * 72)
    speak('To Kill me, type BYE!', True)
    for i in range(3):
        print("\t\t\t\t" + '=' * 72)
    user_input = ask(name + ', What would you like to ask me?')
    while True:
        question_processing(user_input)
        find_similartiy()
        user_input = ask(name + ' , What more would you like to ask me?')
        if user_input == 'BYE' or user_input == 'bye':
            break
    speak(random.choice(goodbyes), True)


main()
