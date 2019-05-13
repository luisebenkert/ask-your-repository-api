from consecution import Node
from textblob import Word
from application.artifacts.text_processing.utils import get_word
from application.artifacts.text_processing.variables import SPELLCHECK_MIN_CONFIDENCE, SPELLCHECK_PRIORITY_FUNCTION

class Spellcheck(Node):
  def _calculate_priority(self, confidence):
    return SPELLCHECK_PRIORITY_FUNCTION(confidence)

  def process(self, item):    
    words = get_word(item)
    for word in words:
      corrected_words = word.spellcheck()
      for element in corrected_words:
        word = element[0]
        confidence = element[1]
        if confidence > SPELLCHECK_MIN_CONFIDENCE:          
          prio = self._calculate_priority(confidence)             
          if word in item:
            item[word]['priority'] = prio
            item[word]['amount'] = item.get(word).get('amount') + 1
          else:
            item[word] = {
              'priority': prio,
              'amount': 1
            }
    self.push(item)