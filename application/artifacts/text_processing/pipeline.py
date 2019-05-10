from consecution import Node, Pipeline, GlobalState
from textblob import TextBlob, Word

from application.artifacts.text_processing.spellcheck import Spellcheck
from application.artifacts.text_processing.part_of_speech_filter import PartOfSpeechFilter

class Consumer(Node):
  def process(self, item):
    blob = TextBlob(item)
    words = blob.words
    search_terms = {}
    for word in words:
      search_terms[word] = 1    
    self.push(search_terms)

class Producer(Node):
  def process(self, item):
    keys = []
    for key in item:
      keys.append(key)    
    self.global_state.result = ' '.join(keys)    

class TextProcessingPipeline:
  def __init__(self, *args):
    self.data = args

  def run(self):
    global_state = GlobalState(result='')
    pipe = Pipeline(
      Consumer('Consumer') |
      Spellcheck('Spellcheck') |
      PartOfSpeechFilter('Part of Speech Filter') |
      Producer('Producer'),
      global_state=global_state
    )
    pipe.consume(self.data)
    return global_state.result