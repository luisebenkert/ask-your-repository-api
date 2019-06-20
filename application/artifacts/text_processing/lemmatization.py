from consecution import Node
from textblob import Word, TextBlob, blob
import nltk
from application.artifacts.text_processing.utils import get_word, to_wordnet
from application.artifacts.text_processing.variables import LEMMATIZATION_FUNCTION

class Lemmatization(Node):

  def process(self, item):
    words = get_word(item)
    to_add = {}
    to_delete = []
    for word in words:
      string = ''.join(word)
      blob = TextBlob(string)
      tag = blob.tags[0][1]   
      pos = to_wordnet(tag)      
      new_word = str(word.lemmatize(pos))
      if new_word != word:
        if new_word in item:
          prio1 = item.get(word).get('priority')
          prio2 = item.get(new_word).get('priority')
          to_add[new_word] = {
            'priority': max(prio1, prio2),
            'amount': item.get(word).get('amount') + 1
          }
          to_delete.append(word)
        else:
          to_add[new_word] = item.pop(word)
    for element in to_add:
      item[element] = to_add[element]
    for element in to_delete:
      del item[element]
    self.push(item)