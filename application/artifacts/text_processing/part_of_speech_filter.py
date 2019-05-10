from consecution import Node
from textblob import Word
from application.artifacts.text_processing.utils import getWord, getBlob
from application.artifacts.text_processing.variables import PART_OF_SPEECH_PRIORITY_FACTOR, PART_OF_SPEECH_PRIORITY_FUNCTION

class PartOfSpeechFilter(Node):
  def _calculate_priority(self, confidence, original_priority):
    return PART_OF_SPEECH_PRIORITY_FUNCTION(confidence, original_priority)

  def process(self, item): 
    print(item)    
    blob = getBlob(item)
    tagged_words = blob.tags
    for pair in tagged_words:        
      word = pair[0]
      tag = pair[1]
      original_priority = item[word]
      print(tag)      
      for pos in PART_OF_SPEECH_PRIORITY_FACTOR:
        tags = pos[0]
        if tag in tags:
          factor = pos[1]
      if factor is not None:
        priority = self._calculate_priority(factor, original_priority)
      else:
        priority = original_priority
      item[word] = priority
    print(item)
    self.push(item)