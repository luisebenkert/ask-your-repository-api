from consecution import Node, Pipeline, GlobalState
from textblob import TextBlob, Word

from application.artifacts.text_processing import Spellcheck, PartOfSpeechFilter, Lemmatization, PriorityFilter, Stemming, Synonyms, OuterSynonyms
from application.artifacts.text_processing.variables import ALL_VARIABLES, MAXIMUM_AMOUNT
from application.artifacts.text_processing.utils import get_string, combine_priorities, to_json, sort_dict

class Log(Node):
  def _pretty_print(self, text, indent=1):
    for key, value in text.items():
      if indent is 1:
        print('\t' * indent + str(key) + ':')
      else:
        print('\t' * indent + str(key) + ': ', end = '')
      if isinstance(value, dict):
         self._pretty_print(value, indent+1)
      else:
         print(' ' + str(value))
   
  def process(self, item):
    print()
    print('-----------------------------')
    print("After {}:".format(self.name[:-4]))
    self._pretty_print(item)
    print()
    print(get_string(item))
    print('-----------------------------')
    print()
    self.push(item) 

class Consumer(Node):
  def process(self, item):
    ''' Tokenization of user generated search terms and initialization of dict '''
    blob = TextBlob(item)
    words = blob.words
    search_terms = {}
    for word in words:
      amount = 1      
      if word in search_terms:        
        array = search_terms.get(word)
        amount = array.get('amount') + 1
      search_terms[word] = {
        'priority': 1.0,
        'amount': amount,
      }
    self.push(search_terms)

class Producer(Node):
  def process(self, item):
    ''' Enriched key words to string '''    
    string = get_string(item)
    best_keys= sort_dict(item)[:MAXIMUM_AMOUNT]
    reduced_list = {}
    for key in best_keys:
      reduced_list[key] = item[key]
    self.global_state.dictionary = reduced_list
    self.global_state.string = string

class TextProcessingPipeline:
  def __init__(self, *args):
    self.data = []
    self.data.append(args[0]["search_args"])
    self.team = args[0]["team_id"]
    self.pipeline = args[0]["pipeline"]

  def _get_pipeline(self, stages, log = False):
    pipe = (Consumer('Consumer'))
    if log:
      pipe = (pipe | Log('Consumer Log'))
    for stage in stages:      
      pipe = (pipe | stage)
      if log:
        name = str(stage)
        name = name[name.find("(")+1:name.find(")")] + ' Log'
        pipe = (pipe | Log(name))
    pipe = (pipe | Producer('Producer'))
    if log:
      pipe = (pipe | Log('Producer Log'))
    return pipe


  def run(self):
    global_state = GlobalState(string='', dictionary={})

    stages = {
      1: [],
      2: [      
        Spellcheck('Spellcheck'),
        PartOfSpeechFilter('Part of Speech Filter'),
        Synonyms('Synonyms'),
        PriorityFilter('Priority Filter'),
        Lemmatization('Lemmatization'),
        Stemming('Stemming'),
      ],
      3: [      
        Spellcheck('Spellcheck'),
        PartOfSpeechFilter('Part of Speech Filter'),
        Synonyms('Synonyms'),
        PriorityFilter('Priority Filter'),
        Lemmatization('Lemmatization'),
      ],
      4: [      
        Spellcheck('Spellcheck'),
        PartOfSpeechFilter('Part of Speech Filter'),
        Synonyms('Synonyms'),
        PriorityFilter('Priority Filter'),
      ],
      5: [      
        Spellcheck('Spellcheck'),
        PartOfSpeechFilter('Part of Speech Filter'),
        Synonyms('Synonyms'),
        OuterSynonyms('Outer Synonyms'),
        PriorityFilter('Priority Filter'),
        Lemmatization('Lemmatization'),
      ],
      6: [      
        Spellcheck('Spellcheck'),
        PartOfSpeechFilter('Part of Speech Filter'),
        Synonyms('Synonyms'),
        OuterSynonyms('Outer Synonyms'),
        Synonyms('Synonyms 2'),
        PriorityFilter('Priority Filter'),
        Lemmatization('Lemmatization'),
      ], 
      7: [      
        Spellcheck('Spellcheck'),
        PartOfSpeechFilter('Part of Speech Filter'),
        Synonyms('Synonyms'),
        OuterSynonyms('Outer Synonyms'),
        Synonyms('Synonyms 2'),
        OuterSynonyms('Outer Synonyms 2'),
        PriorityFilter('Priority Filter'),
        Lemmatization('Lemmatization'),
      ], 
    }

    version = stages[self.pipeline]
    pipeline = self._get_pipeline(version, False)    
    pipe = Pipeline(pipeline, global_state=global_state)
    pipe.consume(self.data)
    to_json(version, global_state.dictionary, self.data, self.team, ALL_VARIABLES)

    return global_state.dictionary