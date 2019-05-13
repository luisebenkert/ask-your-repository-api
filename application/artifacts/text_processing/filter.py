from consecution import Node
from textblob import Word
from application.artifacts.text_processing.utils import get_word
from application.artifacts.text_processing.variables import FILTER_FUNCTION

class Filter(Node):
  def process(self, item):
    keys = []
    for word in item:
        prio = item.get(word).get('priority')
        if FILTER_FUNCTION(prio):
            keys.append(word)
    for key in keys:        
        del item[key]
    self.push(item)