from consecution import Node, Pipeline, GlobalState
from textblob import TextBlob, Word

from application.artifacts.text_processing import Spellcheck, PartOfSpeechFilter, Lemmatization, PriorityFilter, Stemming, Synonyms
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
    self.global_state.dictionary = sort_dict(item)
    self.global_state.string = string

class TextProcessingPipeline:
  def __init__(self, *args):
    self.data = args

  def _get_pipeline(self, stages, log = False):
    pipe = (Consumer('Consumer') | Log('Consumer Log'))
    for stage in stages:      
      pipe = (pipe | stage)
      if log:
        name = str(stage)
        name = name[name.find("(")+1:name.find(")")] + ' Log'
        pipe = (pipe | Log(name))
    pipe = (pipe | Producer('Producer') | Log('Producer Log'))    
    return pipe

  def run(self):
    global_state = GlobalState(string='', dictionary={})
    stages1 = [      
      Spellcheck('Spellcheck'),
      PartOfSpeechFilter('Part of Speech Filter'),
      Synonyms('Synonyms'),
      PriorityFilter('Priority Filter'),
      Lemmatization('Lemmatization'),
      Stemming('Stemming'),
    ]

    pipeline = self._get_pipeline(stages1, True)
    pipe = Pipeline(pipeline, global_state=global_state)
    pipe.consume(self.data)
    to_json(pipe, global_state.dictionary, self.data)
    return global_state.string