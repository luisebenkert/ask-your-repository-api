from consecution import Node
from textblob import Word
from application.artifacts.text_processing.utils import getWord
from application.artifacts.text_processing.variables import SPELLCHECK_MIN_CONFIDENCE, SPELLCHECK_PRIORITY_FACTOR, SPELLCHECK_PRIORITY_FUNCTION

class Spellcheck(Node):
  def _calculate_priority(self, confidence):
    return SPELLCHECK_PRIORITY_FUNCTION(confidence)

  def process(self, item):    
    words = getWord(item)
    for word in words:
      corrected_words = word.spellcheck()
      for element in corrected_words:
        word = element[0]
        confidence = element[1]        
        if confidence > SPELLCHECK_MIN_CONFIDENCE:
          item[word] = self._calculate_priority(confidence)
    print(item)
    self.push(item)