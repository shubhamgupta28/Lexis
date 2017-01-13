import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn
import re
from pymongo import MongoClient
import math
from operator import itemgetter
import sys
import operator

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


# Statements to be made for mountains
# number of mountains in state X are 20
# mountains in state X are [A,B,C]
#
# highest mountain in state X is A
#
# lowest mountain in state Y is B


# ===============================================================================================================
# Mountain
# ===============================================================================================================


list_ques_mountain = []

list_a = []
list_b = []
list_c = []
max_counter = -10000
min_counter = 10000
max_alaska = -10000
min_alaska = 10000
max_colorado = -10000
min_colorado = 10000
max_california = -10000
min_california = 10000

max_counter_name = ''
min_counter_name = ''
max_alaska_name = ''
min_alaska_name = ''
max_colorado_name = ''
min_colorado_name = ''
max_california_name = ''
min_california_name = ''

db.cursor = db.mountain.find()
for i in db.cursor:
    # print(i)

    # Add the highest peak state wise by declaring a varibale speartely for easch state
    if i['state'] == 'alaska':
        list_a.append(i['mountain_name'][0].title())
        if int(max_alaska) < int(i['mountain_name'][1]):
            max_alaska = i['mountain_name'][1]
            max_alaska_name = i['mountain_name'][0].title()
        if int(min_alaska) > int(i['mountain_name'][1]):
            min_alaska = i['mountain_name'][1]
            min_alaska_name = i['mountain_name'][0].title()

    elif i['state'] == 'colorado':
        list_b.append(i['mountain_name'][0].title())
        if int(max_colorado) < int(i['mountain_name'][1]):
            max_colorado = i['mountain_name'][1]
            max_colorado_name = i['mountain_name'][0].title()
        if int(min_colorado) > int(i['mountain_name'][1]):
            min_colorado = i['mountain_name'][1]
            min_colorado_name = i['mountain_name'][0].title()

    elif i['state'] == 'california':
        list_c.append(i['mountain_name'][0].title())
        if int(max_california) < int(i['mountain_name'][1]):
            max_california = i['mountain_name'][1]
            max_california_name = i['mountain_name'][0].title()

        if int(min_california) > int(i['mountain_name'][1]):
            min_california = i['mountain_name'][1]
            min_california_name = i['mountain_name'][0].title()

    if int(max_counter) < int(i['mountain_name'][1]):
        max_counter = i['mountain_name'][1]
        max_counter_name = i['mountain_name'][0].title()

    if int(min_counter) > int(i['mountain_name'][1]):
        min_counter = i['mountain_name'][1]
        min_counter_name = i['mountain_name'][0].title()

    list_ques_mountain.append('The height of mountain ' + i['mountain_name'][0].title() + ' is ' + i['mountain_name'][1] + ' meters')
    list_ques_mountain.append('mountain ' + i['mountain_name'][0].title() + ' is in the state ' + i['state'].title())

mountain_list_a = ' , '.join(list_a)
mountain_list_b = ' , '.join(list_b)
mountain_list_c = ' , '.join(list_c)
list_ques_mountain.append('mountains in state Alaska are ' + mountain_list_a)
list_ques_mountain.append('mountains in state Colorado are ' + mountain_list_b)
list_ques_mountain.append('mountains in state California are ' + mountain_list_c)
list_ques_mountain.append('The highest mountain in Usa is ' + max_counter_name + ' which is ' + max_counter + ' meters')
list_ques_mountain.append('The lowest mountain in Usa is ' + min_counter_name + ' which is ' + min_counter + ' meters')
list_ques_mountain.append('The highest mountain in US is ' + max_counter_name + ' which is ' + max_counter + ' meters')
list_ques_mountain.append('The lowest mountain in US is ' + min_counter_name + ' which is ' + min_counter + ' meters')
list_ques_mountain.append('The highest mountain in America is ' + max_counter_name + ' which is ' + max_counter + ' meters')
list_ques_mountain.append('The lowest mountain in America is ' + min_counter_name + ' which is ' + min_counter + ' meters')
list_ques_mountain.append('The highest mountain in state Alaska is ' + max_alaska_name + ' which is ' + max_alaska + ' meters')
list_ques_mountain.append('The lowest mountain in state Alaska is ' + min_alaska_name + ' which is ' + min_alaska + ' meters')
list_ques_mountain.append('The highest mountain in state Colorado is ' + max_colorado_name + ' which is ' + max_colorado + ' meters')
list_ques_mountain.append('The lowest mountain in state Colorado is ' + min_colorado_name + ' which is ' + min_colorado + ' meters')
list_ques_mountain.append('The highest mountain in state California is ' + max_california_name + ' which is ' + max_california + ' meters')
list_ques_mountain.append('the lowest mountain in state California is ' + min_california_name + ' which is ' + min_california + ' meters')


# print(list_ques_mountain)

# To insert a new collection called mountain_question
# db.questions.insert({'mountain': list_ques_mountain})


# ===============================================================================================================
# Mountain - END
# ===============================================================================================================




# ===============================================================================================================
# States
# ===============================================================================================================
#     the area of state alabama is x
#     the state alabama is x m2 large
#     the state alabama is X metres  big

    # the population of state alabama is x
    # x number of poeple live in alabama
    # the state aalabam has X number of people

# the capital of state alabama is X
# the state number of Alabama is 2
# the state code of Alabama is 2
# the state alabama has A,B,C cities
# a is the most poplu state
# a is the most poplu state in usa
# a is the least popu state
#     the area, code, capital, cities of the most popula state

list_ques_states = []
max_popu = 0
least_popu = 92233720
popu_dict = {}

list_temp = []

db.cursor = db.state.find()
for i in db.cursor:
    # print(i)
    curr_state = i['name']

    # Area
    str1 = 'The area of ' + curr_state.title() + ' is ' + str(format(int(float(i['area'])), ",d")) + ' square meters'
    str2 = 'The state ' + curr_state.title() + ' is ' + str(format(int(float(i['area'])), ",d")) + ' square meters big'
    str3 = 'The state ' + curr_state.title() + ' is ' + str(format(int(float(i['area'])), ",d")) + ' square meters large'
    list_ques_states.append(str1)
    list_ques_states.append(str2)
    list_ques_states.append(str3)

    # Population
    str4 = 'The population of state ' + curr_state.title() + ' is ' + str(format(int(float(i['population'])), ",d"))
    str5 = str(format(int(float(i['population'])), ",d")) + ' number of people live in ' + curr_state.title()
    str6 = 'The state ' + curr_state.title() + ' has ' + str(format(int(float(i['population'])), ",d")) + ' number of people'
    list_ques_states.append(str4)
    list_ques_states.append(str5)
    list_ques_states.append(str6)

    # the capital of state alabama is X
    str7 = 'The capital of state ' + curr_state.title() + ' is ' + i['captial'].title()
    list_ques_states.append(str7)

    # the state number of Alabama is 2
    str8 = 'The state number of state ' + curr_state.title() + ' is ' + i['state_number']
    list_ques_states.append(str8)

    # the state code of Alabama is 2
    # str9 = 'The state code of state ' + curr_state.title() + ' is ' + i['state_number']
    # list_ques_states.append(str9)


    # the most poplu state
    # the leats popu state
    popu_dict[curr_state.title()] = i['population']

    if curr_state == 'florida':
        str10 = 'The capital of most populous state is ' + i['captial'].title()
        str10A = 'The capital of most populous state in USA is ' + i['captial'].title()
        str11 = 'The cities present in the most populous state are ' + ', '.join(i['cities']).title()
        str12 = ', '.join(i['cities']).title() + ' cities are present in the most populous state'
        str13 = 'The area of the most populous state is ' + str(format(int(float(i['area'])), ",d")) + ' square meters'
        str14 = 'The state number of the most populous state is ' + i['state_number']

        list_ques_states.append(str10)
        list_ques_states.append(str11)
        list_ques_states.append(str12)
        list_ques_states.append(str13)
        list_ques_states.append(str14)

    if curr_state == 'ohio':
        str15 = 'The capital of least populous state is ' + i['captial'].title()
        str15A = 'The capital of least populous state in USA is ' + i['captial'].title()
        str16 = 'The cities present in the least populous state are ' + ', '.join(i['cities']).title()
        str17 = ', '.join(i['cities']).title() + ' cities are present in the least populous state'
        str18 = 'The area of the least populous state is ' + str(float(i['area'])) + ' square meters'
        str19 = 'The state number of the least populous state is ' + i['state_number']

        list_ques_states.append(str15)
        list_ques_states.append(str15A)
        list_ques_states.append(str16)
        list_ques_states.append(str17)
        list_ques_states.append(str18)
        list_ques_states.append(str19)


    # TODO rest of the ques writetn above
str20 = 'The most populous state is Florida'
str21 = 'The least populous state is Ohio'
str22 = 'The most populous state in USA is Florida'
str23 = 'The least populous state in USA is Ohio'
list_ques_states.append(str20)
list_ques_states.append(str21)
list_ques_states.append(str22)
list_ques_states.append(str23)

# print('sdfghsdfghj', list_ques_states)

# To insert a new collection called state_question
# db.questions.insert({'state': list_ques_states})


# ===============================================================================================================
# States - END
# ===============================================================================================================





















list_query = []
dict_collections = {}

# To get the elements present in the collection in DB
db.cursor = db.mountain_question.find()
corpus = []
for i in db.cursor:
    corpus = i['list_ques_mountain']
# print('corpus: ', corpus)


dict_collections['mt'] = 'mountain'
dict_collections['mountain'] = 'mountain'
dict_collections['city'] = 'cities'
dict_collections['cities'] = 'cities'
dict_collections['state'] = 'state'
dict_collections['st'] = 'state'
dict_collections['lake'] = 'lake'
dict_collections['river'] = 'river'
dict_collections['rivers'] = 'river'

# Question to be compared in the DB
tokens = nltk.word_tokenize('What is the height of mountain St Elias?')

# POS Tagging
pos_tags = nltk.pos_tag(tokens)
pos_tree = nltk.ne_chunk(pos_tags)
print('11', pos_tags)

# Store our required POS tagged words in a list_query
for i in pos_tags:
    if i[1] == 'NNP' or i[1] == 'NN' or i[1] == 'JJ' or i[1] == 'JJS' or i[1] == 'NNS':
        list_query.append(i[0])


collection_name = ''
for i in list_query:
    if dict_collections.get(i):
        collection_name=dict_collections[i]


# print(list_query)

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


# '''remove punctuation, lowercase, stem'''
def normalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punctuation_map))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]

similarity = {}
for document in corpus:
    similarity[document]=cosine_sim(document, str(list_query))

# Unsorted
# print(similarity)

# Sorted
print('buedjns')
print(sorted(similarity.items(), key=itemgetter(1), reverse=True))
print('buedjns')


