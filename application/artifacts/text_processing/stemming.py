from consecution import Node
from textblob import Word
from nltk.stem import PorterStemmer
from application.artifacts.text_processing.utils import get_word, combine_priorities
from application.artifacts.text_processing.variables import SPELLCHECK_MIN_CONFIDENCE, SPELLCHECK_PRIORITY_FACTOR, SPELLCHECK_PRIORITY_FUNCTION

class Stemming(Node):
  def process(self, item):    
    words = get_word(item)
    ps = PorterStemmer()
    for word in words:
      new_word = ps.stem(word) 
      print(new_word)
    self.push(item)