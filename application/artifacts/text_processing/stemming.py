from consecution import Node
from textblob import Word
from application.artifacts.text_processing.utils import get_word
from application.artifacts.text_processing.variables import STEMMER, STEMMERS

class Stemming(Node):  
  def process(self, item):
    words = get_word(item)
    stemmer = STEMMERS[STEMMER]    
    for word in words:
      new_word = stemmer.stem(word)
      item[new_word] = item.pop(word)
    self.push(item)