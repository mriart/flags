# Flags
# Marc Riart, Dec 2014

import os
import random
import bottle
from bottle import static_file, template, post, request
from beaker.middleware import SessionMiddleware


# Initialization variables
# The first 3 represents the range of the quiz
# bottle.TEMPLATE_PATH is the relative path to the templates for rendering html

NUM_ENTRIES = 136
NUM_QUESTIONS = 5
NUM_POSSIBILITIES = 3                   # For the moment, only works with 3
bottle.TEMPLATE_PATH = ['./template']


# Load entries from file into a list
# Each entry is itself a list of 2 elements: country, file_of_flag_image.jpg

f = open("countries_flags.txt", "r")
entries = []
for line in f:
    poscol = line.find(":")
    e1 = line[:poscol]
    e2 = line[poscol+1:-1]
    entries.append([e1, e2])


# Get question. Takes the previous history in order to not repeat a question

def get_question(quest_history):
    q = random.randint(0, NUM_ENTRIES-1)
    while q in quest_history:
        q = random.randint(0, NUM_ENTRIES-1)
    return q

    
# Get possibilities. Checks to not repeat any possibility

def get_possibilities(quest):
    p = [quest]
    for i in range(NUM_POSSIBILITIES-1):
        p_next = random.randint(0, NUM_ENTRIES-1)
        while p_next in p:
            p_next = random.randint(0, NUM_ENTRIES-1)
        p.append(p_next)
        random.shuffle(p)
    return p


# Define session options
# The session object also have 3 additional elements in the dictionary:
#   'quest_index', the index of the question
#   'quest_history', a list of previous questions
#   'answer_history', the same list of before with the answers chosen

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)


# Define the route of start quiz (the / uri)

@bottle.route('/')
def start():
    return static_file('start.html', root='./static')


# Define the route of images

@bottle.route('/img/<filename>')
def image(filename):
    return static_file(filename, root='./img')


# Define the route of the first question
# It is a GET method. Initializes the session and more

@bottle.route('/q')
def question_first():
    s = bottle.request.environ.get('beaker.session')
    s['quest_index'] = 1
    s['quest_history'] = []
    s['answer_history'] = []
    i = s['quest_index']
    h = s['quest_history']
    
    q = get_question(h)
    p = get_possibilities(q)
    
    # cheat = 'Question: ' + str(q) + ' Pos: ' + str(p) + ' Flag: ' + entries[q][1]
    return template(
            'question',
            i=i,
            # cheat=cheat,
            q=q,
            flag=entries[q][1],
            p0=p[0],
            p0_text=entries[p[0]][0],
            p1=p[1],
            p1_text=entries[p[1]][0],
            p2=p[2],
            p2_text=entries[p[2]][0]
           )


# Define the route of the following questions, from 2 to NUM_QUESTIONS
# It is a POST method

@bottle.post('/q')
def question_next():
    # First, update session
    s = bottle.request.environ.get('beaker.session')
    s['quest_index'] = s['quest_index'] + 1
    last_quest = request.forms.get('quest')
    last_answer = request.forms.get('answer')
    s['quest_history'].append(last_quest)
    s['answer_history'].append(last_answer)

    # Last was not the last question, proceed with next question
    if s['quest_index'] <= NUM_QUESTIONS:
        i = s['quest_index']
        h = s['quest_history']
        q = get_question(h)
        p = get_possibilities(q)
        
        # cheat = 'Question: ' + str(q) + ' Pos: ' + str(p) + ' Flag: ' + entries[q][1]
        return template(
                'question',
                i=i,
                # cheat=cheat,
                q=q,
                flag=entries[q][1],
                p0=p[0],
                p0_text=entries[p[0]][0],
                p1=p[1],
                p1_text=entries[p[1]][0],
                p2=p[2],
                p2_text=entries[p[2]][0]
               )

    # Last was the last question, print the results
    h = s['quest_history']
    a = s['answer_history']
    res = 0
    j = 0
    reviews = []
    for i in h:
        if i == a[j]:
            res = res + 1
            reviews.append(['/img/' + entries[int(i)][1], entries[int(i)][0], ' - OK'])
        else:
            reviews.append(['/img/' + entries[int(i)][1], entries[int(i)][0], ' - KO'])        
        j = j + 1        

    return template(
            'result',
            score=res,
            num_questions=NUM_QUESTIONS,    
            reviews=reviews
           )
 


# Run the HTTP Server

server_host_port = int(os.getenv('VCAP_APP_PORT', 8081))
server_host_name = os.getenv('VCAP_APP_HOST', 'localhost')
bottle.run(app=app, host=server_host_name, port=server_host_port)
