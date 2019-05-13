from consecution import Node, Pipeline, GlobalState
from textblob import TextBlob, Word

from application.artifacts.text_processing import Spellcheck, PartOfSpeechFilter, Lemmatization, Filter, Stemming
from application.artifacts.text_processing.utils import get_string, combine_priorities

class Log(Node):
  def process(self, item):
    print("After {} the values are {}".format(self.name, item))
    print()
    print(get_string(item))
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
    self.global_state.result = string  

class TextProcessingPipeline:
  def __init__(self, *args):
    self.data = args

  def run(self):
    global_state = GlobalState(result='')
    pipe = Pipeline(
      Consumer('Consumer') |
      Log('ConsumerLog') |
      Spellcheck('Spellcheck') | 
      Log('SpellcheckLog') |
      PartOfSpeechFilter('Part of Speech Filter') | 
      Log('Part of Speech FilterLog') |
      Lemmatization('Lemmatization') |
      Log('LemmatizationLog') |
      Filter('Filter') |
      Log('FilterLog') |
      Stemming('Stemming') |
      Log('StemmingLog') | 
      Producer('Producer'), 
      global_state=global_state
    )
    pipe.consume(self.data)
    return global_state.result