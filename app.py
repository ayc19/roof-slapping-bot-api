from flask import Flask, jsonify
from flask_cors import CORS
import requests
import re
import random
import inflect
p = inflect.engine()


app = Flask(__name__)
CORS(app)

BASE_URL = 'http://api.conceptnet.io/c/en/'

# just makes a GET request to the concept net api
def retrieve_word_details(word):
    return requests.get('http://api.conceptnet.io/c/en/{}'.format(word)).json()

"""
Boolean that returns True if the relation on the edge is of the following
RelatedTo, CapableOf, HasA, or AtLocation
"""
def is_fitting(edge):
    potential_relations = [
        # '/r/RelatedTo',
        '/r/CapableOf',
        # '/r/HasA',
        '/r/AtLocation'
        # '/r/Desires'
    ]
    relation = edge['rel']['@id']
    return relation in potential_relations

"""
Function to get the type of edge:
AtLocation, RelatedTo, etc... 
"""
def get_edge_type(edge):
    relation = edge['rel']['@id']
    return relation.split('/')[-1]

# attempt 1 at generating slap text, 
# realized that I can't simply use the surface text since it doesn't always follow the same format. sad
# keeping it as reference for future one
# split this up into generate_fitting_text and generate_capable_of_text
def generate_slap_text(surface_text, edge_type, word):
    print(surface_text)
    words = re.findall('\[\[.*?\]\]', surface_text) # return a list of words, still in the brackets
    
    # go through and remove the [[]] surrounding each word
    for i in range(len(words)):
        words[i] = words[i][2:-2]
    
    # swap the words so that the end word the one that's not the original
    if word in words[1]:
        words[0], words[1] = words[1], words[0]

    print(words)
    if edge_type == 'CapableOf':
        verb = words[-1]
        plural_verb = p.plural(verb)
        print("*Slaps roof of {}* 'This bad boy can do so many {}'".format(word, plural_verb))
        return "*Slaps roof of {}* 'This bad boy can do so many {}'".format(word, plural_verb)
    elif edge_type == 'AtLocation':
        item = words[-1]
        # item = item.replace('a ', '')
        # item = item.replace('an', '')
        # item = item.replace('the', '')
        items = p.singular_noun(item)

        plural_word = p.plural(word)
        if word == item or word == plural_word:
            return False
        print("*Slaps roof of {}* 'This bad boy can fit so many {} in it'".format(word, p.plural(item)))
        return "*Slaps roof of {}* 'This bad boy can fit so many {}'".format(item, plural_word)

"""
start/end are dictionaries containing the key words used in the surface text

this function will generate text such as this __ can fit so many __ in it
"""
def generate_fitting_text(start, end):
    container = end['@id']
    container = container.split('/')[-1]

    item = start['@id']
    item = item.split('/')[-1]

    # Now go through and separate out any words that need to by underscores
    item = ' '.join(item.split('_'))
    container = ' '.join(container.split('_'))

    return "*Slaps roof of {}* This bad boy can fit so many {} in it.".format(container, p.plural(item))

def generate_capable_of_text(start, end):
    verb = end['@id']
    verb = verb.split('/')[-1]

    item = start['@id']
    item = item.split('/')[-1]

    item = ' '.join(item.split('_'))
    verb = ' '.join(verb.split('_'))

    print("*Slaps roof of {}* This bad boy is capable of so many {}.".format(item, p.plural(verb)))
    return "*Slaps roof of {}* This bad boy is capable of so many {}.".format(item, p.plural(verb))


# ********************* ROUTES *********************

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/word/')
def prompt_word():
    return 'Need to input a word!'

@app.route('/word/<word>')
def get_word(word):
    edges = retrieve_word_details(word)['edges']

    # @context, @id, edges, view
    # for key in data:
    #     print(key)
    texts = []
    for edge in edges:
        print(edge['start'])
        print(edge['end'])
        print(edge['rel'])
        print('---------------------')
        text = None
        edge_type = get_edge_type(edge)
        surface_text = edge['surfaceText']
        if edge_type == 'CapableOf' or edge_type == 'UsedFor':
            text = generate_capable_of_text(edge['start'], edge['end'])
        elif edge_type == 'AtLocation':
            text = generate_fitting_text(edge['start'], edge['end'])
        texts.append(text)
    
    texts = list(filter(None, texts))

    if len(texts) == 0:
        return 'No results: try again'

    return jsonify({
        'word': word,
        'text': random.choice(texts)
    })
