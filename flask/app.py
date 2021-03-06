# Author: Chet Lemon (http://github.com/clemon)
from flask import request, Flask, jsonify
import ner
import nltk
import parsedatetime as pdt

app = Flask(__name__)

@app.route('/')
def index():
    return "Chet Lemon - Olset Backend/API challenge"

# POST - parse
# input: '{"sentence" : "String sentence"}'
# ex return: { "dates" : ["mm/dd/yy"],
#            "durations" : ["5 days"],
#            "locations" : ["Chicago"]}
@app.route('/api/1.0/parse', methods=['POST'])
def parse_sent():
    
    # initializing some variables
    locations = []
    dates = []
    uniformDates = []
    durations = []
    cal = pdt.Calendar()

    # quick error check
    if not request.json or not 'sentence' in request.json:
        abort(400)

    # connect to the instance of stanford ner
    tagger = ner.SocketNER(host='localhost', port=8080)
    sentence = request.json['sentence']

    # gets the named entities (LOCATION, DATE)
    parsedSent = tagger.get_entities(sentence)

    # handle the absense of "DURATION"
    tokens = nltk.word_tokenize(sentence)   # nltk's pos tagger 
    pos_tags = nltk.pos_tag(tokens)

    # populate dates and locations if they exist
    try:
        dates = parsedSent['DATE']
    except KeyError:
        if ('tomorrow' or 'tommorow' or 'tommorrow') in tokens:
            dates.append('tomorrow')
        else:
            print 'no DATE found'

    try:
        locations = parsedSent['LOCATION']
    except KeyError:
        print 'no LOCATION found'

    # iterate over each tuple of (word, pos)
    for i, (word,pos) in enumerate(pos_tags):
        if word.lower() == ('days' or 'months' or 'years' or 
                            'day' or 'month' or 'year'):
            tup = pos_tags[i-1]
            if tup[1] == 'CD':     # if i-1 tagged as number
                # this is a valid duration
                durations.append(tup[0]+' '+pos_tags[i][0])
            elif tup[0].lower() == 'a': # if i-1 is 'a' 
                # this is a valid duration
                durations.append(tup[0]+' '+pos_tags[i][0])

    # formatting the dates uniformly as mm/dd/yy
    for entry in dates:
        parsed = cal.parse(entry)
        month ='0'+str(parsed[0][1]) if (parsed[0][1] < 10)else str(parsed[0][1])
        day = '0'+str(parsed[0][2]) if (parsed[0][2] < 10) else str(parsed[0][2])
        twodig = str(parsed[0][0])[-2:]
        year = '0'+twodig if (int(twodig) < 10) else twodig
        newDate = month+'/'+day+'/'+year
        uniformDates.append(newDate)

    return jsonify({'locations':locations, 'dates':uniformDates, 
        'durations':durations}), 201


if __name__ == '__main__':
    app.run(debug=True)
