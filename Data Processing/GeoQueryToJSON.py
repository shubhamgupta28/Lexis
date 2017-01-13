dic=[]
cities=[]
river=[]
border=[]
road=[]
lake=[]
mountain=[]
highlow=[]
import re
from pymongo import MongoClient


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



with open('geobase.txt') as f:
    lines = f.readlines()
    for line in lines:
        t=re.match('.*\(',line)
        key=t.group()[:len(t.group())-1]

        line=re.sub('.*\(|\)|\.|\'|\\n','',line)
        u=line.split(',')
        print(u)
        if(key == 'state'):
            dic.append({'name':u[0],'code':u[1],'captial':u[2],'population':u[3], 'area':u[4], 'state_number':u[5],'cities':[u[6],u[7],u[8],u[9]]})
        if(key == 'city'):
            cities.append({'state':u[0],'code':u[1],'city':u[2],'population':u[3]})
        if(key == 'river'):
            print(line)
            river.append({'name':u[0],'length':u[1], 'states':u[2:]})
        if(key=='border'):
            if u[2]:
                border.append({'state':u[0],'state_abbreviation':u[1],'bordering_states':u[2:]})
        if(key == 'road'):
            road.append({'number':u[0],'states':u[1:]})
        if(key=='lake'):
            lake.append({'name':u[0],'area':u[1],'states':u[2:]})
        if (key == 'mountain'):
            mountain.append({'state': u[0], 'code': u[1], 'mountain_name': u[2:],'height':u[3]})
        if (key == 'highlow'):
            #state, state_abbreviation, highest_point, highest_elevation, lowest_point, lowest_elevation
            highlow.append({'state': u[0], 'code': u[1], 'highest_point': u[2:],'highest_elevation':u[3],'lowest_point':u[4],'lowest_elevation':u[5]})


db.state.insert(dic)
db.river.insert(river)
db.border.insert(border)
db.cities.insert(cities)
db.road.insert(road)
db.lake.insert(lake)
db.mountain.insert(mountain)
db.highlow.insert(highlow)

print(river)
