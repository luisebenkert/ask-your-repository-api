from textblob import Word, TextBlob, blob
import nltk

def get_word(list):
  result = []
  for item in list:
    word = Word(item)
    result.append(word)
  return result

def get_string(list):
  keys = []
  for key in list:
    keys.append(key)
  return ' '.join(keys) 

def get_blob(list):
  string = get_string(list)
  return TextBlob(string)

def combine_priorities(old_prio, new_prio):
  print(old_prio)
  print(new_prio)

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