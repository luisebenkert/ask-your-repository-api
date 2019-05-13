from consecution import Node, Pipeline, GlobalState
from textblob import TextBlob, Word

from application.artifacts.text_processing import Spellcheck, PartOfSpeechFilter, Lemmatization, PriorityFilter, Stemming, Synonyms
from application.artifacts.text_processing.utils import get_string, combine_priorities

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
    print('----------')
    print("After {}:".format(self.name))
    self._pretty_print(item)
    print()
    print(get_string(item))
    print('----------')
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
    stages = [      
      Spellcheck('Spellcheck'),
      PartOfSpeechFilter('Part of Speech Filter'),
      Synonyms('Synonyms'),
      PriorityFilter('PriorityFilter'),
      Lemmatization('Lemmatization'),
      Stemming('Stemming'),
    ]

    pipe2 = (Consumer('Consumer') | Log('ConsumerLog'))
    for stage in stages:      
      pipe2 = (pipe2 | stage)
    pipe2 = (pipe2 | Producer('Producer'))
    print('#################')
    print(Pipeline(pipe2, global_state=global_state))

    pipe = Pipeline(
      Consumer('Consumer') |
      Log('ConsumerLog') |
      Spellcheck('Spellcheck') | 
      Log('SpellcheckLog') |
      PartOfSpeechFilter('Part of Speech Filter') | 
      Log('Part of Speech FilterLog') |
      Synonyms('Synonyms') |
      Log('SynonymsLog') |
      PriorityFilter('PriorityFilter') |
      Log('PriorityFilterLog') |
      Lemmatization('Lemmatization') |
      Log('LemmatizationLog') |
      Stemming('Stemming') |
      Log('StemmingLog') | 
      Producer('Producer'), 
      global_state=global_state
    )
    print(pipe)
    pipe.consume(self.data)
    return global_state.result