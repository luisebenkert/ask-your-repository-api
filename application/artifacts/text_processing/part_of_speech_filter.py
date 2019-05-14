from consecution import Node
from textblob import Word
from application.artifacts.text_processing.utils import get_blob
from application.artifacts.text_processing.variables import PART_OF_SPEECH_CATEGORIES, PART_OF_SPEECH_PRIORITY_FUNCTION

class PartOfSpeechFilter(Node):
  def _calculate_priority(self, confidence, original_priority):
    return PART_OF_SPEECH_PRIORITY_FUNCTION(confidence, original_priority)

  def process(self, item):
    blob = get_blob(item)
    tagged_words = blob.tags
    for pair in tagged_words:        
      word = pair[0]
      tag = pair[1]
      original_priority = item[word]['priority']
      for key, value in PART_OF_SPEECH_CATEGORIES.items():
        tags = value.get('pos')
        if tag in tags:
          factor = value.get('value')
      if factor is not None:
        priority = self._calculate_priority(factor, original_priority)
      else:
        priority = original_priority
      item[word]['priority'] = priority
    self.push(item)