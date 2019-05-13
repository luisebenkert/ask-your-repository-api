from consecution import Node
from textblob import Word, TextBlob, blob
import nltk
from application.artifacts.text_processing.utils import get_word, get_blob, get_string
from application.artifacts.text_processing.variables import nouns, verbs, ad_words, wh_words, pronouns, foreign, number, others

class Lemmatization(Node):
  def _calculate_prio(self, old_prio, new_prio):
    return max([old_prio, new_prio])

  def to_wordnet(self, tag=None):
    """Converts a Penn corpus tag into a Wordnet tag."""
    _wordnet = blob._wordnet
    if tag in ("NN", "NNS", "NNP", "NNPS"):
      return _wordnet.NOUN
    elif tag in ("JJ", "JJR", "JJS"):
      return _wordnet.ADJ
    elif tag in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ"):
      return _wordnet.VERB
    elif tag in ("RB", "RBR", "RBS"):
      return _wordnet.ADV
    else:
      return _wordnet.NOUN

  def process(self, item):
    words = get_word(item)
    to_add = {}
    to_delete = []
    for word in words:
      string = ''.join(word)
      blob = TextBlob(string)
      tag = blob.tags[0][1]   
      pos = self.to_wordnet(tag)      
      new_word = str(word.lemmatize(pos))
      if new_word != word:
        if new_word in item:
          prio1 = item.get(word).get('priority')
          prio2 = item.get(new_word).get('priority')
          to_add[new_word] = {
            'priority': self._calculate_prio(prio1, prio2),
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